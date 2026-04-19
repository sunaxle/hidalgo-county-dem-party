import pdfplumber
import os

pdf_path = "downloads/Gonzalez_Rodolfo_Rudy/Campaign_Finance_Report_July_2017.pdf"

def analyze_pdf(path):
    print(f"📄 Analyzing: {path}")
    
    if not os.path.exists(path):
        print("❌ File not found.")
        return
        
    try:
        with pdfplumber.open(path) as pdf:
            pages = pdf.pages
            print(f"➡️ Total pages: {len(pages)}")
            
            # Check if page 1 has text (native PDF vs Image scan)
            first_page_text = pages[0].extract_text()
            if first_page_text and len(first_page_text.strip()) > 10:
                print("✅ STATUS: NATIVE TEXT PDF (Machine Readable)")
                print("--- First Page Preview ---")
                print(first_page_text[:500])
                print("--------------------------")
                
                # Look for Schedule A1
                print("\n🔍 Scanning for Schedule A1 (Monetary Contributions)...")
                a1_found = False
                for i, page in enumerate(pages):
                    text = page.extract_text()
                    if text and "SCHEDULE A1" in text:
                        print(f"   🎯 Schedule A1 identified on Page {i+1}")
                        a1_found = True
                        
                if not a1_found:
                    print("   ⚠️ Schedule A1 not found in raw text. May require regex tuning.")
                        
            else:
                print("⚠️ STATUS: SCANNED IMAGE PDF (Requires Tesseract OCR)")
                
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")

if __name__ == "__main__":
    analyze_pdf(pdf_path)
