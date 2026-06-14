const { onObjectFinalized } = require("firebase-functions/v2/storage");
const { onRequest } = require("firebase-functions/v2/https");
const { getFirestore } = require("firebase-admin/firestore");
const { initializeApp } = require("firebase-admin/app");
const { getStorage } = require("firebase-admin/storage");
const { GoogleGenAI } = require("@google/genai");
const os = require('os');
const path = require('path');
const nodemailer = require('nodemailer');
const twilio = require('twilio');

initializeApp();
const db = getFirestore();

let ai;

exports.transcribeVoicemail = onObjectFinalized({ bucket: "hcdp-digital-inbox.firebasestorage.app" }, async (event) => {
  // Initialize the Gemini AI SDK lazily inside the function execution
  // This prevents local deployment compilation errors.
  if (!ai) {
    ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "PENDING_API_KEY" });
  }
  const fileBucket = event.data.bucket;
  const filePath = event.data.name; 

  // Only process files uploaded to the 'voicemails/' directory
  if (!filePath.startsWith('voicemails/')) {
    return;
  }

  console.log(`Processing voicemail audio: ${filePath}`);
  const bucket = getStorage().bucket(fileBucket);
  const file = bucket.file(filePath);

  try {
    // Download the audio file to a temporary directory
    const tempFilePath = path.join(os.tmpdir(), path.basename(filePath));
    await file.download({ destination: tempFilePath });

    // Read the audio file directly from the temp directory
    const fs = require('fs');
    const audioData = fs.readFileSync(tempFilePath);

    // Request the transcription from Gemini 2.5 Flash using inlineData
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: [
            {
                inlineData: {
                    data: audioData.toString("base64"),
                    mimeType: event.data.contentType || 'audio/webm'
                }
            },
            "Please accurately transcribe the following audio voicemail. Return ONLY the exact transcribed text. Do not add any conversational filler, markdown formatting, or introductory remarks."
        ]
    });

    const transcript = response.text;
    console.log("Transcription successful:", transcript);

    const metadata = event.data.metadata || {};
    const firstName = metadata.firstName || 'Anonymous';
    const lastName = metadata.lastName || '';
    const phone = metadata.phone || 'N/A';
    const email = metadata.email || '';

    // Save the transcription to the Firestore database for the Chairman to read
    await db.collection('VoiceMemos').add({
      transcript: transcript,
      audioPath: filePath,
      audioUrl: `gs://${fileBucket}/${filePath}`, // Storage URI
      timestamp: new Date().toISOString(),
      status: 'unread',
      firstName: firstName,
      lastName: lastName,
      phone: phone,
      email: email
    });
    
    console.log("Successfully saved transcript to Firestore.");

    const publicAudioUrl = `https://firebasestorage.googleapis.com/v0/b/${fileBucket}/o/${encodeURIComponent(filePath)}?alt=media`;

    // Send an automatic email to info@hidalgocountydems.org
    try {
      const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: 'info@hidalgocountydems.org',
          // Remove spaces from the app password, just in case
          pass: (process.env.EMAIL_APP_PASSWORD || '').replace(/\s+/g, '')
        }
      });

      const toEmails = ['info@hidalgocountydems.org'];
      if (email && email.includes('@')) {
        toEmails.push(email);
      }

      const mailOptions = {
        from: '"HCDP Digital Voicemail" <info@hidalgocountydems.org>',
        to: toEmails.join(', '),
        subject: '🎤 New Grassroots Voicemail Received!',
        text: `You have received a new digital voicemail from the website!\n\nCaller: ${firstName} ${lastName}\nPhone: ${phone}\nEmail: ${email || 'N/A'}\n\n---\n\nTRANSCRIPT:\n${transcript}\n\n---\n\nLISTEN TO AUDIO:\n${publicAudioUrl}\n\nTimestamp: ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })}`,
      };

      await transporter.sendMail(mailOptions);
      console.log("Successfully sent notification email to info@hidalgocountydems.org");
    } catch (emailError) {
      console.error("Failed to send email notification:", emailError);
    }

  } catch (error) {
    console.error("Transcription error:", error);
  }
});

const { onCall, HttpsError } = require("firebase-functions/v2/https");

// Smart SMS Blast Function
exports.sendSmsBlast = onCall(async (request) => {
  const message = request.data.message;
  
  if (!message || message.trim() === '') {
    throw new HttpsError('invalid-argument', 'Message content is required.');
  }

  const accountSid = process.env.TWILIO_ACCOUNT_SID;
  const authToken = process.env.TWILIO_AUTH_TOKEN;
  const twilioNumber = process.env.TWILIO_SENDER_NUMBER;

  if (!accountSid || !authToken) {
    console.error('Twilio credentials not configured.');
    throw new HttpsError('internal', 'SMS gateway not configured.');
  }

  const client = twilio(accountSid, authToken);
  
  // For safety during testing without a live list, we will use the test number from the frontend.
  // We format it simply, but it should include the country code.
  const inputTestNumber = request.data.testNumber;
  const testNumbers = inputTestNumber && inputTestNumber.trim() !== '' ? [inputTestNumber.trim()] : ["+19560000000"]; 
  let successCount = 0;
  let errorCount = 0;

  for (const number of testNumbers) {
    try {
      if (twilioNumber && twilioNumber !== 'PENDING') {
        await client.messages.create({
          body: message,
          from: twilioNumber,
          to: number
        });
        successCount++;
      } else {
        // Test mode: just log it
        console.log(`[TEST MODE] Would send SMS to ${number}: ${message}`);
        successCount++;
      }
    } catch (error) {
      console.error(`Failed to send SMS to ${number}:`, error);
      errorCount++;
    }
  }

  return { 
    success: true, 
    message: `SMS blast completed. ${successCount} sent, ${errorCount} failed.` 
  };
});

