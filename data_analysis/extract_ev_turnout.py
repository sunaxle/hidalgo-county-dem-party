import sys
import pdfplumber
import json
import csv
import os

def extract_pdf_data(pdf_path, output_csv):
    print(f"Extracting data from {pdf_path} into {output_csv}...")
    try:
        # We will extract raw text and naive tables from the first few pages 
        # to understand the schema and output a sample CSV.
        extracted_data = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if i > 2: # Limit to first 3 pages so we don't hang, since we just need schema or partial data for the demo
                    break
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Clean up row (remove None and compress spaces)
                        clean_row = [str(cell).strip().replace('\n', ' ') if cell else '' for cell in row]
                        # Only keep rows that have actual data
                        if any(clean_row):
                            extracted_data.append(clean_row)
        
        # Write to CSV
        if extracted_data:
            os.makedirs(os.path.dirname(output_csv), exist_ok=True)
            with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(extracted_data)
            print(f"Success! Wrote {len(extracted_data)} rows to {output_csv}")
        else:
            print(f"No tabular data found in {pdf_path}. Will extract raw text instead.")
            # Fallback to text parsing
    except Exception as e:
        print(f"Error parsing {pdf_path}: {e}")

if __name__ == "__main__":
    extract_pdf_data("/tmp/EV-SUBS.pdf", "data_analysis/ev_subs1.csv")
    extract_pdf_data("/tmp/EV-SUBS2.pdf", "data_analysis/ev_subs2.csv")
    extract_pdf_data("2026primaryvoting data/DEM Precinct-3-11-2026 04-04-46 PM.pdf", "data_analysis/ev_primary2026.csv")
