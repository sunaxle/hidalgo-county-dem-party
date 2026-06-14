import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  query,
  orderBy,
  limit,
  onSnapshot
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Initialize Firebase
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
const db = getFirestore(app);

document.addEventListener("DOMContentLoaded", () => {
  const tbody = document.getElementById("liveDataFeedBody");
  if (!tbody) return;

  const q = query(
    collection(db, "form_submissions"),
    orderBy("timestamp", "desc"),
    limit(50)
  );

  onSnapshot(q, (snapshot) => {
    tbody.innerHTML = "";
    
    if (snapshot.empty) {
      tbody.innerHTML = `<tr><td colspan="4" style="padding: 2rem; text-align: center; color: #008f11; font-family: 'Courier New', Courier, monospace;">No submissions yet.</td></tr>`;
      return;
    }

    snapshot.forEach((doc) => {
      const data = doc.data();
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px dashed #008f11";
      
      // Handle timestamp safely
      let dateString = "Just now";
      if (data.timestamp) {
        const date = data.timestamp.toDate();
        dateString = date.toLocaleString();
      }

      const formType = data.source || data.formType || "General Intake";
      const name = data.name || data.firstName + " " + (data.lastName || "") || "Unknown";
      const email = data.email || "N/A";
      const phone = data.phone || "N/A";

      const message = data.message || "(No message)";

      tr.innerHTML = `
        <td style="padding: 1rem; color: #008f11; font-size: 0.9rem; vertical-align: top; font-family: 'Courier New', Courier, monospace;">${dateString}</td>
        <td style="padding: 1rem; vertical-align: top;">
          <span style="background: rgba(0, 255, 65, 0.1); color: #00ff41; padding: 0.25rem 0.5rem; border: 1px solid #008f11; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; display: inline-block; font-family: 'Courier New', Courier, monospace;">
            ${formType}
          </span>
        </td>
        <td style="padding: 1rem; vertical-align: top;">
          <div style="color: #00ff41; font-weight: 600; margin-bottom: 0.25rem; font-family: 'Courier New', Courier, monospace; text-shadow: 0 0 3px rgba(0,255,65,0.5);">${name}</div>
          <div style="color: #008f11; font-size: 0.85rem; margin-bottom: 0.25rem; font-family: 'Courier New', Courier, monospace;"><a href="mailto:${email}" style="color: inherit; text-decoration: none;">${email}</a></div>
          <div style="color: #008f11; font-size: 0.85rem; font-family: 'Courier New', Courier, monospace;">${phone}</div>
        </td>
        <td style="padding: 1rem; color: #00ff41; font-size: 0.95rem; vertical-align: top; line-height: 1.5; white-space: pre-wrap; font-family: 'Courier New', Courier, monospace;">${message}</td>
      `;
      tbody.appendChild(tr);
    });
  }, (error) => {
    console.error("Error fetching live feed:", error);
    tbody.innerHTML = `<tr><td colspan="4" style="padding: 2rem; text-align: center; color: #ef4444; font-family: 'Courier New', Courier, monospace;">Error loading live data. Do you have permission?</td></tr>`;
  });
});
