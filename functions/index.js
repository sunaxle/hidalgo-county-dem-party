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

exports.transcribeVoicemail = onObjectFinalized(async (event) => {
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
