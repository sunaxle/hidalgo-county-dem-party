import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { initializeAppCheck, ReCaptchaV3Provider } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app-check.js";
import {
  getFirestore,
  collection,
  addDoc,
  getDocs,
  query,
  orderBy,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

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

// Initialize Firebase App Check
const appCheck = initializeAppCheck(app, {
  provider: new ReCaptchaV3Provider('PENDING_RECAPTCHA_V3_SITE_KEY'),
  isTokenAutoRefreshEnabled: true
});

const db = getFirestore(app);

document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("shareStoryForm");
  const grid = document.querySelector(".story-masonry");

  if (!form || !grid) return;

  // 1. Fetch existing stories from Firestore and append to grid
  try {
    const q = query(collection(db, "community_stories"), orderBy("timestamp", "asc"));
    const snapshot = await getDocs(q);
    
    snapshot.forEach((doc) => {
      const data = doc.data();
      // Render to DOM
      const article = document.createElement("article");
      article.className = `story-card theme-border-${data.issue}`;
      
      let badgeLabel = data.issue;
      if (data.issue === "living") badgeLabel = "Cost of Living";
      if (data.issue === "immigration") badgeLabel = "Immigration & the Border";
      if (data.issue === "economy") badgeLabel = "Economy & Wages";
      if (data.issue === "abortion") badgeLabel = "Healthcare & Abortion";
      if (data.issue === "ai") badgeLabel = "Jobs & A.I.";

      article.innerHTML = `
        <span class="story-badge badge-${data.issue}">${badgeLabel}</span>
        <p class="story-content">${data.story}</p>
        <span class="story-author">${data.name || 'Anonymous'}</span>
      `;
      // Prepend so newest is at the top of the grid
      grid.prepend(article);
    });
  } catch (err) {
    console.error("Error loading stories from Firestore:", err);
  }

  // 2. Handle new submissions
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerText;
    submitBtn.disabled = true;
    submitBtn.innerText = "Submitting...";

    const name = document.getElementById("storyName").value;
    const issue = document.getElementById("storyIssue").value;
    const story = document.getElementById("storyText").value;

    try {
      await addDoc(collection(db, "community_stories"), {
        name: name,
        issue: issue,
        story: story,
        timestamp: serverTimestamp()
      });

      form.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem;">
          <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
          <h3 style="color: var(--primary); margin-bottom: 1rem;">Story Submitted!</h3>
          <p style="color: #666; font-size: 1.1rem; line-height: 1.5;">Thank you for sharing your perspective with the community. Your story is now live.</p>
        </div>
      `;

      // Render the new story immediately locally to give instant feedback
      const article = document.createElement("article");
      article.className = `story-card theme-border-${issue}`;
      
      let badgeLabel = issue;
      if (issue === "living") badgeLabel = "Cost of Living";
      if (issue === "immigration") badgeLabel = "Immigration & the Border";
      if (issue === "economy") badgeLabel = "Economy & Wages";
      if (issue === "abortion") badgeLabel = "Healthcare & Abortion";
      if (issue === "ai") badgeLabel = "Jobs & A.I.";

      article.innerHTML = `
        <span class="story-badge badge-${issue}">${badgeLabel}</span>
        <p class="story-content">${story}</p>
        <span class="story-author">${name || 'Anonymous'}</span>
      `;
      grid.prepend(article);

    } catch (err) {
      console.error("Error saving story:", err);
      alert("Failed to submit story. Please try again.");
      submitBtn.disabled = false;
      submitBtn.innerText = originalText;
    }
  });
});
