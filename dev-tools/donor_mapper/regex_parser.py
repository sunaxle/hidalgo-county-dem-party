import re

# This is a sample OCR text block structured similar to how Tesseract reads a Texas TEC Form C/OH
sample_ocr_output = """
1 Total pages Schedule A1: 3
2 FILER NAME 3 Filer ID (Ethics Commission Filers)
Gonzalez, Rodolfo Rudy

4 Date 5 Full name of contributor CJ out-ot-state PAG (IDF: _)
07/15/2017 John Doe
6 Contributor address: City: State; Zip Code
123 Main St, McAllen, TX 78501
7 Amount of contribution ($)
$1000.00
8 Principal occupation / Job title (See Instructions) 9 Employer (See Instructions)
CEO None
"""

def extract_schedule_A1(text):
    print("🔬 Parsing Raw OCR Text into Structured Database format...")
    
    # We use regex to hunt for the specific anchor tags found on Texas Campaign Finance Forms
    # We look for "Date", "Full name of contributor", "Contributor address", and "Amount"
    
    # Extract Date (looking for MM/DD/YYYY)
    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    date = date_match.group(1) if date_match else "Unknown"
    
    # Extract Amount (looking for $ followed by numbers)
    amount_match = re.search(r'\$\s*(\d+[\.,]\d{2})', text)
    amount = amount_match.group(1) if amount_match else "Unknown"
    
    # Extract Name (often sits right next to or below the date)
    # This is a basic heuristical regex looking for words right after the date
    name_match = re.search(r'\d{2}/\d{2}/\d{4}\s+(.+?)(?=\n|$)', text)
    name = name_match.group(1).strip() if name_match else "Unknown"
    
    # Extract Address (looking for standard Zip code patterns)
    address_match = re.search(r'(\d+\s+[A-Za-z\s,]+(?:TX|Texas)\s+\d{5})', text)
    address = address_match.group(1) if address_match else "Unknown"
    
    # Structured Payload
    structured_data = {
        "Candidate": "Gonzalez, Rodolfo Rudy", 
        "Donor_Name": name,
        "Donor_Address": address,
        "Date": date,
        "Amount": amount
    }
    
    print("--------------------------------------------------")
    print(f"👤 DONOR: {structured_data['Donor_Name']}")
    print(f"🏠 ADDRESS: {structured_data['Donor_Address']}")
    print(f"📅 DATE: {structured_data['Date']}")
    print(f"💰 AMOUNT: ${structured_data['Amount']}")
    print("--------------------------------------------------")
    
    return structured_data

if __name__ == "__main__":
    extract_schedule_A1(sample_ocr_output)
    print("✅ Schema built. Next step: Hooking this parser directly into the live Tesseract pipeline.")
