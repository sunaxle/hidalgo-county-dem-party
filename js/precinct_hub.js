document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.getElementById("precinct-search-btn");
  const searchInput = document.getElementById("precinct-search-input");
  const errorMsg = document.getElementById("precinct-search-error");
  
  if (searchBtn) {
    searchBtn.addEventListener("click", () => {
      const val = searchInput.value.trim();
      if (!val || val === "" || isNaN(val)) {
        errorMsg.style.display = "block";
        errorMsg.innerText = "Please enter a valid precinct number.";
        return;
      }
      // Route over to the dynamic single page
      window.location.href = `precinct.html?id=${val}`;
    });
  }

  // Load static array and populate recent chairs initially
  if (typeof chairDataList2026 !== 'undefined') {
    const data = chairDataList2026;
    // Filter for leadership
    const chairs = data.filter(d => d.role === "Precinct Chair" || d.role === "Block Captain");
    
    const grid = document.getElementById("recent-profiles-grid");
    if (grid) {
      if (chairs.length === 0) {
         grid.innerHTML = `<p style="color:#94a3b8; text-align:center; grid-column: 1/-1;">No updated profiles found yet.</p>`;
         return;
      }

      grid.innerHTML = "";
      // Show up to 4 recent profiles realistically
      chairs.slice(0, 4).forEach(chair => {
         const isBlockCapt = chair.role === "Block Captain";
         const badgeColor = isBlockCapt ? "#3b82f6" : "#10b981"; // Blue for Capt, Green for Chair
         
         // Fallback photo
         let photoUrl = chair.photo && chair.photo.trim().length > 0 
           ? chair.photo 
           : "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png";

         const customHtml = `
           <div style="background: rgba(255,255,255,0.05); padding: 0; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; transition: transform 0.2s; cursor:pointer;" onclick="window.location.href='precinct.html?id=${chair.precinct}'" class="hub-card-hover">
             <div style="height: 150px; width: 100%; overflow: hidden;">
               <img src="${photoUrl}" style="width: 100%; height: 100%; object-fit: cover;" alt="Profile Picture"/>
             </div>
             <div style="padding: 1.5rem;">
               <strong style="color: #fff; font-size: 1.25rem; display:block;">${chair.name}</strong>
               <div style="background: ${badgeColor}22; color: ${badgeColor}; font-size: 0.8rem; text-transform: uppercase; margin: 0.5rem auto; padding: 0.3rem 0.6rem; border-radius: 999px; display:inline-block; border: 1px solid ${badgeColor}55;">
                  ${chair.role}
               </div>
               <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 0.5rem;">Precinct ${chair.precinct}</div>
             </div>
           </div>
         `;
         grid.innerHTML += customHtml;
      });
      
      // Inject minor CSS for hover
      const style = document.createElement('style');
      style.innerHTML = `.hub-card-hover:hover { transform: translateY(-5px); border-color: var(--accent) !important; box-shadow: 0 4px 20px rgba(0, 240, 255, 0.2); }`;
      document.head.appendChild(style);
    }
  }
});

// --- Congressional District API Filter Logic ---
let cd15List = [];
let cd28List = [];

// Fetch raw JSON geometry arrays
Promise.all([
    fetch('data/cd15_precincts.json').then(res => res.json()),
    fetch('data/cd28_precincts.json').then(res => res.json())
]).then(data => {
    cd15List = data[0];
    cd28List = data[1];
    console.log(`Loaded CD-15: ${cd15List.length} precincts | CD-28: ${cd28List.length} precincts`);
}).catch(err => console.error("Filter API Error:", err));

// Expose filter function globally so inline HTML button clicks can trigger it
window.filterGridByCD = function(districtStr, btnElement) {
    // 1. Update UI Toggle States
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

    // 2. Iterate Live DOM Nodes to Hide/Show based on binary mapping arrays
    const allPrecinctCards = document.querySelectorAll('.hub-card-hover');
    allPrecinctCards.forEach(card => {
        // The script in `js/chair_data.js` constructs the cards. We extract the precinct number from the text.
        // It writes "<div ...>Precinct X</div>". We need to find that number safely.
        const pctDiv = Array.from(card.querySelectorAll('div')).find(el => el.textContent.includes('Precinct '));
        if (!pctDiv) return;

        const rawText = pctDiv.textContent.replace('Precinct ', '').trim();
        const pctNum = parseInt(rawText, 10);
        
        if (isNaN(pctNum)) return;

        // Reset visibility
        card.style.display = 'block';

        if (districtStr === '15') {
            if (!cd15List.includes(pctNum)) card.style.display = 'none';
        } else if (districtStr === '28') {
            if (!cd28List.includes(pctNum)) card.style.display = 'none';
        }
        // If 'ALL', we leave display as 'block'
    });
};
