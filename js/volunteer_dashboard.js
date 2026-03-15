/**
 * Volunteer Dashboard & Hall of Fame Engine
 * Calculates real baseline stats from `chair_data.js` and injects 
 * mock top-performer metrics for Block Walkers, Phone Bankers, and the Spanish Action Team.
 */

document.addEventListener("DOMContentLoaded", () => {
    
    // ==========================================
    // 1. TIER 1 & 2: Executive Real Data Extraction
    // ==========================================
    if (typeof chairDataList !== 'undefined') {
        const uniquePrecincts = new Set();
        let blockCaptainCount = 0;

        chairDataList.forEach(person => {
            if (person.role.toLowerCase().includes("chair")) {
                uniquePrecincts.add(person.precinct);
            } else if (person.role.toLowerCase().includes("captain")) {
                blockCaptainCount++;
            }
        });

        document.getElementById('stat-precinct-chairs').innerText = uniquePrecincts.size;
        document.getElementById('stat-block-captains').innerText = blockCaptainCount;
    }

    // ==========================================
    // 2. MOCK DATA RANGES (Gamification Tiers)
    // ==========================================
    
    const mockBlockWalkers = [
        { name: "Maria Rodriguez", metric: "1,240 Doors", phone: "Active" },
        { name: "David Martinez", metric: "985 Doors", phone: "Active" },
        { name: "Sarah Jenkins", metric: "812 Doors", phone: "Active" },
        { name: "Carlos Garza", metric: "750 Doors", phone: "Active" },
        { name: "Elena Ochoa", metric: "620 Doors", phone: "Active" }
    ];

    const mockPhoneBankers = [
        { name: "John Torres", metric: "3,400 Calls", phone: "Active" },
        { name: "Linda Perez", metric: "2,950 Calls", phone: "Active" },
        { name: "Michael Chang", metric: "2,100 Calls", phone: "Active" },
        { name: "Ana Silva", metric: "1,850 Calls", phone: "Active" },
        { name: "Robert Gonzales", metric: "1,400 Calls", phone: "Active" }
    ];

    const mockLetterWriters = [
        { name: "Betty White", metric: "500 Letters", phone: "Active" },
        { name: "George Ramos", metric: "450 Letters", phone: "Active" },
        { name: "Clara Diaz", metric: "300 Letters", phone: "Active" }
    ];

    const mockSpanishTeam = [
        "Javier Ruiz", "Sofia Vargas", "Mateo Castillo", "Valentina Rios",
        "Diego Herrera", "Camila Flores", "Luis Morales", "Isabella Guzman",
        "Santiago Reyes", "Lucia Fernandez"
    ];

    // ==========================================
    // 3. UI INJECTION FUNCTIONS
    // ==========================================

    function renderHallOfFame(containerId, data) {
        const container = document.getElementById(containerId);
        if (!container) return;

        data.forEach((volunteer, index) => {
            const rank = index + 1;
            const topClass = rank <= 3 ? "hof-top-3" : "";
            
            const card = document.createElement('div');
            card.className = `hof-card ${topClass}`;
            card.innerHTML = `
                <div class="hof-rank">#${rank}</div>
                <div class="hof-info">
                    <h4>${volunteer.name}</h4>
                    <p>🏆 ${volunteer.metric}</p>
                </div>
            `;
            container.appendChild(card);
        });
    }

    function renderSpanishTeam() {
        const container = document.getElementById('spanish-team-grid');
        if (!container) return;

        mockSpanishTeam.forEach(name => {
            const initial = name.charAt(0);
            const card = document.createElement('div');
            card.className = 'translator-card';
            card.innerHTML = `
                <div class="translator-avatar">${initial}</div>
                <div class="translator-name" style="color: #fff; font-weight: 500;">${name}</div>
            `;
            container.appendChild(card);
        });
    }

    // Execute Renders
    renderHallOfFame("block-walkers-grid", mockBlockWalkers);
    renderHallOfFame("phone-bankers-grid", mockPhoneBankers);
    renderHallOfFame("letter-writers-grid", mockLetterWriters);
    renderSpanishTeam();

});
