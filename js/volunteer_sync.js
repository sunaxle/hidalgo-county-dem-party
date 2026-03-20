/**
 * Volunteer Sync Module
 * Fetches and parses the published Google Sheet CSV (or locally mocked CSV).
 */

const GOOGLE_SHEET_CSV_URL = "data/prepped_old_volunteer_list.csv"; // Authenticated legacy target

async function fetchVolunteerData() {
    try {
        const fetchUrl = GOOGLE_SHEET_CSV_URL.includes("?") 
            ? GOOGLE_SHEET_CSV_URL + "&t=" + new Date().getTime() 
            : GOOGLE_SHEET_CSV_URL + "?t=" + new Date().getTime();
            
        const response = await fetch(fetchUrl);
        if (!response.ok) throw new Error("Network response was not ok");
        
        const csvText = await response.text();
        return parseCSV(csvText);
    } catch (error) {
        console.error("Failed to load volunteer data:", error);
        return [];
    }
}

function parseCSV(csvText) {
    const lines = csvText.split(/\r?\n/).filter(line => line.trim().length > 0);
    if (lines.length < 2) return [];

    const headers = lines[0].split(",").map(h => h.trim());
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        // Basic CSV regex to handle commas inside quotes (if any)
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

// Attach globally for easy access across different pages
window.fetchVolunteerData = fetchVolunteerData;
