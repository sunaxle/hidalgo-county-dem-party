/**
 * 🚀 HCDP CRM AUTOMATION: VAN Outreach & Follow-up Email Blaster
 * 
 * INSTRUCTIONS:
 * 1. Open Google Sheets and create a new sheet.
 * 2. Import your 'pending_van_emails.csv' into the sheet.
 * 3. Go to Extensions -> Apps Script.
 * 4. Paste this exact code into the editor.
 * 5. Run the `sendCombinedOutreachEmails` function to blast the 161 emails!
 */

function sendCombinedOutreachEmails() {
  // Get the active sheet (where you pasted your CSV)
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // The HTML Body of the combined email
  const htmlBodyTemplate = `
    <p>Hi {{NAME}},</p>

    <p>You are the grassroots foundation of our party, and our success completely depends on the work we all do in our own neighborhoods.</p>

    <p>My main goal is to leave the infrastructure of our precinct chairs stronger than ever before. We want to give you as many tools, information, and options as possible so you have everything you need to pull out maximum voter turnout in <strong>Precinct {{PRECINCT}}</strong>.</p>

    <h3 style="color: #1a56db;">1. URGENT: Request Your VAN Access</h3>
    <p>To effectively reach out to the Democrats in your neighborhood, <strong>you need access to the Voter Activation Network (VAN).</strong></p>

    <p>Our records currently indicate that you do not have access to the VAN. We need to get you set up immediately so you can start pulling lists of voters in your neighborhood!</p>

    <p style="background-color: #fef08a; padding: 15px; border-left: 4px solid #854d0e;">
      <strong>Action Required: Would you like to get access to the VAN?</strong><br>
      <strong>If yes, please reply directly to this email at <a href="mailto:info@hidalgocountydems.org">info@hidalgocountydems.org</a>.</strong>
    </p>

    <p>Once you reply and we get your account created, you will receive your login credentials.</p>

    <h3 style="color: #1a56db;">2. Precinct Chair 101 Training</h3>
    <p>As we discussed, we are hosting <strong>Precinct Chair 101</strong> meetings and training sessions! Whether you are a brand new chair or just need a quick refresher, this training is critical.</p>
    <ul>
      <li><strong>Precinct Chair 101 Virtual Training</strong><br>Wednesday, June 10, 5:30 PM - 6:30 PM | <a href="https://mobilize.us/s/YQ8PQh">Sign Up on Mobilize</a></li>
      <li><strong>"What’s A Precinct Chair?" Virtual Training</strong><br>Wednesday, June 17, 5:30 PM - 6:30 PM | <a href="https://mobilize.us/s/yUo7VI">Sign Up on Mobilize</a></li>
    </ul>

    <h3 style="color: #1a56db;">3. Key Updates & Campaign Events</h3>
    <ul>
      <li><strong>Phone Banking Push:</strong> We are making a massive push for phone banking right now. Please sign up for a shift on Mobilize!</li>
      <li><strong>Campaign Needs:</strong> Bobby Pulido, the Henry Cuellar Team, and Talarico for US Senate are actively looking for grassroots support.</li>
      <li><strong>Menu of Options:</strong> If you find neighbors who want to help but don't want to knock on doors, ask them to host a yard sign, hand out slate cards at the polls, or simply text 5 friends!</li>
    </ul>

    <h3 style="color: #1a56db;">4. Your Next Steps & Onboarding Resources</h3>
    <p>Once you do get access to the VAN, please read through the following resources so you know exactly how to use it, what it means to be a precinct chair, and where to find all the tools the party has built for you:</p>
    <ul>
      <li><strong>Chair Onboarding Page:</strong> <a href="https://hidalgocountydems.org/chair_onboarding.html">https://hidalgocountydems.org/chair_onboarding.html</a></li>
      <li><strong>Precinct Chair Playbook:</strong> <a href="https://docs.google.com/document/d/16jS0hZ8F3QiPt2AQ-cB3TYRbkxNevoLum6IQbNPeyiY/edit?usp=sharing">Google Doc Link</a></li>
      <li><strong>Precinct Chair Hub:</strong> <a href="https://hidalgocountydems.org/precinct_chairs.html">https://hidalgocountydems.org/precinct_chairs.html</a></li>
      <li><strong>Master Volunteer Shift Survey:</strong> <a href="https://hidalgocountydems.org/volunteer_master_survey.html">https://hidalgocountydems.org/volunteer_master_survey.html</a></li>
    </ul>

    <p>Thank you again for stepping up to lead your precinct. Remember guys, it's also about having fun! Make the best of it, get out there and meet your neighbors. Let's get to work!</p>

    <p>Best,<br><br><strong>Richard Gonzalez</strong><br>County Chair, Hidalgo County Democratic Party</p>
  `;

  let emailsSent = 0;

  // Assuming row 0 is headers (Name, Email, Precinct)
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const name = row[0];
    const emailAddress = row[1];
    const precinct = row[2];

    if (emailAddress && emailAddress.includes('@')) {
      // Personalize the email template
      let customizedBody = htmlBodyTemplate.replace('{{NAME}}', name);
      customizedBody = customizedBody.replace('{{PRECINCT}}', precinct);

      try {
        GmailApp.sendEmail(emailAddress, "Thank You & URGENT: Request Your Precinct VAN Access Today!", "", {
          htmlBody: customizedBody,
          name: "Richard Gonzalez - HCDP Chair",
          from: "info@hidalgocountydems.org",
          replyTo: "info@hidalgocountydems.org"
        });
        
        // Log to the sheet that it was sent
        sheet.getRange(i + 1, 4).setValue("SENT"); 
        emailsSent++;
        
      } catch (e) {
        sheet.getRange(i + 1, 4).setValue("ERROR: " + e.toString());
      }
    }
  }

  Logger.log("Successfully blasted " + emailsSent + " emails!");
  SpreadsheetApp.getUi().alert("Email Blast Complete", "Successfully sent " + emailsSent + " VAN Outreach emails.", SpreadsheetApp.getUi().ButtonSet.OK);
}
