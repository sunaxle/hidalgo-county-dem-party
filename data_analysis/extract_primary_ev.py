import sys
import pdfplumber
import json

def extract_primary_ev(path):
    print(f"Parsing Primary Locations PDF ({path}) for EV totals...")
    location_totals = {}
    
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    clean_row = [str(c).strip().replace('\n', ' ') if c else '' for c in row]
                    
                    # Target row with a total column at the very end
                    if len(clean_row) > 5 and clean_row[1] and "POLLING" not in clean_row[1].upper():
                        loc_name = clean_row[1]
                        # For the Feb-March EV SUBS, sum up D/R totals or just take the very last column
                        # Often the rightmost column is the total. Let's safely extract it:
                        try:
                            if clean_row[-1].isdigit():
                                total = int(clean_row[-1].replace(',', ''))
                            elif clean_row[-2].isdigit():
                                total = int(clean_row[-2].replace(',', ''))
                            else:
                                continue
                            location_totals[loc_name] = total
                        except ValueError:
                            pass
                            
    print("Found totals for", len(location_totals), "locations.")
    for k,v in list(location_totals.items())[:3]:
        print(f"{k}: {v}")
        
    with open("data_analysis/location_turnout_primary.json", "w") as f:
        json.dump(location_totals, f, indent=2)

if __name__ == "__main__":
    extract_primary_ev(sys.argv[1])
