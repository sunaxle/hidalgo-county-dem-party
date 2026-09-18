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

async function initDirectory() {
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
              officials = officials.map(item => item.name.toLowerCase() === key ? { ...item, ...fsItem } : item);
            } else {
              officials.push(fsItem);
            }
          });
          
          renderGrid();
        }
      }
    } catch (err) {
      console.warn("Could not fetch Firestore officials directory updates, using built-in verified registry:", err);
    }
  }

  // Filter Buttons
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.getAttribute("data-filter");
      renderGrid();
    });
  });

  // Search Input with Debouncing
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener("input", (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchQuery = e.target.value.toLowerCase().trim();
        renderGrid();
      }, 150);
    });
  }

  function renderGrid() {
    grid.innerHTML = "";

    const filtered = officials.filter(official => {
      // Exclude Colin Allred completely
      if (official.name && (official.name.toLowerCase().includes("allred") || official.name === "Colin Allred")) {
        return false;
      }

      // Filter by Level
      let matchesFilter = true;
      if (currentFilter !== "all") {
        matchesFilter = (official.level && official.level.toLowerCase() === currentFilter.toLowerCase());
      }

      // Search Query Filter
      let matchesSearch = true;
      if (searchQuery) {
        const nameMatch = official.name && official.name.toLowerCase().includes(searchQuery);
        const officeMatch = official.office && official.office.toLowerCase().includes(searchQuery);
        const districtMatch = official.district && official.district.toLowerCase().includes(searchQuery);
        const levelMatch = official.level && official.level.toLowerCase().includes(searchQuery);
        matchesSearch = nameMatch || officeMatch || districtMatch || levelMatch;
      }

      return matchesFilter && matchesSearch;
    });

    // Update Counter
    if (resultsCount) {
      resultsCount.textContent = `Showing ${filtered.length} official${filtered.length === 1 ? '' : 's'}`;
    }

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: #64748b;">
          <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
          <h3 style="font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">No candidates or officials found</h3>
          <p style="font-size: 0.95rem;">Try adjusting your search terms or filter selection.</p>
        </div>
      `;
      return;
    }

    filtered.forEach(official => {
      const card = document.createElement("div");
      card.className = "candidate-card";

      // Status Badge
      let statusClass = "badge-general";
      let statusLabel = "General Election Candidate";
      if (official.status === "incumbent") {
        statusClass = "badge-incumbent";
        statusLabel = "Incumbent";
      } else if (official.status === "won_primary") {
        statusClass = "badge-nominee";
        statusLabel = "Democratic Nominee";
      }

      // Level Badge Styling
      let levelClass = "level-federal";
      if (official.level === "State") levelClass = "level-state";
      if (official.level === "County") levelClass = "level-county";
      if (official.level === "Judicial") levelClass = "level-judicial";
      if (official.level === "Municipal") levelClass = "level-municipal";

      // Links Bar
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
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initDirectory);
} else {
  initDirectory();
}
