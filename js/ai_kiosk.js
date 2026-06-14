import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getFunctions, httpsCallable } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-functions.js";

// Initialize Firebase (Using same config as form_handler)
const firebaseConfig = {
  projectId: "hcdp-digital-inbox",
  appId: "1:884194084346:web:ee44e3410c73322a631043",
  storageBucket: "hcdp-digital-inbox.firebasestorage.app",
  apiKey: "AIzaSyBMSgg__pJEm6NESKJe6l72UydEWZpdMhw",
  authDomain: "hcdp-digital-inbox.firebaseapp.com",
  messagingSenderId: "884194084346",
  projectNumber: "884194084346",
};

const app = initializeApp(firebaseConfig);
const functions = getFunctions(app);

// Connect to the Cloud Function
const askVoterQuestion = httpsCallable(functions, 'askVoterQuestion');

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("kioskForm");
  const input = document.getElementById("questionInput");
  const askButton = document.getElementById("askButton");
  const chatBox = document.getElementById("chatBox");

  function appendMessage(text, sender, isMarkdown = false) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}`;
    
    if (isMarkdown && typeof marked !== 'undefined') {
      msgDiv.innerHTML = marked.parse(text);
    } else {
      msgDiv.textContent = text;
    }
    
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
  }

  function appendLoading() {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ai`;
    msgDiv.id = "loadingMsg";
    msgDiv.innerHTML = `
      <div class="loading-dots">
        <div></div><div></div><div></div>
      </div>
    `;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    // Add user question to UI
    appendMessage(question, 'user');
    input.value = '';
    
    // Disable inputs
    askButton.disabled = true;
    input.disabled = true;

    // Show loading indicator
    const loadingEl = appendLoading();

    try {
      // Call Firebase Cloud Function
      const result = await askVoterQuestion({ question: question });
      
      // Remove loading indicator
      if(loadingEl) loadingEl.remove();

      if (result.data.success) {
        appendMessage(result.data.answer, 'ai', true);
      } else {
        appendMessage("I'm sorry, I encountered an error processing your request.", 'ai');
      }
    } catch (error) {
      console.error("Cloud function error:", error);
      if(loadingEl) loadingEl.remove();
      appendMessage("I'm having trouble connecting to headquarters right now. Please try again later.", 'ai');
    } finally {
      // Re-enable inputs
      askButton.disabled = false;
      input.disabled = false;
      input.focus();
    }
  });
});
