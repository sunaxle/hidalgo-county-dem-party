const fs = require('fs');
let text = fs.readFileSync('hidalgo-election-map/hidalgo_precincts.js', 'utf8');
text = text.replace('let hidalgoPrecinctsData = ', '');
text = text.trim();
if (text.endsWith(';')) text = text.slice(0, -1);
const geojson = JSON.parse(text);

let chairText = fs.readFileSync('js/chair_data.js', 'utf8');
chairText = chairText.replace('const chairDataList = ', '');
chairText = chairText.trim();
if (chairText.endsWith(';')) chairText = chairText.slice(0, -1);
const chairData = JSON.parse(chairText);

// Find 99
let target = geojson.features.find(f => {
    let p = f.properties.PREC || f.properties.ID;
    if(!p && f.properties.tooltip) {
        let m = f.properties.tooltip.match(/Precinct\s*(\d+)/i);
        if(m) p = m[1];
    }
    return parseInt(p, 10) === 99;
});

// A naive bounding box intersection for GeoJSON polygons
function getBounds(coords) {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    const processCoord = (c) => {
        if (typeof c[0] === 'number') {
            minX = Math.min(minX, c[0]);
            maxX = Math.max(maxX, c[0]);
            minY = Math.min(minY, c[1]);
            maxY = Math.max(maxY, c[1]);
        } else {
            c.forEach(processCoord);
        }
    };
    coords.forEach(processCoord);
    return {minX, minY, maxX, maxY};
}

let tBounds = getBounds(target.geometry.coordinates);
// Expand slightly
let pad = 0.005; // 0.005 degrees is approx 500m
tBounds.minX -= pad; tBounds.maxX += pad;
tBounds.minY -= pad; tBounds.maxY += pad;

let neighbors = [];
geojson.features.forEach(f => {
    if (f === target) return;
    let b = getBounds(f.geometry.coordinates);
    if (!(tBounds.minX > b.maxX || tBounds.maxX < b.minX || tBounds.minY > b.maxY || tBounds.maxY < b.minY)) {
        let p = f.properties.PREC || f.properties.ID;
        if(!p && f.properties.tooltip) {
            let m = f.properties.tooltip.match(/Precinct\s*(\d+)/i);
            if(m) p = m[1];
        }
        neighbors.push(parseInt(p, 10).toString());
    }
});

let pcts = ['99', ...new Set(neighbors)];
let filled = chairData.filter(c => pcts.includes(c.precinct));

console.log("NEIGHBORS OF 99:", pcts.join(", "));
console.log("\nFILLED CONTACTS:");
filled.forEach(c => {
    console.log(`Precinct ${c.precinct}: ${c.name} - ${c.phone} - ${c.email}`);
});
