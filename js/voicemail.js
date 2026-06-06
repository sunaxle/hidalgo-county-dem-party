import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getStorage, ref, uploadBytes } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-storage.js";

const firebaseConfig = {
  projectId: "hcdp-digital-inbox",
  appId: "1:884194084346:web:ee44e3410c73322a631043",
  storageBucket: "hcdp-digital-inbox.firebasestorage.app",
  apiKey: "AIzaSyBMSgg__pJEm6NESKJe6l72UydEWZpdMhw",
  authDomain: "hcdp-digital-inbox.firebaseapp.com",
  messagingSenderId: "884194084346",
  projectNumber: "884194084346"
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

document.addEventListener('DOMContentLoaded', () => {
  const recordBtn = document.getElementById('record-btn');
  const recordStatus = document.getElementById('record-status');
  const recordIcon = document.getElementById('record-icon');

  if (!recordBtn) return;

  let mediaRecorder;
  let audioChunks = [];
  let isRecording = false;

  recordBtn.addEventListener('click', async () => {
    if (!isRecording) {
      // Start Recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
          if (event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          recordStatus.innerHTML = '<span style="color: #fcd34d;">Uploading and transcribing... ⏳</span>';
          
          try {
            // Upload raw audio to Firebase Storage
            const timestamp = Date.now();
            const storageRef = ref(storage, `voicemails/voicemail_${timestamp}.webm`);
            await uploadBytes(storageRef, audioBlob);

            // Once uploaded, the backend Cloud Function will trigger, transcribe it, and save to Firestore
            recordStatus.innerHTML = '<span style="color: #4ade80;">Success! Your voice message has been sent to the Chairman. ✅</span>';
          } catch (error) {
            console.error("Upload failed", error);
            recordStatus.innerHTML = '<span style="color: #ef4444;">Upload failed. Please check your connection.</span>';
          }

          setTimeout(() => {
            recordStatus.textContent = 'Tap to record a voice message';
          }, 5000);
        };

        mediaRecorder.start();
        isRecording = true;
        recordBtn.classList.add('recording-pulse');
        recordIcon.innerHTML = '🛑'; // Stop icon
        recordStatus.innerHTML = '<span style="color: #ef4444; font-weight: bold;">Recording... Tap to stop. 🔴</span>';
      } catch (err) {
        console.error("Microphone access denied or error:", err);
        recordStatus.innerHTML = '<span style="color: #ef4444;">Microphone access denied. Please allow permissions.</span>';
      }
    } else {
      // Stop Recording
      mediaRecorder.stop();
      isRecording = false;
      recordBtn.classList.remove('recording-pulse');
      recordIcon.innerHTML = '🎤'; // Mic icon
      
      // Stop all tracks to turn off the microphone light
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
  });
});
