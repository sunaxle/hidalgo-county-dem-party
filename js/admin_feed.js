import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
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

  const colRef = collection(db, "form_submissions");

  onSnapshot(colRef, (snapshot) => {
    tbody.innerHTML = "";
    
    // Update live metrics on the dashboard if present
    const countEl = document.querySelector(".metric-value.counter[data-target]");
    if (countEl) {
      countEl.innerText = snapshot.size;
    }

    if (snapshot.empty) {
      tbody.innerHTML = `<tr><td colspan="4" style="padding: 2rem; text-align: center; color: #008f11; font-family: 'Courier New', Courier, monospace;">No incoming submissions recorded yet. Submissions from Contact, Join, Subscribe, and Community forms will appear here in real time.</td></tr>`;
      return;
    }

    const items = [];
    snapshot.forEach((doc) => {
      items.push({ id: doc.id, ...doc.data() });
    });

    // Sort descending by timestamp/date
    items.sort((a, b) => {
      const getMs = (obj) => {
        if (!obj) return 0;
        if (obj.timestamp && typeof obj.timestamp.toDate === 'function') return obj.timestamp.toDate().getTime();
        if (obj.timestamp) {
          const t = new Date(obj.timestamp).getTime();
          if (!isNaN(t)) return t;
        }
        if (obj.createdAt) {
          const t = new Date(obj.createdAt).getTime();
          if (!isNaN(t)) return t;
        }
        return 0;
      };
      return getMs(b) - getMs(a);
    });

    items.forEach((data) => {
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px dashed #008f11";
      tr.style.transition = "background 0.2s ease";
      tr.addEventListener("mouseenter", () => tr.style.background = "rgba(0, 255, 65, 0.05)");
      tr.addEventListener("mouseleave", () => tr.style.background = "transparent");
      
      // Handle timestamp safely
      let dateString = "Just now";
      if (data.timestamp) {
        try {
          const date = typeof data.timestamp.toDate === 'function' ? data.timestamp.toDate() : new Date(data.timestamp);
          dateString = date.toLocaleString();
        } catch (e) {
          dateString = "Recently";
        }
      } else if (data.createdAt) {
        try {
          dateString = new Date(data.createdAt).toLocaleString();
        } catch(e) {
          dateString = "Recently";
        }
      }

      const formType = data.source || data.formType || "General Intake";
      const name = data.name || (data.firstName ? (data.firstName + " " + (data.lastName || "")).trim() : "") || "Anonymous";
      const email = data.email || "N/A";
      const phone = data.phone || "N/A";
      const zipcode = data.zipcode ? ` [ZIP: ${data.zipcode}]` : "";

      const message = data.message || "(No additional text)";

      tr.innerHTML = `
        <td style="padding: 1rem; color: #008f11; font-size: 0.85rem; vertical-align: top; font-family: 'Courier New', Courier, monospace; white-space: nowrap;">${dateString}</td>
        <td style="padding: 1rem; vertical-align: top;">
          <span style="background: rgba(0, 255, 65, 0.1); color: #00ff41; padding: 0.25rem 0.5rem; border: 1px solid #008f11; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; display: inline-block; font-family: 'Courier New', Courier, monospace; border-radius: 2px;">
            ${formType}
          </span>
        </td>
        <td style="padding: 1rem; vertical-align: top;">
          <div style="color: #00ff41; font-weight: 700; margin-bottom: 0.25rem; font-family: 'Courier New', Courier, monospace; text-shadow: 0 0 3px rgba(0,255,65,0.5);">${name}${zipcode}</div>
          <div style="color: #008f11; font-size: 0.85rem; margin-bottom: 0.25rem; font-family: 'Courier New', Courier, monospace;">
            ${email !== "N/A" ? `<a href="mailto:${email}" style="color: #00ff41; text-decoration: underline;">${email}</a>` : '<span style="color: #555;">No email</span>'}
          </div>
          <div style="color: #008f11; font-size: 0.85rem; font-family: 'Courier New', Courier, monospace;">
            ${phone !== "N/A" ? `<a href="tel:${phone}" style="color: inherit; text-decoration: none;">📞 ${phone}</a>` : '<span style="color: #555;">No phone</span>'}
          </div>
        </td>
        <td style="padding: 1rem; color: #00ff41; font-size: 0.95rem; vertical-align: top; line-height: 1.5; white-space: pre-wrap; font-family: 'Courier New', Courier, monospace;">${message}</td>
      `;
      tbody.appendChild(tr);
    });
  }, (error) => {
    console.error("Error fetching live feed:", error);
    tbody.innerHTML = `<tr><td colspan="4" style="padding: 2rem; text-align: center; color: #ef4444; font-family: 'Courier New', Courier, monospace;">⚠️ Error loading real-time data: ${error.message}</td></tr>`;
  });
});
