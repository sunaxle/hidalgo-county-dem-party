import pdfplumber
import pytesseract
import re
import sys

# Connect directly to the Homebrew C++ binaries
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

target_pdf = "downloads/Gonzalez_Rodolfo_Rudy/Campaign_Finance_Report_July_2017.pdf"

def parse_ocr_text(text):
    """Attempt to force raw OCR strings into a structured database payload"""
    donors = []
    
    # 1. Look for Date (e.g. 05/12/2017, 5/12/17, or 05-12-2017)
    date_pattern = r'(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})'
    # 2. Look for Dollar Amounts (e.g. $3500.00, 3,500.00, or even $3500)
    amount_pattern = r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    
    # Check if the page has both a date and a monetary value
    date_match = re.search(date_pattern, text)
    amount_match = re.search(amount_pattern, text)
    
    if amount_match: # Sometimes dates are illegible in Tesseract, rely on Amounts
        date_str = date_match.group(1) if date_match else "Unreadable by OCR"
        amount_str = amount_match.group(1)
        
        # Look for ZIP codes as an anchor for the address
        zip_pattern = r'(\b(?:TX|Texas)\s+\d{5}\b)'
        address_match = re.search(zip_pattern, text, re.IGNORECASE)
        address_str = address_match.group(1) if address_match else "Unreadable by OCR"
        
        donors.append({
            "Date": date_str,
            "Amount": amount_str,
            "Address_Hint": address_str,
            "Raw_Scan": text.replace('\n', '  ')[:150]
        })
        
    return donors

def execute_pipeline():
    print(f"🔥 EXECUTING FULL PIPELINE TEST ON: {target_pdf}\\n")
    master_database = []
    
    try:
        with pdfplumber.open(target_pdf) as pdf:
            # We will scan the first 8 pages to find Schedules
            print("🖨️  Scanning PDF...")
            for i in range(min(8, len(pdf.pages))):
                page = pdf.pages[i]
                print(f"   [Page {i+1}] Rendering to image matrix...")
                
                # Convert the PDF page to a raw pixel image
                page_image = page.to_image(resolution=300).original
                
                # Force Tesseract C++ to read the pixels
                text = pytesseract.image_to_string(page_image)
                
                # If the image contains a financial schedule, parse it
                if "SCHEDULE" in text.upper():
                    print(f"   ✅ Schedule identified on Page {i+1}. Parsing data...")
                    structured_data = parse_ocr_text(text)
                    
                    for donor in structured_data:
                        print("      --------------------------------------------------")
                        print(f"      💰 AMOUNT: ${donor['Amount']}")
                        print(f"      📅 DATE: {donor['Date']}")
                        print(f"      🏠 ADDRESS HINT: {donor['Address_Hint']}")
                        print("      --------------------------------------------------")
                        master_database.append(donor)
                        
            print(f"\\n🏁 PIPELINE TEST COMPLETE. Extracted {len(master_database)} financial entries via raw OCR.")
                        
    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    execute_pipeline()
