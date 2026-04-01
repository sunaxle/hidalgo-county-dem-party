document.addEventListener('DOMContentLoaded', async () => {
    const map = L.map('map').setView([26.3, -98.15], 10);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    const getColor = (d) => {
        return d > 15  ? '#d9381e' : 
               d > 10  ? '#e67300' : 
               d > 5   ? '#e6b800' : 
               d > 2   ? '#80b300' : 
                         '#339933';  
    };

    let isSimulated = false;

    const stylePrecinct = (feature) => {
        let distance = isSimulated ? (feature.properties.simulated_distance || 0) : (feature.properties.distance_to_ev || 0);
        
        let cdColor = 'white';
        let cdDash = '3';
        let cdWeight = 1;
        let cdOp = 0.8;
        
        if (feature.properties.CD === "15") {
            cdColor = '#eab308'; // Gold edge for CD15
            cdDash = '';
            cdWeight = 2;
            cdOp = 1;
        } else if (feature.properties.CD === "28") {
            cdColor = '#a855f7'; // Purple edge for CD28
            cdDash = '';
            cdWeight = 2;
            cdOp = 1;
        }

        return {
            fillColor: getColor(distance),
            weight: cdWeight,
            opacity: cdOp,
            color: cdColor,
            dashArray: cdDash,
            fillOpacity: 0.6
        };
    };

    const highlightFeature = (e) => {
        var layer = e.target;
        layer.setStyle({
            weight: 3,
            color: '#333',
            dashArray: '',
            fillOpacity: 0.8
        });
        layer.bringToFront();
    };

    let geojsonLayer;
    let circleMarkersLayer = L.featureGroup().addTo(map);
    let baselineLayer = L.featureGroup().addTo(map);
    let simulationLayer = L.featureGroup().addTo(map);

    try {
        const [geojsonRes, evLocRes, evTotal2024, evTotal2026, simLocRes] = await Promise.all([
            fetch('data_analysis/hidalgo_analysis_precincts.geojson'),
            fetch('hidalgo-election-map/polling_locations.geojson'),
            fetch('data_analysis/location_turnout_2024.json'),
            fetch('data_analysis/location_turnout_primary.json'),
            fetch('data_analysis/proposed_ev_sites.geojson')
        ]);
        
        const precinctsGeojson = await geojsonRes.json();
        const evLocations = await evLocRes.json();
        const evTotals2024 = await evTotal2024.json();
        const evTotals2026 = await evTotal2026.json();
        const simLocations = await simLocRes.json();

        // 1. Render Precinct Layer
        const renderPrecincts = () => {
            if (geojsonLayer) {
                map.removeLayer(geojsonLayer);
            }
            geojsonLayer = L.geoJson(precinctsGeojson, {
                style: stylePrecinct,
                onEachFeature: (feature, layer) => {
                    const dist = (isSimulated ? feature.properties.simulated_distance : feature.properties.distance_to_ev) || 0;
                    const pct = feature.properties.PCT || feature.properties.PREC || 'Unknown';
                    const site = feature.properties.nearest_ev_site || 'None';
                    const rv = feature.properties.registered_voters || 0;
                    const penalty = isSimulated ? feature.properties.simulated_penalty : feature.properties.collective_mileage_penalty;
                    
                    let tooltipContent = `
                        <div style="font-family: 'Public Sans', sans-serif;">
                            <strong>Precinct ${pct}</strong><br>
                            Registered Voters: ${rv.toLocaleString()}<br>
                            ${isSimulated ? "Distance (w/ Sim): " : "Nearest EV: " + site + "<br>Distance: "} ${dist.toFixed(1)} miles<br>
                            <strong style="color:var(--primary-color);">Aggregated Friction: ${Math.round(penalty || 0).toLocaleString()} mi</strong>
                        </div>
                    `;
                    layer.bindTooltip(tooltipContent);
                    layer.on({
                        mouseover: highlightFeature,
                        mouseout: (e) => geojsonLayer.resetStyle(e.target),
                    });
                }
            }).addTo(map);
        };
        renderPrecincts();

        // 2. Legend setup
        const legendDiv = document.getElementById('map-legend');
        const grades = [0, 2, 5, 10, 15];
        const labels = ['< 2 mi', '2 - 5 mi', '5 - 10 mi', '10 - 15 mi', '> 15 mi'];
        let legendHTML = '';
        for (let i = 0; i < grades.length; i++) {
            legendHTML += `
                <div class="legend-item">
                    <i class="legend-color" style="background:${getColor(grades[i] + 0.1)}"></i>
                    <span>${labels[i]}</span>
                </div>
            `;
        }
        legendDiv.innerHTML = legendHTML;

        // 3. Draw Static Baseline Dotted Circles (2.3 miles = 3701 meters)
        evLocations.features.forEach(site => {
            let coords = site.geometry.coordinates;
            let latlng = [coords[1], coords[0]]; 
            
            L.circle(latlng, {
                radius: 3701,
                color: "#64748b",
                weight: 2,
                dashArray: "4, 8",
                fillColor: "transparent",
                fillOpacity: 0
            }).addTo(baselineLayer);
        });

        // 4. Draw Simulation Layer (hidden initially)
        simLocations.features.forEach(site => {
            let coords = site.geometry.coordinates;
            let latlng = [coords[1], coords[0]]; 

            // The bright green star marker for the site itself
            L.circleMarker(latlng, {
                radius: 8,
                fillColor: "#10b981", // Emerald
                color: "#047857",
                weight: 2,
                opacity: 1,
                fillOpacity: 1
            }).bindTooltip("<strong>" + site.properties.name + "</strong>").addTo(simulationLayer);

            // The exact 2.3-mile baseline reach of the new site
            L.circle(latlng, {
                radius: 3701,
                color: "#10b981",
                weight: 2,
                dashArray: "4, 8",
                fillColor: "rgba(16, 185, 129, 0.1)",
                fillOpacity: 0.1
            }).addTo(simulationLayer);
        });
        map.removeLayer(simulationLayer); // hide by default

        // 5. Dynamic render circles
        const renderCircles = (turnoutDataset, electionLabel) => {
            circleMarkersLayer.clearLayers();
            document.getElementById('turnout-label').innerText = `${electionLabel} Turnout`;
            
            // Calc avg turnout for the simulation projection
            let totalVals = 0;
            let countVals = 0;

            evLocations.features.forEach(site => {
                let locName = site.properties.name;
                let latlng = [site.geometry.coordinates[1], site.geometry.coordinates[0]]; 
                let matchedTurnout = 0;
                for (let [key, val] of Object.entries(turnoutDataset)) {
                    if (locName.toLowerCase().includes(key.toLowerCase().substring(0, 8))) {
                        matchedTurnout = val;
                        totalVals += val;
                        countVals++;
                        break;
                    }
                }

                let displayTurnout = matchedTurnout > 0 ? matchedTurnout : 1000;
                let radiusMeters = Math.sqrt(displayTurnout) * 40;
                if (radiusMeters < 500) radiusMeters = 500;
                if (radiusMeters > 8000) radiusMeters = 8000;

                L.circle(latlng, {
                    radius: radiusMeters,
                    fillColor: "rgba(0, 82, 163, 0.4)",
                    color: "#0052a3",
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.4
                }).bindTooltip(`
                    <div style="text-align: center;">
                        <strong>${locName}</strong><br>
                        ${electionLabel} EV Turnout: <br>
                        <span style="font-size: 1.2rem; font-weight: bold; color: #0052a3;">
                            ${matchedTurnout > 0 ? matchedTurnout.toLocaleString() : 'N/A'}
                        </span>
                    </div>
                `).addTo(circleMarkersLayer);
            });

            // Calculate simulation potential votes
            const avgTurnout = countVals > 0 ? Math.round(totalVals / countVals) : 0;
            document.getElementById('stat-new-votes').innerText = `+${(avgTurnout * 10).toLocaleString()}`;
        };

        let currentActiveDataset = evTotals2024;
        let currentActiveLabel = "2024 General";
        renderCircles(currentActiveDataset, currentActiveLabel);

        // 6. Output the Datatable
        const buildTable = () => {
            let deserts = [];
            precinctsGeojson.features.forEach(f => {
                const pct = f.properties.PCT || f.properties.PREC;
                const dist = isSimulated ? f.properties.simulated_distance : f.properties.distance_to_ev;
                const penalty = isSimulated ? f.properties.simulated_penalty : f.properties.collective_mileage_penalty;
                
                if (dist && pct) {
                    deserts.push({
                        pct: pct,
                        dist: dist,
                        site: f.properties.nearest_ev_site || "Simulation Target",
                        rv: f.properties.registered_voters || 0,
                        penalty: penalty || 0
                    });
                }
            });
            
            // Sort descending by collective mileage penalty
            deserts.sort((a, b) => b.penalty - a.penalty);
            
            const tbody = document.getElementById('desert-table-body');
            tbody.innerHTML = '';
            for (let i = 0; i < Math.min(10, deserts.length); i++) {
                let row = deserts[i];
                let tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${row.pct}</strong></td>
                    <td>${isSimulated ? '<i>Optimum Assigned</i>' : row.site}</td>
                    <td>${row.rv.toLocaleString()}</td>
                    <td class="distance-cell">${row.dist.toFixed(1)} miles</td>
                    <td style="font-weight: 800; color: #d9381e;">${Math.round(row.penalty).toLocaleString()} mi</td>
                `;
                tbody.appendChild(tr);
            }

            // Stats UI block update
            if (deserts.length > 0) {
                let maxDist = [...deserts].sort((a, b) => b.dist - a.dist)[0].dist;
                document.getElementById('stat-max-dist').innerText = maxDist.toFixed(1);
                
                let totalDist = deserts.reduce((sum, current) => sum + current.dist, 0);
                document.getElementById('stat-avg-dist').innerText = (totalDist / deserts.length).toFixed(1);
            }
        };
        buildTable();

        // 7. UI Toggles
        const t2024 = document.getElementById('toggle-2024');
        const t2026 = document.getElementById('toggle-2026');
        const tSim = document.getElementById('toggle-sim');
        const simStats = document.getElementById('sim-stats');

        t2024.addEventListener('click', () => {
            t2024.style.background = '#0052a3';
            t2024.style.color = 'white';
            t2026.style.background = 'transparent';
            t2026.style.color = '#1e293b';
            currentActiveDataset = evTotals2024;
            currentActiveLabel = "2024 General";
            renderCircles(currentActiveDataset, currentActiveLabel);
        });

        t2026.addEventListener('click', () => {
            t2026.style.background = '#0052a3';
            t2026.style.color = 'white';
            t2024.style.background = 'transparent';
            t2024.style.color = '#1e293b';
            currentActiveDataset = evTotals2026;
            currentActiveLabel = "2026 Primary";
            renderCircles(currentActiveDataset, currentActiveLabel);
        });

        tSim.addEventListener('click', () => {
            isSimulated = !isSimulated;
            if (isSimulated) {
                tSim.style.background = 'transparent';
                tSim.style.color = '#10b981';
                tSim.style.border = '2px solid #10b981';
                tSim.innerText = '↺ Reset Baseline';
                map.addLayer(simulationLayer);
                simStats.style.display = 'block';
            } else {
                tSim.style.background = '#10b981';
                tSim.style.color = 'white';
                tSim.style.border = 'none';
                tSim.innerText = '💡 Simulate 10 Sites';
                map.removeLayer(simulationLayer);
                simStats.style.display = 'none';
            }
            renderPrecincts();
            buildTable();
        });

    } catch (error) {
        console.error("Error loading map assets:", error);
    }
});
