import { CANDIDATE_DIRECTORY } from "./directory_data.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  getDocs,
  query
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  projectId: "hcdp-digital-inbox",
  appId: "1:884194084346:web:ee44e3410c73322a631043",
  storageBucket: "hcdp-digital-inbox.firebasestorage.app",
  apiKey: "AIzaSyBMSgg__pJEm6NESKJe6l72UydEWZpdMhw",
  authDomain: "hcdp-digital-inbox.firebaseapp.com",
};

let db = null;
try {
  const app = initializeApp(firebaseConfig);
  db = getFirestore(app);
} catch (e) {
  console.warn("Firebase initialized with offline dataset fallback:", e);
}

document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("directoryGrid");
  const filterBtns = document.querySelectorAll(".filter-btn");
  const searchInput = document.getElementById("candidateSearchInput");
  const resultsCount = document.getElementById("resultsCount");

  if (!grid) return;

  // Initialize with verified master dataset
  let officials = [...CANDIDATE_DIRECTORY];
  let currentFilter = "all";
  let searchQuery = "";

  // Render instantly from master dataset
  renderGrid();

  // Optionally fetch dynamic updates from Firestore if available
  if (db) {
    try {
      const q = query(collection(db, "officials_directory"));
      const snapshot = await getDocs(q);
      
      if (snapshot.docs.length > 0) {
        const firestoreOfficials = snapshot.docs
          .map(doc => ({ id: doc.id, ...doc.data() }))
          .filter(o => o.name && !o.name.toLowerCase().includes("allred") && o.name !== "Colin Allred");
        
        if (firestoreOfficials.length > 0) {
          // Merge with master dataset, giving priority to enriched fields
          const idMap = new Map();
          officials.forEach(item => idMap.set(item.name.toLowerCase(), item));
          
          firestoreOfficials.forEach(fsItem => {
            const key = fsItem.name.toLowerCase();
            if (idMap.has(key)) {
              idMap.set(key, { ...idMap.get(key), ...fsItem });
            } else {
              idMap.set(key, fsItem);
            }
          });
          
          officials = Array.from(idMap.values());
          renderGrid();
        }
      }
    } catch (err) {
      console.info("Using cached static directory dataset (offline / network fast mode).");
    }
  }

  // Filter Buttons Click
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.getAttribute("data-filter") || "all";
      renderGrid();
    });
  });

  // Search Input Listener
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      renderGrid();
    });
  }

  function getFilteredData() {
    return officials.filter(official => {
      // Level & Type filter
      let matchesFilter = true;
      const level = (official.level || "").toLowerCase();
      const type = (official.type || "").toLowerCase();

      if (currentFilter === "federal") {
        matchesFilter = level === "federal";
      } else if (currentFilter === "state") {
        matchesFilter = level === "state";
      } else if (currentFilter === "county") {
        matchesFilter = level === "county";
      } else if (currentFilter === "candidate") {
        matchesFilter = type.includes("candidate") || type.includes("nominee");
      } else if (currentFilter === "incumbent") {
        matchesFilter = type.includes("incumbent") || type.includes("officeholder");
      }

      if (!matchesFilter) return false;

      // Text search filter
      if (!searchQuery) return true;

      const name = (official.name || "").toLowerCase();
      const office = (official.office || official.title || "").toLowerCase();
      const email = (official.email || "").toLowerCase();
      const phone = (official.phone || "").toLowerCase();

      return name.includes(searchQuery) ||
             office.includes(searchQuery) ||
             email.includes(searchQuery) ||
             phone.includes(searchQuery);
    });
  }

  function renderGrid() {
    const data = getFilteredData();
    
    // Sort: Federal (1) -> State (2) -> County (3), then by Name
    const levelOrder = { "Federal": 1, "State": 2, "County": 3 };
    data.sort((a, b) => {
      const levelA = levelOrder[a.level] || 99;
      const levelB = levelOrder[b.level] || 99;
      if (levelA === levelB) {
        return (a.name || "").localeCompare(b.name || "");
      }
      return levelA - levelB;
    });

    // Update Results Counter
    if (resultsCount) {
      resultsCount.textContent = `Showing ${data.length} of ${officials.length} officials & candidates`;
    }

    grid.innerHTML = "";

    if (data.length === 0) {
      grid.innerHTML = `
        <div class="empty-state">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="color: #fff; margin-bottom: 0.5rem;">No candidates or officials found</h3>
          <p style="color: #94a3b8; max-width: 450px; margin: 0 auto;">Try adjusting your search query or switching to another filter category.</p>
        </div>
      `;
      return;
    }

    data.forEach(official => {
      const card = document.createElement("div");
      card.className = "candidate-card";

      // Determine level badge class
      const levelKey = (official.level || "Federal").toLowerCase();
      let levelClass = "badge-federal";
      if (levelKey === "state") levelClass = "badge-state";
      if (levelKey === "county") levelClass = "badge-county";

      // Determine status badge class
      const typeKey = (official.type || "Candidate").toLowerCase();
      let statusClass = "type-candidate";
      let statusLabel = official.type || "2026 Candidate";
      if (typeKey.includes("nominee")) {
        statusClass = "type-nominee";
        statusLabel = "2026 Nominee";
      } else if (typeKey.includes("incumbent") || typeKey.includes("officeholder")) {
        statusClass = "type-incumbent";
        statusLabel = "Elected Incumbent";
      }

      // Build Action links
      let actionLinks = "";
      if (official.website) {
        actionLinks += `<a href="${official.website}" target="_blank" rel="noopener noreferrer">🌐 Website</a>`;
      }
      if (official.email) {
        actionLinks += `<a href="mailto:${official.email}">✉️ ${official.email}</a>`;
      }
      if (official.phone) {
        actionLinks += `<a href="tel:${official.phone.replace(/[^0-9]/g, '')}">📞 ${official.phone}</a>`;
      }
      if (official.twitter) {
        actionLinks += `<a href="${official.twitter}" target="_blank" rel="noopener noreferrer">🐦 Twitter/X</a>`;
      }
      if (official.facebook) {
        actionLinks += `<a href="${official.facebook}" target="_blank" rel="noopener noreferrer">📘 Facebook</a>`;
      }
      if (official.instagram) {
        actionLinks += `<a href="${official.instagram}" target="_blank" rel="noopener noreferrer">📸 Instagram</a>`;
      }

      // Donate Button (ActBlue)
      let donateButton = "";
      if (official.donate_url) {
        donateButton = `
          <a href="${official.donate_url}" target="_blank" rel="noopener noreferrer" class="btn-donate-actblue">
            <span>💙 Donate to Campaign</span> &rarr;
          </a>
        `;
      }

      card.innerHTML = `
        <div class="candidate-photo">
          <img src="${official.photo_url || 'images/facebook_1656248751972_6946810765393131439.webp'}" alt="${official.name}" onerror="this.src='images/facebook_1656248751972_6946810765393131439.webp'">
          <span class="level-badge ${levelClass}">${official.level || 'Federal'}</span>
        </div>
        <div class="candidate-info">
          <span class="status-badge ${statusClass}">${statusLabel}</span>
          <h3 class="candidate-name">${official.name}</h3>
          <p class="candidate-race">${official.office || official.title || ''}</p>
          
          <div class="card-actions">
            ${donateButton}
            <div class="candidate-links">
              ${actionLinks || '<span style="color: #64748b; font-size: 0.8rem;">Contact info coming soon</span>'}
            </div>
          </div>
        </div>
      `;

      grid.appendChild(card);
    });
  }
});
