// Google Apps Script for Hidalgo County Democrats Form Intake
// 1. Create a new Google Sheet
// 2. Click Extensions > Apps Script
// 3. Paste this entire code block into the editor, replacing the default code
// 4. Click 'Deploy' > 'New Deployment'
// 5. Select type: 'Web app'
// 6. Give it a description like "Website Forms"
// 7. Execute as: "Me (your email)"
// 8. Who has access: "Anyone"
// 9. Click Deploy, Authorize access, and COPY THE WEB APP URL!

const SHEET_NAME = 'Sheet1';

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    
    // Parse the incoming JSON payload from the website
    const data = JSON.parse(e.postData.contents);
    
    // Check if headers exist, if not, create them
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'Timestamp', 
        'Source Page', 
        'First Name', 
        'Last Name', 
        'Email', 
        'Phone', 
        'Zip Code', 
        'Message', 
        'SMS Opt-In', 
        'Email Opt-In', 
        'Phone Opt-In', 
        'In-Person Opt-In'
      ]);
      // Make headers bold
      sheet.getRange("A1:L1").setFontWeight("bold");
    }
    
    // Append the new row with the data received
    sheet.appendRow([
      new Date(),                             // Timestamp
      data.source || 'Unknown',               // Source Page (Contact, Subscribe, etc.)
      data.firstName || data.name || '',      // First Name (or Full Name if combined)
      data.lastName || '',                    // Last Name
      data.email || '',                       // Email
      data.phone || '',                       // Phone
      data.zipcode || '',                     // Zip Code
      data.message || '',                     // Message
      data.optInSms ? 'Yes' : 'No',           // SMS Opt-In
      data.optInEmail ? 'Yes' : 'No',         // Email Opt-In
      data.optInCall ? 'Yes' : 'No',          // Phone Opt-In
      data.optInPerson ? 'Yes' : 'No'         // In-Person Opt-In
    ]);
    
    return ContentService
      .createTextOutput(JSON.stringify({ 'result': 'success', 'row': sheet.getLastRow() }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ 'result': 'error', 'error': error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Handle CORS preflight requests
function doOptions(e) {
  return ContentService.createTextOutput("")
    .setMimeType(ContentService.MimeType.JSON)
    .setHeader("Access-Control-Allow-Origin", "*")
    .setHeader("Access-Control-Allow-Methods", "POST")
    .setHeader("Access-Control-Allow-Headers", "Content-Type");
}
