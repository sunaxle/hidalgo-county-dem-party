/**
 * VAN Auto Sender - Google Apps Script
 * 
 * Instructions:
 * 1. Open your Precinct Chairs Google Sheet.
 * 2. Click "Extensions" > "Apps Script".
 * 3. Paste this code into the editor.
 * 4. Save and close the editor. Refresh your Google Sheet.
 * 5. A new menu "VAN Campaign Tools" will appear at the top.
 */

const EMAIL_SUBJECT = "Your Precinct Superpower 🚀";

// The raw HTML of our Ultimate VAN Email
// Make sure to replace the GIF link and Concierge link with your actual hosted links once live!
const HTML_BODY = `
<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: Arial, sans-serif; color: #333333; line-height: 1.6; background-color: #f4f4f4; padding: 20px; }
  .container { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; }
  .header { background: #0f172a; color: white; padding: 20px; text-align: center; }
  .content { padding: 30px; }
  .gif-container { text-align: center; margin: 20px 0; }
  .gif-container img { max-width: 100%; border: 2px solid #e2e8f0; border-radius: 8px; }
  .btn { display: block; width: 90%; margin: 10px auto; padding: 15px; text-decoration: none; border-radius: 6px; font-weight: bold; text-align: center; }
  .btn-primary { background-color: #2563eb; color: #ffffff; }
  .btn-secondary { background-color: #ffffff; color: #0f172a; border: 2px solid #0f172a; }
  .footer { text-align: center; padding: 20px; font-size: 12px; color: #64748b; background: #f8fafc; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h2 style="margin:0; font-size: 24px;">Your Precinct Superpower 🚀</h2>
  </div>
  <div class="content">
    <p>Hi {{FIRST_NAME}},</p>
    <p>As a Precinct Chair, your time is your most valuable asset. If you are knocking on random doors hoping to find Democrats, you are working too hard.</p>
    <p>We want to give you access to <strong>VAN (Voter Activation Network)</strong>. It is the ultimate superpower for organizers. It tells you exactly who the most reliable Democrats are in your specific neighborhood.</p>
    <div class="gif-container">
      <img src="https://drive.google.com/uc?export=view&id=1M87GoePX6GY56wdNOtyis8VuYL_UwYMV" alt="VAN Tutorial Preview">
    </div>
    <p>We have two options to help you mobilize your neighborhood this weekend:</p>
    <div class="button-group">
      <a href="mailto:info@hidalgocountydems.org?subject=I%20want%20VAN%20Access!&body=Please%20set%20up%20my%20VAN%20account." class="btn btn-primary">🎓 Set up my VAN Account</a>
      <a href="https://hidalgocountydems.org/van_concierge.html" class="btn btn-secondary">🚀 I'm too busy, just cut my list for me</a>
    </div>
  </div>
  <div class="footer">Hidalgo County Democratic Party</div>
</div>
</body>
</html>
`;

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('VAN Campaign Tools')
      .addItem('Send Onboarding Emails', 'sendVanEmails')
      .addToUi();
}

function sendVanEmails() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const dataRange = sheet.getDataRange();
  const data = dataRange.getValues();
  
  // Assuming headers are in Row 1:
  // Column A: Precinct
  // Column B: First Name
  // Column C: Last Name
  // Column D: Email
  // Column E: Phone
  // Column F: VAN Access Status (If empty, send email. If 'Sent' or 'Active', skip)
  
  let emailsSent = 0;

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const firstName = row[1]; // Index 1 is Column B (First Name)
    const emailAddress = row[3]; // Index 3 is Column D (Email)
    const status = row[5]; // Index 5 is Column F (VAN Access Status)

    // Only send if they have an email address and we haven't sent it yet
    if (emailAddress && emailAddress.includes("@") && (!status || status === "")) {
      
      // Personalize the email HTML
      const personalizedHtml = HTML_BODY.replace("{{FIRST_NAME}}", firstName);
      
      // Send the email
      MailApp.sendEmail({
        to: emailAddress,
        subject: EMAIL_SUBJECT,
        htmlBody: personalizedHtml,
        name: "Hidalgo County Democratic Party"
      });
      
      // Update spreadsheet to mark as sent (Column F is index 6 in getRange which is 1-based)
      sheet.getRange(i + 1, 6).setValue("Sent Email");
      emailsSent++;
    }
  }
  
  SpreadsheetApp.getUi().alert(`Success! Sent ${emailsSent} VAN Onboarding emails.`);
}
