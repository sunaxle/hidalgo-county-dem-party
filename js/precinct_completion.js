/**
 * Pathway to Precinct Completion - Dashboard Logic
 * Calculates the exact number of vacant seats and maps them organically
 * to their respective County Commissioner Precincts using the master geographic crosswalk.
 */

document.addEventListener("DOMContentLoaded", () => {
    
    // We expect window.chairDataList (from chair_data.js) and window.precinctDistricts (from precinct_mapping_data.js) to exist.
    if (typeof chairDataList === 'undefined' || typeof precinctDistricts === 'undefined') {
        console.error("Required data arrays (chairDataList or precinctDistricts) are not loaded.");
        return;
    }

    // 1. Calculate Active Precinct Chairs
    const uniqueFilledPrecincts = new Set();
    
    // We only care about Precinct Chairs for this specific Gap Tracker (ignore Block Captains)
    chairDataList.forEach(person => {
        if (person.role.toLowerCase() === "precinct chair") {
            // Force strict integer casting to strip padding (e.g., "002" -> 2)
            const cleanPct = parseInt(person.precinct, 10);
            if (!isNaN(cleanPct)) {
                uniqueFilledPrecincts.add(cleanPct);
            }
        }
    });

    const filledCount = uniqueFilledPrecincts.size;

    // 2. Identify Vacant Precincts via the Geographic Crosswalk
    const vacantPrecincts = [];
    const totalPrecinctsCount = precinctDistricts.length; // Now perfectly accurate to the 259 map
    
    precinctDistricts.forEach(geo => {
        // The crosswalk keys are padded strings (e.g. "0001", "0054"). 
        // We cast them to Integers to match the chair_data.js format
        const pctNum = parseInt(geo.PRECINCT, 10);
        
        if (!uniqueFilledPrecincts.has(pctNum) && !isNaN(pctNum)) {
            // Push the full geography object so we know where to sort it later
            vacantPrecincts.push({
                precinct: pctNum,
                commissioner: geo.CC,
                house: geo.HD,
                senate: geo.SD,
                city: geo.CITY || "Rural"
            });
        }
    });

    const vacantCount = vacantPrecincts.length;
    
    // 3. Update the Top Dashboard Headers
    const targetElement = document.getElementById('val-total');
    const filledElement = document.getElementById('val-filled');
    const vacantElement = document.getElementById('val-vacant');
    const percentElement = document.getElementById('val-percent');

    if (targetElement) targetElement.innerText = totalPrecinctsCount;
    if (filledElement) filledElement.innerText = filledCount;
    if (vacantElement) vacantElement.innerText = vacantCount;
    
    if (percentElement) {
        const percent = Math.round((filledCount / totalPrecinctsCount) * 100);
        percentElement.innerText = `${percent}%`;
    }
    
    // Calculate the 'Adopt 5' & 'Even Spread' Strategy
    const countyCandidates = 3; // DA, Treasurer, Sheriff
    const countyQuota = countyCandidates * 5;
    document.getElementById('val-adopted-total').innerText = countyQuota;
    
    // The Remaining Drop
    const remainingLocalOfficials = 20; // 4 CC, 5 State Repts, 2 Senators, 9 JPs
    const remainingGap = Math.max(0, vacantCount - countyQuota);
    const evenSpreadQuota = Math.ceil(remainingGap / remainingLocalOfficials);
    document.getElementById('val-even-spread').innerText = evenSpreadQuota;

    // 4. Map Vacancies Automatically to Commissioner, House, and Senate Precincts
    const commissionerBuckets = { "1": [], "2": [], "3": [], "4": [] };
    const houseBuckets = { "035": [], "036": [], "039": [], "040": [], "041": [] };
    const senateBuckets = { "020": [], "027": [] };

    // Define Mock City Bins for the Municipal Tracker
    const cityBuckets = { "mcallen": [], "edinburg": [], "mission": [], "psja": [], "midvalley": [], "rural": [] };

    vacantPrecincts.forEach(gap => {
        const cc = gap.commissioner;
        const hd = gap.house;
        const sd = gap.senate;
        
        if (commissionerBuckets[cc] !== undefined) commissionerBuckets[cc].push(gap.precinct);
        if (houseBuckets[hd] !== undefined) houseBuckets[hd].push(gap.precinct);
        if (senateBuckets[sd] !== undefined) senateBuckets[sd].push(gap.precinct);
        
        // Distribute to real municipal buckets based on geographic data
        const cityName = gap.city.toLowerCase();
        
        if (cityName === "mcallen") {
            cityBuckets["mcallen"].push(gap.precinct);
        } else if (cityName === "edinburg") {
            cityBuckets["edinburg"].push(gap.precinct);
        } else if (["mission", "palmview", "palmhurst", "penitas", "la joya", "sullivan city"].includes(cityName)) {
            cityBuckets["mission"].push(gap.precinct);
        } else if (["pharr", "san juan", "alamo"].includes(cityName)) {
            cityBuckets["psja"].push(gap.precinct);
        } else if (["weslaco", "mercedes", "donna", "edcouch", "elsa", "la villa"].includes(cityName)) {
            cityBuckets["midvalley"].push(gap.precinct);
        } else {
            cityBuckets["rural"].push(gap.precinct);
        }
    });

    // 5. Render the UI Grids Dynamically
    const renderBucket = (bucketId, dataArray, titleId) => {
        const container = document.getElementById(bucketId);
        const titleBadge = document.getElementById(titleId);
        
        if (!container || !titleBadge) return;
        
        // Sort numerically
        dataArray.sort((a, b) => a - b);
        
        titleBadge.innerText = `${dataArray.length} Vacant`;
        
        // Generate the HTML chips
        let htmlContent = '';
        dataArray.forEach(pct => {
            htmlContent += `<div class="chip">Pct ${pct}</div>`;
        });
        
        container.innerHTML = htmlContent;
    };

    renderBucket('chips-area1', commissionerBuckets["1"], 'badge-area1');
    renderBucket('chips-area2', commissionerBuckets["2"], 'badge-area2');
    renderBucket('chips-area3', commissionerBuckets["3"], 'badge-area3');
    renderBucket('chips-area4', commissionerBuckets["4"], 'badge-area4');
    
    // House Render
    renderBucket('chips-hd35', houseBuckets["035"], 'badge-hd35');
    renderBucket('chips-hd36', houseBuckets["036"], 'badge-hd36');
    renderBucket('chips-hd39', houseBuckets["039"], 'badge-hd39');
    renderBucket('chips-hd40', houseBuckets["040"], 'badge-hd40');
    renderBucket('chips-hd41', houseBuckets["041"], 'badge-hd41');
    
    // Senate Render
    renderBucket('chips-sd20', senateBuckets["020"], 'badge-sd20');
    renderBucket('chips-sd27', senateBuckets["027"], 'badge-sd27');
    
    // City Render
    renderBucket('chips-city-mcallen', cityBuckets["mcallen"], 'badge-city-mcallen');
    renderBucket('chips-city-edinburg', cityBuckets["edinburg"], 'badge-city-edinburg');
    renderBucket('chips-city-mission', cityBuckets["mission"], 'badge-city-mission');
    renderBucket('chips-city-psja', cityBuckets["psja"], 'badge-city-psja');
    renderBucket('chips-city-midvalley', cityBuckets["midvalley"], 'badge-city-midvalley');
    renderBucket('chips-city-rural', cityBuckets["rural"], 'badge-city-rural');

    // 6. Draw the Interactive D3 Geographic Map
    const containerEl = document.querySelector('.map-container');
    const width = containerEl ? containerEl.clientWidth : 800;
    const height = 600;
    const svg = d3.select("#tx-map").attr("viewBox", [0, 0, width, height]);
    
    // Center Hidalgo map accurately inside SVG
    const projection = d3.geoMercator()
        .center([-98.15, 26.3])
        .scale(35000)
        .translate([width / 2, height / 2]);
        
    const pathGenerator = d3.geoPath().projection(projection);

    try {
        const geojson = hidalgoPrecinctsData;
        svg.selectAll("path")
            .data(geojson.features)
            .enter()
            .append("path")
            // Map JSON properties id directly to D3 SVG #path-1
            .attr("id", d => `path-${parseInt(d.properties.PREC, 10)}`)
            .attr("class", "precinct-path")
            .attr("d", pathGenerator);
    } catch (error) {
        console.error("Failed to load map geographic boundaries.", error);
    }

    // 7. Interactive Accordion Toggles + Visual Highlighting
    const headers = document.querySelectorAll('.card-header');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const targetId = header.getAttribute('data-target');
            if (!targetId) return;
            
            const listEl = document.getElementById(targetId);
            const isActive = listEl.classList.contains('active');
            
            // Wipe all sections and map styles clean
            document.querySelectorAll('.vacancy-list').forEach(s => s.classList.remove('active'));
            d3.selectAll('.precinct-path').classed('active-vacancy', false);
            
            // If opening a section, colorize the corresponding SVG boundaries physically
            if (!isActive) {
                listEl.classList.add('active');
                
                // Fetch the chip lists to highlight active vacancy array on map
                const chips = listEl.querySelectorAll('.chip');
                chips.forEach(chip => {
                    const pctText = chip.innerText.replace('Pct ', '');
                    const pctNum = parseInt(pctText, 10);
                    d3.select(`#path-${pctNum}`).classed('active-vacancy', true);
                });
            }
        });
    });

});
