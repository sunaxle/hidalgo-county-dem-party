document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------
    // 1. Initial Map Setup (Similar to map_chairs.js)
    // -------------------------------------------------------------
    
    // Inject Custom Styles for Map Labels Let them look like just text.
    const style = document.createElement('style');
    style.innerHTML = `
        .precinct-label {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            font-weight: bold;
            font-size: 11px;
            color: #0f172a;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.9), -1px -1px 2px rgba(255,255,255,0.9), 1px -1px 2px rgba(255,255,255,0.9), -1px 1px 2px rgba(255,255,255,0.9);
        }
    `;
    document.head.appendChild(style);

    let chairData = typeof chairDataList !== 'undefined' ? chairDataList : [];
    let perfData = typeof performanceData !== 'undefined' ? performanceData : [];

    const map = L.map('map').setView([26.3, -98.2], 9);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    let currentFilter = 'all'; // 'all', 'filled', 'vacant'

    function getPrecinctStatus(pct) {
        let cleanPct = pct ? parseInt(pct, 10).toString() : '';
        if (cleanPct === 'NaN') cleanPct = pct;
        
        let officials = chairData.filter(c => c.precinct === cleanPct);
        return officials.length > 0 ? 'filled' : 'vacant';
    }

    function styleFeature(feature) {
        let pct = feature.properties.PREC || feature.properties.ID;
        if(!pct && feature.properties.tooltip) {
            let match = feature.properties.tooltip.match(/Precinct\s*(\d+)/i);
            if(match) pct = match[1];
        }

        let status = getPrecinctStatus(pct);
        let style = { fillColor: '#3b82f6', color: '#1d4ed8', weight: 1, fillOpacity: 0.2 };

        if (currentFilter === 'filled') {
            if (status === 'filled') {
                style.fillColor = '#10b981';
                style.fillOpacity = 0.6;
                style.color = '#059669';
                style.weight = 2;
            } else {
                style.fillOpacity = 0.1;
                style.color = '#cbd5e1';
                style.fillColor = '#94a3b8';
            }
        } else if (currentFilter === 'vacant') {
            if (status === 'vacant') {
                style.fillColor = '#ef4444';
                style.fillOpacity = 0.6;
                style.color = '#b91c1c';
                style.weight = 2;
            } else {
                style.fillOpacity = 0.1;
                style.color = '#cbd5e1';
                style.fillColor = '#94a3b8';
            }
        }

        return style;
    }

    function onEachFeature(feature, layer) {
        let pct = feature.properties.PREC || feature.properties.ID;
        if(!pct && feature.properties.tooltip) {
            let match = feature.properties.tooltip.match(/Precinct\s*(\d+)/i);
            if(match) pct = match[1];
        }

        let cleanPct = pct ? parseInt(pct, 10).toString() : '';
        if (cleanPct === 'NaN') cleanPct = pct;

        let status = getPrecinctStatus(pct);
        let pd = perfData.find(p => p.precinct === cleanPct);
        
        let popupContent = `<div style="min-width: 200px;">
            <h3 style="margin-top:0; color:#0f172a; border-bottom: 2px solid ${status === 'filled' ? '#10b981' : '#ef4444'}; padding-bottom: 5px;">
                Precinct ${cleanPct || 'Unknown'} <span style="font-size: 0.7em; float:right; padding: 2px 5px; border-radius: 4px; background: ${status === 'filled' ? '#d1fae5' : '#fee2e2'}; color: ${status === 'filled' ? '#065f46' : '#991b1b'};">${status.toUpperCase()}</span>
            </h3>`;
            
        if(pd) {
            popupContent += `
                <div style="font-size: 0.9em; color: #334155; margin-bottom: 8px;">
                    <strong>Reg Voters:</strong> ${pd.registered_voters.toLocaleString()}<br>
                    <strong>Past Primary Target:</strong> ${pd.past_primary.toLocaleString()}<br>
                    <strong style="color: #0284c7;">Proj. Target:</strong> ${pd.target_votes.toLocaleString()}
                </div>
            `;
        }

        popupContent += `<a href="precinct_chairs.html" style="display: block; text-align: center; margin-top: 10px; padding: 5px 10px; background: #3b82f6; color: white; border-radius: 4px; text-decoration: none; font-size: 0.85em;">View Directory</a></div>`;

        layer.bindPopup(popupContent);
        layer.on({
            mouseover: (e) => {
                let l = e.target;
                l.setStyle({ weight: 3, color: '#22d3ee', fillOpacity: 0.7 });
                l.bringToFront();
            },
            mouseout: (e) => { geojsonLayer.resetStyle(e.target); }
        });
    }

    let geojsonLayer = L.geoJSON(hidalgoPrecinctsData, { 
        style: styleFeature, 
        onEachFeature: onEachFeature 
    }).addTo(map);

    map.fitBounds(geojsonLayer.getBounds());

    function updateLabels() {
        geojsonLayer.eachLayer(function(layer) {
            let pct = layer.feature.properties.PREC || layer.feature.properties.ID;
            if(!pct && layer.feature.properties.tooltip) {
                let match = layer.feature.properties.tooltip.match(/Precinct\s*(\d+)/i);
                if(match) pct = match[1];
            }
            let cleanPct = pct ? parseInt(pct, 10).toString() : '';
            if (cleanPct === 'NaN') cleanPct = pct;
            if (!cleanPct || cleanPct === 'Unknown') return;

            let status = getPrecinctStatus(pct);
            let showLabel = (currentFilter === 'all') || 
                            (currentFilter === 'filled' && status === 'filled') || 
                            (currentFilter === 'vacant' && status === 'vacant');

            if (showLabel) {
                if (!layer.getTooltip()) {
                    layer.bindTooltip(cleanPct, { permanent: true, direction: 'center', className: 'precinct-label', interactive: false });
                }
            } else {
                if (layer.getTooltip()) layer.unbindTooltip();
            }
        });
    }


    // -------------------------------------------------------------
    // 2. Chart.js Setup and Data Aggregation
    // -------------------------------------------------------------
    
    // Configuration
    const COUNTY_GOAL = 150000;
    
    // Chart References
    let voterChart;
    let goalChart;
    
    Chart.defaults.color = 'rgba(255, 255, 255, 0.7)';
    Chart.defaults.font.family = "'Inter', sans-serif";

    function aggregateData(filter) {
        let totalRegistered = 0;
        let totalPastPrimary = 0;
        let totalTarget = 0;
        
        perfData.forEach(pd => {
            let status = getPrecinctStatus(pd.precinct);
            
            if (filter === 'all' || 
               (filter === 'filled' && status === 'filled') || 
               (filter === 'vacant' && status === 'vacant')) {
                
                totalRegistered += pd.registered_voters;
                totalPastPrimary += pd.past_primary;
                totalTarget += pd.target_votes;
            }
        });
        
        return { totalRegistered, totalPastPrimary, totalTarget };
    }

    function initCharts() {
        const stats = aggregateData('all');
        
        // 1. Bar Chart: Voters vs Past Primary
        const ctxVoter = document.getElementById('voterChart').getContext('2d');
        voterChart = new Chart(ctxVoter, {
            type: 'bar',
            data: {
                labels: ['Registered Voters', 'Past Primary Turnout'],
                datasets: [{
                    label: 'Count',
                    data: [stats.totalRegistered, stats.totalPastPrimary],
                    backgroundColor: [
                        'rgba(56, 189, 248, 0.8)', // Sky blue
                        'rgba(16, 185, 129, 0.8)'  // Emerald green
                    ],
                    borderColor: [
                        'rgba(56, 189, 248, 1)',
                        'rgba(16, 185, 129, 1)'
                    ],
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) { return context.parsed.y.toLocaleString(); }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: {
                            callback: function(value) { return value.toLocaleString(); }
                        }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });

        // 2. Doughnut Chart: Goal Target
        const ctxGoal = document.getElementById('goalChart').getContext('2d');
        goalChart = new Chart(ctxGoal, {
            type: 'doughnut',
            data: {
                labels: ['Projected Target', 'Remaining to Goal'],
                datasets: [{
                    data: [stats.totalTarget, Math.max(0, COUNTY_GOAL - stats.totalTarget)],
                    backgroundColor: [
                        'rgba(250, 204, 21, 0.9)', // Yellow
                        'rgba(255, 255, 255, 0.1)'  // Faint background
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '80%',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
        
        // Update Text Display
        document.getElementById('goalTargetText').innerText = stats.totalTarget.toLocaleString();
    }

    function updateCharts(filter) {
        const stats = aggregateData(filter);
        
        // Update Bar Chart
        voterChart.data.datasets[0].data = [stats.totalRegistered, stats.totalPastPrimary];
        voterChart.update();
        
        // Update Goal Chart
        goalChart.data.datasets[0].data = [stats.totalTarget, Math.max(0, COUNTY_GOAL - stats.totalTarget)];
        goalChart.update();
        
        // Update Text with animation counter
        const targetEl = document.getElementById('goalTargetText');
        animateValue(targetEl, parseInt(targetEl.innerText.replace(/,/g, '')), stats.totalTarget, 500);
    }
    
    // Helper animation for number roll
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start).toLocaleString();
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }


    // -------------------------------------------------------------
    // 3. User Interaction / Button Logic
    // -------------------------------------------------------------
    
    function updateActiveButton(activeBtnId) {
        ['btn-show-all', 'btn-show-filled', 'btn-show-vacant'].forEach(id => {
            const btn = document.getElementById(id);
            if(btn) {
                if (id === activeBtnId) {
                    btn.classList.add('active');
                    btn.style.boxShadow = '0 0 15px rgba(255,255,255,0.3)';
                } else {
                    btn.classList.remove('active');
                    btn.style.boxShadow = 'none';
                }
            }
        });
    }

    const btnAll = document.getElementById('btn-show-all');
    const btnFilled = document.getElementById('btn-show-filled');
    const btnVacant = document.getElementById('btn-show-vacant');

    if (btnAll) btnAll.addEventListener('click', () => {
        currentFilter = 'all';
        geojsonLayer.setStyle(styleFeature);
        updateLabels();
        updateActiveButton('btn-show-all');
        updateCharts('all');
    });

    if (btnFilled) btnFilled.addEventListener('click', () => {
        currentFilter = 'filled';
        geojsonLayer.setStyle(styleFeature);
        updateLabels();
        updateActiveButton('btn-show-filled');
        updateCharts('filled');
    });

    if (btnVacant) btnVacant.addEventListener('click', () => {
        currentFilter = 'vacant';
        geojsonLayer.setStyle(styleFeature);
        updateLabels();
        updateActiveButton('btn-show-vacant');
        updateCharts('vacant');
    });

    // Initialize 
    updateActiveButton('btn-show-all');
    updateLabels();
    initCharts();
});
