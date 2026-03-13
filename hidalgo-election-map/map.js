document.addEventListener("DOMContentLoaded", () => {
    // Initialize map
    const map = L.map('map').setView([26.3, -98.2], 9);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(map);

    function styleFeature(feature) {
        let winnerName = feature.properties.winner_name;
        let fillColor = '#cbd5e1'; let color = '#94a3b8'; let weight = 1; let fillOpacity = 0.5;
        if (winnerName && winnerName !== "No Winner" && winnerName !== "No Data") {
            fillColor = '#3b82f6'; color = '#1d4ed8'; weight = 1; fillOpacity = 0.6;
        }
        return { fillColor: fillColor, color: color, weight: weight, fillOpacity: fillOpacity };
    }

    function onEachFeature(feature, layer) {
        if (feature.properties && feature.properties.tooltip) { layer.bindPopup(feature.properties.tooltip); }
        layer.on({
            mouseover: (e) => {
                let layer = e.target;
                layer.setStyle({ weight: 3, color: '#22d3ee', fillOpacity: 0.8 });
                layer.bringToFront();
            },
            mouseout: (e) => { geojsonLayer.resetStyle(e.target); }
        });
    }

    let layerControl = L.control.layers(null, null, { collapsed: false }).addTo(map);

    // Use global variable hidalgoPrecinctsData directly!
    let geojsonLayer = L.geoJSON(hidalgoPrecinctsData, { style: styleFeature, onEachFeature: onEachFeature }).addTo(map);
    layerControl.addOverlay(geojsonLayer, "Winner Breakdown (Precincts)");
    map.fitBounds(geojsonLayer.getBounds());

    function loadPollingSites(map, layerControl) {
        const ONE_MILE_METERS = 1609.34;
        let earlyIcon = L.divIcon({ className: 'custom-polling-icon early-voting-icon', html: '🗳️', iconSize: [24, 24], iconAnchor: [12, 12] });
        let electionDayIcon = L.divIcon({ className: 'custom-polling-icon election-day-icon', html: '🇺🇸', iconSize: [24, 24], iconAnchor: [12, 12] });

        let earlyVotingLayer = L.layerGroup().addTo(map);
        let electionDayLayer = L.layerGroup(); 

        // Early Voting built instantly from memory var
        L.geoJSON(pollingLocationsData, {
             pointToLayer: function (feature, latlng) {
                 let circle = L.circle(latlng, { radius: ONE_MILE_METERS, color: '#16a34a', fillColor: '#22c55e', fillOpacity: 0.15, weight: 2, dashArray: '5, 5' });
                 let marker = L.marker(latlng, { icon: earlyIcon });
                 circle.addTo(earlyVotingLayer); return marker.addTo(earlyVotingLayer);
             },
             onEachFeature: function (feature, layer) {
                 if (feature.properties && feature.properties.name) {
                     layer.bindPopup(`<b>🗳️ Early Voting Site</b><br/><b>${feature.properties.name}</b><br/>${feature.properties.address}`);
                 }
             }
         });
         layerControl.addOverlay(earlyVotingLayer, "Early Voting Sites (1mi Radius)");

         // Election Day built instantly from memory var
         L.geoJSON(electionDayLocationsData, {
             pointToLayer: function (feature, latlng) {
                 let circle = L.circle(latlng, { radius: ONE_MILE_METERS, color: '#9333ea', fillColor: '#a855f7', fillOpacity: 0.15, weight: 2, dashArray: '5, 5' });
                 let marker = L.marker(latlng, { icon: electionDayIcon });
                 circle.addTo(electionDayLayer); return marker.addTo(electionDayLayer);
             },
             onEachFeature: function (feature, layer) {
                 if (feature.properties && feature.properties.name) {
                     layer.bindPopup(`<b>🇺🇸 Election Day Site</b><br/><b>${feature.properties.name}</b><br/>${feature.properties.address}`);
                 }
             }
         });
         layerControl.addOverlay(electionDayLayer, "Election Day Sites (1mi Radius)");
    }
    
    loadPollingSites(map, layerControl);
});
