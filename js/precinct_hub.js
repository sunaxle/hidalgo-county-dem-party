// Embedded Congressional District arrays to eliminate fetch dependencies
const cd15List = [1,2,3,4,5,6,8,13,14,15,16,17,18,19,20,21,22,23,24,25,30,31,32,33,39,40,41,42,43,44,45,46,52,53,54,55,56,57,58,59,60,62,65,68,69,70,71,72,73,74,75,76,77,79,81,84,85,87,90,91,92,96,104,105,106,107,108,109,110,111,112,113,114,116,117,118,119,120,121,122,123,124,126,127,129,130,132,134,137,140,142,143,144,146,147,150,151,152,153,154,155,156,157,158,159,160,162,163,166,167,169,171,172,173,174,175,176,177,178,179,180,181,184,186,189,190,191,192,196,199,200,201,202,206,207,213,214,221,222,223,224,225,226,227,228,229,230,232,234,235,237,238,239,240,242,245,249,250,251,252,253,255,259];
const cd28List = [7,8,9,10,11,12,26,27,28,29,34,35,36,37,38,47,48,49,50,51,61,63,64,65,66,67,78,80,82,83,84,86,88,89,93,94,95,97,98,99,100,101,102,103,115,124,125,128,131,133,134,135,136,138,139,141,145,148,149,150,161,164,165,168,170,182,183,185,187,188,193,194,195,197,198,203,204,205,208,209,210,211,212,215,216,217,218,219,220,231,233,234,236,240,241,243,244,246,247,248,254,256,257,258];

let currentCDFilter = "ALL";
let currentRoleFilter = "ALL";
let currentSearchQuery = "";
let filterTimeout = null;

function initHub() {
  const searchInput = document.getElementById("dir-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearchQuery = e.target.value.toLowerCase().trim().replace(/#/g, "");
      if (filterTimeout) clearTimeout(filterTimeout);
      filterTimeout = setTimeout(() => {
        applyFilters();
      }, 80);
    });
  }

  renderGrid();
}

function renderGrid() {
  if (typeof chairDataList2026 === "undefined") {
    console.warn("chairDataList2026 not loaded yet.");
    return;
  }
  const data = chairDataList2026;
  const chairs = data.filter(
    (d) =>
      d.role.includes("Precinct Chair") ||
      d.role === "Neighborhood Captain" ||
      d.role === "Block Worker",
  );

  // Sort by precinct number
  chairs.sort((a, b) => {
    const pA = parseInt(a.precinct) || 0;
    const pB = parseInt(b.precinct) || 0;
    return pA - pB;
  });

  const grid = document.getElementById("recent-profiles-grid");
  if (!grid) return;

  if (chairs.length === 0) {
    grid.innerHTML = `<p style="color:#94a3b8; text-align:center; grid-column: 1/-1;">No updated profiles found yet.</p>`;
    return;
  }

  const customProfileMap = {
    "84": { url: "alma.html", photo: "alma_butcher.png" },
    "146": { url: "olga.html", photo: "olga_cardoza.png" },
    "35": { url: "liza.html", photo: "" },
    "25": { url: "daniela.html", photo: "daniela_avila.png" },
    "93": { url: "karen.html", photo: "karen_prewitt.png" }
  };

  let htmlBuffer = "";

  chairs.forEach((chair, index) => {
    const isBlockCapt = chair.role === "Neighborhood Captain";
    const isBlockWorker = chair.role === "Block Worker";
    const badgeColor = isBlockWorker
      ? "#f59e0b"
      : isBlockCapt
        ? "#3b82f6"
        : "#10b981";

    const customInfo = customProfileMap[String(chair.precinct)];
    const hasCustomProfile = customInfo && chair.role.includes("Precinct Chair");
    const targetUrl = hasCustomProfile ? customInfo.url : `precinct.html?id=${chair.precinct}`;

    let photoUrl = (customInfo && customInfo.photo && customInfo.photo.length > 0)
      ? customInfo.photo
      : (chair.photo && chair.photo.trim().length > 0
        ? chair.photo
        : "https://ui-avatars.com/api/?name=" +
          encodeURIComponent(chair.name) +
          "&background=1e293b&color=38bdf8&size=256&font-size=0.4");

    const animDelay = (index * 0.04) % 1.2;

    htmlBuffer += `
      <div data-name="${chair.name.replace(/"/g, "").toLowerCase()}" data-pct="${chair.precinct}" data-role="${chair.role}" class="hub-card-hover stagger-fade-in" style="animation-delay: ${animDelay}s; background: rgba(255,255,255,0.05); padding: 0; border-radius: 12px; text-align: center; border: 1px solid ${hasCustomProfile ? "#38bdf8" : "rgba(255,255,255,0.1)"}; overflow: hidden; cursor:pointer; ${hasCustomProfile ? "box-shadow: 0 0 15px rgba(56,189,248,0.25);" : ""}" onclick="window.location.href='${targetUrl}'">
          <div style="height: 180px; width: 100%; overflow: hidden; position: relative; background: #0f172a;">
              <img src="${photoUrl}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease;" class="card-img-zoom" alt="${chair.name}" onerror="this.onerror=null;this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(chair.name)}&background=1e293b&color=38bdf8&size=256';"/>
              <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 50%; background: linear-gradient(to top, rgba(15,23,42,1) 0%, rgba(15,23,42,0) 100%);"></div>
              ${hasCustomProfile ? "<div style="position: absolute; top: 10px; right: 10px; background: rgba(14,165,233,0.9); color: #020617; font-weight: 800; font-size: 0.7rem; padding: 0.25rem 0.6rem; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 8px rgba(0,0,0,0.4);">⭐ Profile Hub</div>" : ""}
          </div>
          <div style="padding: 1.5rem; position: relative;">
              <div style="background: ${badgeColor}22; color: ${badgeColor}; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-top: -2.5rem; margin-bottom: 0.75rem; padding: 0.4rem 0.8rem; border-radius: 999px; display:inline-block; border: 1px solid ${badgeColor}55; backdrop-filter: blur(4px); position: relative; z-index: 2;">
                  ${chair.role}
              </div>
              <strong style="color: #fff; font-size: 1.25rem; display:block; margin-bottom: 0.25rem; position: relative; z-index: 2;">${chair.name}</strong>
              <div style="color: #94a3b8; font-size: 0.95rem; font-weight: 600; position: relative; z-index: 2;">Precinct ${chair.precinct}</div>
              ${cd15List.includes(parseInt(chair.precinct)) && cd28List.includes(parseInt(chair.precinct)) ? "<div style="color: #ea580c; font-size: 0.8rem; font-weight: 700; margin-top: 0.25rem;">⚠️ Split District</div>" : ""}
          </div>
      </div>
    `;
  });

  grid.innerHTML = htmlBuffer;
}

