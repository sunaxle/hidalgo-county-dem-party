import pandas as pd
import json

df = pd.read_csv('/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/HCDP_Precinct_Contacts.csv')

contact_map = {}
for index, row in df.iterrows():
    precinct = row['precinct']
    first = str(row['first']).strip()
    last = str(row['last']).strip()
    name = f"{first} {last}"
    if pd.isna(row['first']) or first == 'nan':
        name = "Unknown"
    
    key = f"Precinct {precinct} - {name}"
    
    email = str(row['email']).strip()
    phone = str(row['phone']).strip()
    if pd.isna(row['email']) or email == 'nan':
        email = ""
    if pd.isna(row['phone']) or phone == 'nan':
        phone = ""
    
    contact_map[key] = {
        "email": email,
        "phone": phone
    }

js_code = f"""/**
 * VAN Concierge Web App Backend
 * Securely looks up Email and Phone numbers based on the user's dropdown selection.
 */

// DO NOT SHARE THIS FILE - CONTAINS PRIVATE CONTACT INFO
var CHAIR_DATABASE = {json.dumps(contact_map, indent=2)};

function doPost(e) {{
  try {{
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Grab the data sent from the website
    var chair = e.parameter.precinct_chair;
    var listType = e.parameter.list_type;
    var timestamp = new Date();
    
    // Secure Lookup!
    var email = "";
    var phone = "";
    if (CHAIR_DATABASE[chair]) {{
      email = CHAIR_DATABASE[chair].email;
      phone = CHAIR_DATABASE[chair].phone;
    }}
    
    // Drop it into a new row!
    sheet.appendRow([timestamp, chair, email, phone, listType]);
    
    // Tell the website it was successful
    return ContentService.createTextOutput("Success").setMimeType(ContentService.MimeType.TEXT);
    
  }} catch (error) {{
    return ContentService.createTextOutput("Error: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }}
}}
"""

with open('/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/scratch/backend.js', 'w') as f:
    f.write(js_code)
