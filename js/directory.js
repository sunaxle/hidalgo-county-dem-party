import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  getDocs,
  query,
  orderBy
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  projectId: "hcdp-digital-inbox",
  appId: "1:884194084346:web:ee44e3410c73322a631043",
  storageBucket: "hcdp-digital-inbox.firebasestorage.app",
  apiKey: "AIzaSyBMSgg__pJEm6NESKJe6l72UydEWZpdMhw",
  authDomain: "hcdp-digital-inbox.firebaseapp.com",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("directoryGrid");
  const filterBtns = document.querySelectorAll(".filter-btn");

  if (!grid) return;

  let officials = [];

  // Fetch data
  try {
    const q = query(collection(db, "officials_directory"), orderBy("level", "asc"), orderBy("name", "asc"));
    const snapshot = await getDocs(q);
    
    officials = snapshot.docs.map(doc => doc.data());
    renderGrid(officials);
  } catch (err) {
    console.error("Error loading officials:", err);
    grid.innerHTML = "<p style='color: white; grid-column: 1/-1; text-align: center;'>Failed to load directory. Please refresh.</p>";
  }

  // Filter logic
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      const filter = btn.getAttribute("data-filter");
      let filtered = officials;
      
      if (filter === "candidate") {
        filtered = officials.filter(o => o.type.toLowerCase().includes("candidate"));
      } else if (filter === "incumbent") {
        filtered = officials.filter(o => o.type.toLowerCase().includes("incumbent") || o.type.toLowerCase().includes("officeholder"));
      } else if (filter === "federal") {
        filtered = officials.filter(o => o.level.toLowerCase() === "federal");
      } else if (filter === "state") {
        filtered = officials.filter(o => o.level.toLowerCase() === "state");
      } else if (filter === "county") {
        filtered = officials.filter(o => o.level.toLowerCase() === "county");
      }
      
      renderGrid(filtered);
    });
  });

  function renderGrid(data) {
    grid.innerHTML = "";
    if (data.length === 0) {
      grid.innerHTML = "<p style='color: var(--text-muted); grid-column: 1/-1; text-align: center;'>No officials found for this filter.</p>";
      return;
    }

    data.forEach(official => {
      const card = document.createElement("div");
      card.className = "candidate-card";
      
      let badgeClass = "badge-dem";
      let badgeText = "Democrat";
      // Fallbacks in case someone is republican or non-partisan
      if (official.party === "Republican") { badgeClass = "badge-rep"; badgeText = "Republican"; }
      
      let socialLinks = "";
      if (official.website) socialLinks += `<a href="${official.website}" target="_blank">🌐 Website</a>`;
      if (official.twitter) socialLinks += `<a href="${official.twitter}" target="_blank">🐦 Twitter</a>`;
      if (official.facebook) socialLinks += `<a href="${official.facebook}" target="_blank">📘 Facebook</a>`;
      if (official.instagram) socialLinks += `<a href="${official.instagram}" target="_blank">📸 Instagram</a>`;
      
      // Contact fallback
      if (official.phone) socialLinks += `<a href="tel:${official.phone}">📞 Call</a>`;
      if (official.email) socialLinks += `<a href="mailto:${official.email}">✉️ Email</a>`;

      card.innerHTML = `
        <div class="candidate-photo">
          <img src="${official.photo_url || 'images/default_avatar.png'}" alt="${official.name}" onerror="this.src='images/facebook_1656248751972_6946810765393131439.webp'">
          <span class="level-badge">${official.level}</span>
        </div>
        <div class="candidate-info">
          <span class="party-badge ${badgeClass}">${badgeText} | ${official.type}</span>
          <h3 class="candidate-name">${official.name}</h3>
          <p class="candidate-race">${official.title}</p>
          <div class="candidate-links">
            ${socialLinks}
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  }
});
