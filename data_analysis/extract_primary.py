import sys
import PyPDF2
import json

def extract_precinct_totals(path):
    print("Parsing 2026 Primary PDF for precinct totals and Registered Voters...")
    precinct_totals = {}
    current_precinct = None
    
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if not text: continue
            
            lines = text.split('\n')
            for line in lines:
                # "001 92 of 1,016 registered voters = 9.06%"
                if "registered voters" in line.lower() and "=" in line:
                    parts = line.split(" ")
                    if len(parts) > 3 and parts[0].isdigit():
                        current_precinct = str(int(parts[0]))
                        # Parse the Registered Voters out of the string "1,016" -> 1016
                        try:
                            # Search for the string right before "registered"
                            idx = [i for i, v in enumerate(parts) if "registered" in v.lower()][0]
                            rv_count = int(parts[idx - 1].replace(',', ''))
                            if current_precinct not in precinct_totals:
                                precinct_totals[current_precinct] = {
                                    "early_voting": 0, 
                                    "election_day": 0, 
                                    "total_turnout": 0,
                                    "registered_voters": rv_count
                                }
                        except Exception:
                            pass
                
                # Check for cast votes line
                if line.startswith("Cast Votes:"):
                    parts = line.split(" ")
                    if len(parts) >= 8:
                        try:
                            ev_votes = int(parts[4].replace(',',''))
                            ed_votes = int(parts[6].replace(',',''))
                            total_votes = int(parts[8].replace(',',''))
                            if current_precinct:
                                if ev_votes > precinct_totals[current_precinct].get("early_voting", 0):
                                    precinct_totals[current_precinct]["early_voting"] = ev_votes
                                if ed_votes > precinct_totals[current_precinct].get("election_day", 0):
                                    precinct_totals[current_precinct]["election_day"] = ed_votes
                                if total_votes > precinct_totals[current_precinct].get("total_turnout", 0):
                                    precinct_totals[current_precinct]["total_turnout"] = total_votes
                        except ValueError:
                            pass
                            
    print("Found totals for", len(precinct_totals), "precincts.")
    print("Sample:", {k: precinct_totals[k] for k in list(precinct_totals)[:3]})
    
    with open("data_analysis/precinct_turnout.json", "w") as f:
        json.dump(precinct_totals, f, indent=2)

if __name__ == "__main__":
    extract_precinct_totals(sys.argv[1])