// Interactive AI Kiosk Assistant
exports.askVoterQuestion = onCall(async (request) => {
  const question = request.data.question;
  
  if (!question || question.trim() === '') {
    throw new HttpsError('invalid-argument', 'Question content is required.');
  }

  // Initialize the Gemini AI SDK lazily
  if (!ai) {
    ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "PENDING_API_KEY" });
  }

  try {
    const systemPrompt = `You are the official Digital Campaign Manager and voter assistant for the Hidalgo County Democratic Party. 
Your job is to answer questions from voters accurately, politely, and concisely. 
You must always encourage voters to vote for Democrats up and down the ballot. 
Keep your answers under 3 paragraphs. Use bullet points if it makes the answer clearer.
If you don't know the specific answer, direct them to call the party headquarters at (956) 672-7274 or email info@hidalgocountydems.org.`;

    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: [
            systemPrompt,
            `Voter Question: ${question}`
        ]
    });

    return {
      success: true,
      answer: response.text
    };
  } catch (error) {
    console.error("AI Generation error:", error);
    throw new HttpsError('internal', 'Failed to generate a response from the AI.');
  }
});

const { onSchedule } = require("firebase-functions/v2/scheduler");

// Automated SEO Inbound Traffic Engine
exports.generateSEOArticle = onSchedule("every 24 hours", async (event) => {
  // Initialize the Gemini AI SDK lazily
  if (!ai) {
    ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "PENDING_API_KEY" });
  }

  const systemPrompt = `You are an expert political blogger for the Hidalgo County Democratic Party in South Texas. 
Write a highly engaging, 400-word SEO-optimized blog post about one of the following local issues:
- How Democrats are bringing jobs to the Rio Grande Valley and supporting economic growth.
- Tracking local issues like gas prices, inflation, and helping working families.
- Helping out our teachers and fighting for public school funding.
- Optimistic news of good governance in our cities, such as drainage improvements, infrastructure, new buildings, and community assets.

Randomly select ONE of these topics and write a deep-dive, localized article.
The tone should be informative, inspiring, and clearly advocate for Democratic values and community engagement.
Use Markdown formatting for headers, bullet points, and bold text. 
Return ONLY the raw markdown content. No conversational filler.`;

  try {
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: [systemPrompt]
    });

    const content = response.text;
    
    // Extract a title from the first H1 or H2, or generate one
    const titleMatch = content.match(/^#+\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : "Hidalgo County Politics Update";

    await db.collection("seo_articles").add({
      title: title,
      content: content,
      timestamp: new Date().toISOString()
    });

    console.log("Successfully generated and saved SEO article.");
  } catch (error) {
    console.error("Failed to generate SEO article:", error);
  }
});

const { onDocumentCreated } = require("firebase-functions/v2/firestore");

// Notification on New Form Submission
exports.notifyOnNewSubmission = onDocumentCreated("form_submissions/{docId}", async (event) => {
  const snapshot = event.data;
  if (!snapshot) {
    return;
  }
  const data = snapshot.data();

  const firstName = data.firstName || data.name || 'Anonymous';
  const lastName = data.lastName || '';
  const phone = data.phone || 'N/A';
  const email = data.email || 'N/A';
  const formType = data.formType || 'General Intake';

  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: 'info@hidalgocountydems.org',
        pass: (process.env.EMAIL_APP_PASSWORD || '').replace(/\s+/g, '')
      }
    });

    // 1. Alert the Admin Team
    const adminMailOptions = {
      from: '"HCDP Alerts" <info@hidalgocountydems.org>',
      to: 'info@hidalgocountydems.org',
      subject: `🚨 New Submission: ${formType} from ${firstName}`,
      text: `You have received a new form submission on the website!\n\nType: ${formType}\nName: ${firstName} ${lastName}\nPhone: ${phone}\nEmail: ${email}\n\nTimestamp: ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })}\n\nLog in to the Admin Dashboard to view all submissions.`,
    };

    await transporter.sendMail(adminMailOptions);
    console.log("Successfully sent notification email to info@hidalgocountydems.org");

    // 2. Auto-reply to the Submitter
    if (email && email !== 'N/A' && email.includes('@')) {
      const userMailOptions = {
        from: '"Hidalgo County Democrats" <info@hidalgocountydems.org>',
        to: email,
        subject: `Welcome to the Team! We received your submission`,
        text: `Hi ${firstName},\n\nThank you for reaching out to the Hidalgo County Democratic Party! We have successfully received your submission for: ${formType}.\n\nOur team is reviewing your information and we will be in touch with you shortly. If you need immediate assistance or would like to send a direct message back to the party, please email us directly at info@hidalgocountydems.org.\n\nThank you for being part of the movement to build a better South Texas!\n\nBest regards,\nHidalgo County Democratic Party\n\n(Note: Please do not reply directly to this automated email. Send any individualized emails to info@hidalgocountydems.org)`,
      };

      await transporter.sendMail(userMailOptions);
      console.log(`Successfully sent auto-reply welcome email to ${email}`);
    }

  } catch (emailError) {
    console.error("Failed to send email notification:", emailError);
  }
});