function applyFilters() {
  const cards = document.querySelectorAll(".hub-card-hover");
  let visibleCount = 0;

  cards.forEach((card) => {
    const name = card.getAttribute("data-name") || "";
    const pct = card.getAttribute("data-pct") || "";
    const role = card.getAttribute("data-role") || "";
    const pctNum = parseInt(pct, 10);

    let roleMatch = true;
    if (currentRoleFilter === "CHAIR") {
      roleMatch = role.includes("Precinct Chair");
    } else if (currentRoleFilter === "CAPTAIN") {
      roleMatch = role === "Neighborhood Captain";
    } else if (currentRoleFilter === "BLOCK") {
      roleMatch = role === "Block Worker";
    }

    let cdMatch = true;
    if (currentCDFilter === "15") {
      cdMatch = cd15List.includes(pctNum);
    } else if (currentCDFilter === "28") {
      cdMatch = cd28List.includes(pctNum);
    }

    let textMatch = true;
    if (currentSearchQuery.length > 0) {
      textMatch =
        name.includes(currentSearchQuery) ||
        String(pct).includes(currentSearchQuery);
    }

    if (roleMatch && cdMatch && textMatch) {
      card.style.display = "block";
      card.style.opacity = "1";
      visibleCount++;
    } else {
      card.style.display = "none";
    }
  });

  const grid = document.getElementById("recent-profiles-grid");
  let emptyMsg = document.getElementById("empty-filter-msg");

  if (visibleCount === 0) {
    if (!emptyMsg && grid) {
      emptyMsg = document.createElement("p");
      emptyMsg.id = "empty-filter-msg";
      emptyMsg.style.color = "#94a3b8";
      emptyMsg.style.textAlign = "center";
      emptyMsg.style.gridColumn = "1/-1";
      emptyMsg.style.padding = "2rem";
      emptyMsg.style.fontSize = "1.1rem";
      emptyMsg.innerHTML = "No precincts or names matched your search criteria.";
      grid.appendChild(emptyMsg);
    } else if (emptyMsg) {
      emptyMsg.style.display = "block";
    }
  } else {
    if (emptyMsg) emptyMsg.style.display = "none";
  }
}

window.filterGridByCD = function (districtStr, btnElement) {
  const buttons = document.querySelectorAll(".cd-filter-btn");
  buttons.forEach((b) => {
    b.style.background = "rgba(255,255,255,0.05)";
    b.style.color = "#94a3b8";
    b.style.borderColor = "rgba(255,255,255,0.1)";
    b.style.boxShadow = "none";
    b.classList.remove("active-cd");
  });

  if (btnElement) {
    btnElement.style.background = "var(--accent)";
    btnElement.style.color = "#020617";
    btnElement.style.borderColor = "var(--accent)";
    btnElement.style.boxShadow = "0 0 15px rgba(56,189,248,0.4)";
    btnElement.classList.add("active-cd");
  }

  currentCDFilter = districtStr;
  applyFilters();
};

window.filterGridByRole = function (roleStr, btnElement) {
  const buttons = document.querySelectorAll(".role-filter-btn");
  buttons.forEach((b) => {
    b.style.background = "rgba(255,255,255,0.05)";
    b.style.color = "#94a3b8";
    b.style.borderColor = "rgba(255,255,255,0.1)";
    b.style.boxShadow = "none";
    b.classList.remove("active-role");
  });

  if (btnElement) {
    btnElement.style.background = "var(--accent)";
    btnElement.style.color = "#020617";
    btnElement.style.borderColor = "var(--accent)";
    btnElement.style.boxShadow = "0 0 15px rgba(56,189,248,0.4)";
    btnElement.classList.add("active-role");
  }

  currentRoleFilter = roleStr;
  applyFilters();
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initHub);
} else {
  initHub();
}
