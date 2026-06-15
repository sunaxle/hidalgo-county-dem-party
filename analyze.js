const fs = require('fs');
const vm = require('vm');

let context = vm.createContext({ window: {}, sessionStorage: { getItem: () => null, setItem: () => null } });

let mapText = fs.readFileSync('js/precinct_mapping_data.js', 'utf8');
vm.runInContext(mapText, context);

let chairText = fs.readFileSync('js/chair_data.js', 'utf8');
vm.runInContext(chairText, context);

let text = fs.readFileSync('hidalgo-election-map/hidalgo_precincts.js', 'utf8');
vm.runInContext(text, context);

let mapping = context.precinctDistricts;
let chairData = context.chairDataList;
let geojson = context.hidalgoPrecinctsData;

let totalMapPrecincts = geojson.features.length;

let allPrecinctIds = geojson.features.map(f => {
    let p = f.properties.PREC || f.properties.ID;
    if(!p && f.properties.tooltip) {
        let m = f.properties.tooltip.match(/Precinct\s*(\d+)/i);
        if(m) p = m[1];
    }
    return p ? parseInt(p, 10).toString() : 'UNKNOWN';
});

let filledPrecincts = new Set(chairData.map(c => parseInt(c.precinct, 10).toString()));
let totalFilled = filledPrecincts.size;
let totalVacant = allPrecinctIds.length - totalFilled;

console.log(`Total Precincts: ${allPrecinctIds.length}`);
console.log(`Filled Precincts: ${totalFilled} (${((totalFilled / allPrecinctIds.length) * 100).toFixed(1)}%)`);
console.log(`Vacant Precincts: ${totalVacant}`);

let vacantByCity = {};

allPrecinctIds.forEach(pct => {
    if (!filledPrecincts.has(pct)) {
        let mapInfo = mapping.find(m => parseInt(m.PRECINCT, 10).toString() === pct);
        let city = mapInfo ? mapInfo.CITY : 'Unknown/Rural';
        if (!city || city.trim() === '') city = 'Rural/Unincorporated';
        vacantByCity[city] = (vacantByCity[city] || 0) + 1;
    }
});

console.log(`\nVacant breakdown:`);
let entries = Object.entries(vacantByCity).sort((a,b) => b[1] - a[1]);
for (let [city, count] of entries) {
    console.log(`- ${city}: ${count}`);
}
