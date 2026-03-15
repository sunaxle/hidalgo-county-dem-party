/**
 * Precinct Completion Engine
 * Reads the chairDataList from chair_data.js, computes missing vacancies out of the 268 total target,
 * models them into the 4 geographic commissioner precincts, and updates the DOM dashboards.
 */

document.addEventListener("DOMContentLoaded", () => {
    
    const TOTAL_PRECINCTS = 268; // Based on Hidalgo County's active voting layout

    // Step 1: Extract all unique filled precinct chairs & captains
    // parse int safely just in case format has trailing chars
    const filledStrings = chairDataList
                            .map(c => parseInt(c.precinct))
                            .filter(val => !isNaN(val));

    // Remove duplicates (since both a Chair and Block Captain can occupy the same precinct)
    const uniqueFilled = [...new Set(filledStrings)];
    
    const countFilled = uniqueFilled.length;
    const countVacant = TOTAL_PRECINCTS - countFilled;
    const percentCompletion = Math.round((countFilled / TOTAL_PRECINCTS) * 100);

    // Step 2: Inject Top Level Metrics
    document.getElementById('val-filled').innerText = countFilled;
    document.getElementById('val-vacant').innerText = countVacant;
    document.getElementById('val-percent').innerText = `${percentCompletion}%`;

    // Step 3: Compute the logical gap array (Which specific numbers are missing?)
    const vacantList = [];
    for (let i = 1; i <= TOTAL_PRECINCTS; i++) {
        if (!uniqueFilled.includes(i)) {
            vacantList.push(i);
        }
    }

    // Step 4: Map Vacancies to Regional Commissioner Precincts
    // Mock algorithm since we don't have the strict County-Clerk mapping dictionary
    // Dividing sequentially 1 -> 67, 68 -> 134, etc.
    const area1_gap = vacantList.filter(p => p <= 67);
    const area2_gap = vacantList.filter(p => p > 67 && p <= 134);
    const area3_gap = vacantList.filter(p => p > 134 && p <= 201);
    const area4_gap = vacantList.filter(p => p > 201);

    // Step 5: Render chips into DOM
    renderChips("area1", area1_gap);
    renderChips("area2", area2_gap);
    renderChips("area3", area3_gap);
    renderChips("area4", area4_gap);

});

/**
 * Helper to generate HTML chips and update UI badges
 */
function renderChips(areaBaseID, dataArray) {
    const badgeEl = document.getElementById(`badge-${areaBaseID}`);
    const chipsEl = document.getElementById(`chips-${areaBaseID}`);

    // Update the red badge count
    badgeEl.innerText = `${dataArray.length} Vacant`;

    // Empty previous
    chipsEl.innerHTML = "";
    
    // Inject spans
    dataArray.forEach(p_num => {
        const span = document.createElement("span");
        span.className = "chip";
        span.innerText = `Pct. ${p_num}`;
        chipsEl.appendChild(span);
    });
}
