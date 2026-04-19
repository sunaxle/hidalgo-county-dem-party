// Global State
let cd15List = [];
let cd28List = [];
let currentCDFilter = 'ALL';
let currentSearchQuery = '';
let filterTimeout = null;

// Load Geo JSON arrays
Promise.all([
    fetch('data/cd15_precincts.json').then(res => res.json()),
    fetch('data/cd28_precincts.json').then(res => res.json())
]).then(data => {
    cd15List = data[0];
    cd28List = data[1];
    console.log(`Loaded CD-15: ${cd15List.length} precincts | CD-28: ${cd28List.length} precincts`);
    // Re-filter just in case data loads after render
    applyFilters();
}).catch(err => console.error("Filter API Error:", err));

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("dir-search-input");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            // Strip out pound signs folks might use for precincts (e.g. "#14")
            currentSearchQuery = e.target.value.toLowerCase().trim().replace(/#/g, '');
            
            // Debounce for smoother rendering
            if (filterTimeout) clearTimeout(filterTimeout);
            filterTimeout = setTimeout(() => {
                applyFilters();
            }, 100);
        });
    }

    renderGrid();
});

function renderGrid() {
    if (typeof chairDataList2026 === 'undefined') return;
    const data = chairDataList2026;
    const chairs = data.filter(d => d.role.includes("Precinct Chair") || d.role === "Block Captain");
    
    // Sort by precinct number to keep it organized
    chairs.sort((a,b) => {
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

    grid.innerHTML = "";
    
    chairs.forEach((chair, index) => {
        const isBlockCapt = chair.role === "Block Captain";
        const badgeColor = isBlockCapt ? "#3b82f6" : "#10b981"; // Blue for Capt, Green for Chair
        
        let photoUrl = chair.photo && chair.photo.trim().length > 0 
           ? chair.photo 
           : "https://ui-avatars.com/api/?name=" + encodeURIComponent(chair.name) + "&background=1e293b&color=38bdf8&size=256&font-size=0.4";

        // Add stagger property via inline style for animation
        const animDelay = (index * 0.05) % 1.5; // Cap at 1.5s for stagger loop
        
        const cardHtml = `
            <div data-name="${chair.name.replace(/"/g, '').toLowerCase()}" data-pct="${chair.precinct}" class="hub-card-hover stagger-fade-in" style="animation-delay: ${animDelay}s; background: rgba(255,255,255,0.05); padding: 0; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; cursor:pointer;" onclick="window.location.href='precinct.html?id=${chair.precinct}'">
                <div style="height: 180px; width: 100%; overflow: hidden; position: relative;">
                    <img src="${photoUrl}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease;" class="card-img-zoom" alt="Profile Picture"/>
                    <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 50%; background: linear-gradient(to top, rgba(15,23,42,1) 0%, rgba(15,23,42,0) 100%);"></div>
                </div>
                <div style="padding: 1.5rem; position: relative;">
                    <div style="background: ${badgeColor}22; color: ${badgeColor}; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-top: -2.5rem; margin-bottom: 0.75rem; padding: 0.4rem 0.8rem; border-radius: 999px; display:inline-block; border: 1px solid ${badgeColor}55; backdrop-filter: blur(4px); position: relative; z-index: 2;">
                        ${chair.role}
                    </div>
                    <strong style="color: #fff; font-size: 1.25rem; display:block; margin-bottom: 0.25rem; position: relative; z-index: 2;">${chair.name}</strong>
                    <div style="color: #94a3b8; font-size: 0.95rem; font-weight: 600; position: relative; z-index: 2;">Precinct ${chair.precinct}</div>
                    ${(cd15List.includes(parseInt(chair.precinct)) && cd28List.includes(parseInt(chair.precinct))) ? '<div style="color: #ea580c; font-size: 0.8rem; font-weight: 700; margin-top: 0.25rem;">⚠️ Split District</div>' : ''}
                </div>
            </div>
        `;
        grid.innerHTML += cardHtml;
    });
}

function applyFilters() {
    const cards = document.querySelectorAll('.hub-card-hover');
    let visibleCount = 0;

    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const pct = card.getAttribute('data-pct');
        const pctNum = parseInt(pct, 10);
        
        // 1. Check CD Filter
        let cdMatch = true;
        if (currentCDFilter === '15') {
            // Note: cd15List contains numbers matching pctNum
            cdMatch = cd15List.includes(pctNum);
        } else if (currentCDFilter === '28') {
            cdMatch = cd28List.includes(pctNum);
        }

        // 2. Check Text Search Filter
        let textMatch = true;
        if (currentSearchQuery.length > 0) {
            textMatch = name.includes(currentSearchQuery) || String(pct).includes(currentSearchQuery);
        }

        if (cdMatch && textMatch) {
            card.style.display = 'block';
            card.style.opacity = '1';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    // Handle Empty State
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

// Global hook for the HTML buttons
window.filterGridByCD = function(districtStr, btnElement) {
    const buttons = document.querySelectorAll('.cd-filter-btn');
    buttons.forEach(b => {
        b.style.background = 'rgba(255,255,255,0.05)';
        b.style.color = '#94a3b8';
        b.style.borderColor = 'rgba(255,255,255,0.1)';
        b.style.boxShadow = 'none';
        b.classList.remove('active-cd');
    });

    if (btnElement) {
        btnElement.style.background = 'var(--accent)';
        btnElement.style.color = '#020617';
        btnElement.style.borderColor = 'var(--accent)';
        btnElement.style.boxShadow = '0 0 15px rgba(56,189,248,0.4)';
        btnElement.classList.add('active-cd');
    }

    currentCDFilter = districtStr;
    applyFilters();
};
