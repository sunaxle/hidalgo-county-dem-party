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
      tbody.innerHTML = `<tr><td colspan="5" style="padding: 2rem; text-align: center; color: #cbd5e1;">No submissions yet.</td></tr>`;
      return;
    }

    snapshot.forEach((doc) => {
      const data = doc.data();
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid #e2e8f0";
      
      // Handle timestamp safely
      let dateString = "Just now";
      if (data.timestamp) {
        const date = data.timestamp.toDate();
        dateString = date.toLocaleString();
      }

      const formType = data.formType || "General Intake";
      const name = data.name || data.firstName + " " + (data.lastName || "") || "Unknown";
      const email = data.email || "N/A";
      const phone = data.phone || "N/A";

      tr.innerHTML = `
        <td style="padding: 1rem; color: #64748b; font-size: 0.9rem;">${dateString}</td>
        <td style="padding: 1rem; color: #0f172a; font-weight: 600;">${name}</td>
        <td style="padding: 1rem; color: #2563eb;">
          <a href="mailto:${email}" style="color: inherit; text-decoration: none;">${email}</a>
        </td>
        <td style="padding: 1rem; color: #64748b;">${phone}</td>
        <td style="padding: 1rem;">
          <span style="background: rgba(59, 130, 246, 0.1); color: #2563eb; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">
            ${formType}
          </span>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }, (error) => {
    console.error("Error fetching live feed:", error);
    tbody.innerHTML = `<tr><td colspan="5" style="padding: 2rem; text-align: center; color: #ef4444;">Error loading live data. Do you have permission?</td></tr>`;
  });
});
