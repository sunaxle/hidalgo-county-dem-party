document.addEventListener("DOMContentLoaded", () => {
    // Basic map setup
    const map = L.map('map').setView([26.2, -98.15], 11);
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(map);

    let isSimulated = false;
    let showCommerce = false;
    
    let precinctsLayer, evSitesLayer, newSitesLayer, commerceLayer;
    let geojsonData = null;
    let snappedSites = [];
    let commerceData = null;

    const getColor = (d) => {
        return d > 8 ? '#800026' :
               d > 6  ? '#BD0026' :
               d > 4  ? '#E31A1C' :
               d > 2  ? '#FC4E2A' :
               d > 1   ? '#FD8D3C' :
               d > 0.5   ? '#FEB24C' :
                          '#FFEDA0';
    };

    const stylePrecinct = (feature) => {
        let cdColor = 'rgba(255,255,255,0.1)';
        let cdWeight = 1;
        if(feature.properties.CD === "15") { cdColor = '#eab308'; cdWeight = 2; }
        if(feature.properties.CD === "28") { cdColor = '#a855f7'; cdWeight = 2; }
        
        let dist = isSimulated ? (feature.properties.simulated_logistics_distance || feature.properties.distance_to_ev) : feature.properties.distance_to_ev;
        return {
            fillColor: getColor(dist || 0),
            weight: cdWeight,
            opacity: 1,
            color: cdColor,
            fillOpacity: 0.6
        };
    };

    // Load Data
    Promise.all([
        fetch('data_analysis/hidalgo_logistics_precincts.geojson').then(r => r.json()),
        fetch('data/hidalgo_grocery.geojson').then(r => r.json()),
        fetch('data_analysis/logistics_sites.json').then(r => r.json()),
        fetch('hidalgo-election-map/polling_locations.geojson').then(r => r.json())
    ]).then(([precincts, groceries, sites, evs]) => {
        geojsonData = precincts;
        commerceData = groceries;
        snappedSites = sites;

        // Draw Precincts
        precinctsLayer = L.geoJson(geojsonData, { style: stylePrecinct }).addTo(map);

        // Draw basic EV sites fixed
        const drawOriginalSites = () => {
             evSitesLayer = L.layerGroup();
             evs.features.forEach(f => {
                 let lon = f.geometry.coordinates[0];
                 let lat = f.geometry.coordinates[1];
                 let name = f.properties.location || "Polling Site";
                 let marker = L.circle([lat, lon], {
                    color: '#60a5fa', fillOpacity: 0.8, weight: 2, radius: 400
                 });
                 let zone = L.circle([lat, lon], {
                    color: '#60a5fa', weight: 2, fill: false, dashArray: '5, 5', radius: 3701 // 2.3 miles
                 });
                 marker.bindTooltip(name);
                 evSitesLayer.addLayer(marker);
                 evSitesLayer.addLayer(zone);
             });
             evSitesLayer.addTo(map);
        };
        drawOriginalSites();
        
        // Setup Toggles
        document.getElementById('toggle-sim').addEventListener('click', (e) => {
            isSimulated = !isSimulated;
            if(isSimulated) {
                e.target.classList.add('active');
                e.target.innerText = "Revert to Original";
                if(!newSitesLayer) {
                    newSitesLayer = L.layerGroup();
                    
                    snappedSites.forEach(s => {
                         let color = s.is_snapped ? '#10b981' : '#f59e0b'; // Green if snapped, Orange if drift
                         let marker = L.circle([s.lat, s.lon], {
                            color: color, fillOpacity: 0.8, weight: 2, radius: 500
                         });
                         let note = s.is_snapped ? `Snapped to: ${s.snapped_to}` : `Strict K-Means Centroid (No Groceries near)`;
                         marker.bindPopup(`<b>Proposed Site</b><br>${note}`);
                         newSitesLayer.addLayer(marker);
                    });
                }
                newSitesLayer.addTo(map);
            } else {
                e.target.classList.remove('active');
                e.target.innerText = "Run Logistics Simulation (Snap to HEB)";
                if(newSitesLayer) map.removeLayer(newSitesLayer);
            }
            precinctsLayer.eachLayer(layer => layer.setStyle(stylePrecinct(layer.feature)));
        });

        document.getElementById('toggle-commerce').addEventListener('click', (e) => {
            showCommerce = !showCommerce;
            if(showCommerce) {
                e.target.classList.add('active');
                if(!commerceLayer) {
                    commerceLayer = L.geoJson(commerceData, {
                        pointToLayer: function (feature, latlng) {
                            return L.circleMarker(latlng, {
                                radius: 8,
                                fillColor: "#ec4899", // pink
                                color: "#fff",
                                weight: 1,
                                opacity: 1,
                                fillOpacity: 0.8
                            });
                        },
                        onEachFeature: (feature, layer) => {
                            layer.bindTooltip("🛒 " + feature.properties.name);
                        }
                    });
                }
                commerceLayer.addTo(map);
            } else {
                e.target.classList.remove('active');
                if(commerceLayer) map.removeLayer(commerceLayer);
            }
        });
    });
});
