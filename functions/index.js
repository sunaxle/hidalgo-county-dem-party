const { onObjectFinalized } = require("firebase-functions/v2/storage");
const { getFirestore } = require("firebase-admin/firestore");
const { initializeApp } = require("firebase-admin/app");
const { getStorage } = require("firebase-admin/storage");
const { GoogleGenAI } = require("@google/genai");
const os = require('os');
const path = require('path');

initializeApp();
const db = getFirestore();

// Initialize the Gemini AI SDK
const ai = new GoogleGenAI();

exports.transcribeVoicemail = onObjectFinalized(async (event) => {
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

    // Upload the audio file to the Gemini File API
    const uploadResult = await ai.files.upload({
        file: tempFilePath,
        mimeType: event.data.contentType || 'audio/webm',
    });

    // Request the transcription from Gemini 2.5 Flash
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: [
            uploadResult,
            "Please accurately transcribe the following audio voicemail. Return ONLY the exact transcribed text. Do not add any conversational filler, markdown formatting, or introductory remarks."
        ]
    });

    const transcript = response.text;
    console.log("Transcription successful:", transcript);

    // Save the transcription to the Firestore database for the Chairman to read
    await db.collection('VoiceMemos').add({
      transcript: transcript,
      audioPath: filePath,
      audioUrl: `gs://${fileBucket}/${filePath}`, // Storage URI
      timestamp: new Date().toISOString(),
      status: 'unread' // Marks it as unread in the admin dashboard
    });
    
    console.log("Successfully saved transcript to Firestore.");

  } catch (error) {
    console.error("Transcription error:", error);
  }
});
