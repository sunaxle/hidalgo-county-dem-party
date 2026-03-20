const fs = require('fs');

function parseCSV(csvText) {
    const lines = csvText.split("\\n").filter(line => line.trim().length > 0);
    if (lines.length < 2) return [];

    const headers = lines[0].split(",").map(h => h.trim());
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const rowString = lines[i];
        const rowValues = [];
        let inQuotes = false;
        let currentValue = "";

        for (let char of rowString) {
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                rowValues.push(currentValue.trim());
                currentValue = "";
            } else {
                currentValue += char;
            }
        }
        rowValues.push(currentValue.trim());

        const rowObj = {};
        headers.forEach((header, index) => {
            rowObj[header] = rowValues[index] || "";
        });
        data.push(rowObj);
    }
    
    return data;
}

const csv = fs.readFileSync('data/mock_volunteers.csv', 'utf8');
const result = parseCSV(csv);
console.log("Total records:", result.length);
if (result.length > 0) {
    console.log("First item:", result[0]);
    
    const chairs = result.filter(d => d["Role"] === "Precinct Chair" || d["Role"] === "Block Captain");
    console.log("Match count:", chairs.length);
}
