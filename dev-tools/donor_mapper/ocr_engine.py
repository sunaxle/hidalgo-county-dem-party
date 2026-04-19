import pdfplumber
import pytesseract
import sys

# Because Tesseract is installed in /opt/homebrew/bin, we must tell pytesseract exactly where it is.
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

pdf_path = "downloads/Gonzalez_Rodolfo_Rudy/Campaign_Finance_Report_July_2017.pdf"

def brute_force_ocr(path):
    print(f"🔥 INITIATING TESSERACT OCR ON: {path}\\n")
    
    try:
        with pdfplumber.open(path) as pdf:
            # Grab page 4 (usually where the meat of Schedule A1 is, or page 3)
            page = pdf.pages[3] 
            
            # Extract the raw visual image of the page
            print("📸 Rendering PDF page into an image block...")
            page_image = page.to_image(resolution=300).original
            
            # Feed the raw image into Tesseract
            print("🧠 Feeding image matrix to Tesseract C++ Engine...\\n")
            extracted_text = pytesseract.image_to_string(page_image)
            
            print("====================================")
            print("=== RAW EXTRACTED OCR TEXT ===")
            print("====================================")
            print(extracted_text[:1000]) # Print first 1000 chars
            print("====================================")
            
            if "SCHEDULE A" in extracted_text.upper():
                print("✅ STATUS: Schedule A Successfully Identified via OCR!")
            else:
                print("⚠️ STATUS: Schedule A not immediately visible on this page.")
                
    except Exception as e:
        print(f"❌ OCR Pipeline Failed: {e}")

if __name__ == "__main__":
    brute_force_ocr(pdf_path)
