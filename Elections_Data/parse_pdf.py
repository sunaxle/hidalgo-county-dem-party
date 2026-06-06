import PyPDF2
import re
import pandas as pd

def extract_dem_races(pdf_path):
    data = []
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            full_text = ''
            for page in reader.pages:
                full_text += page.extract_text() + '\n'
            
            # Simple heuristics to find Lieutenant Governor DEM totals and races
            matches = re.finditer(r'Lieutenant Governor - Democratic Party[\s\S]+?Precinct\s+Marcos Isaias Velez\s+Vikki Goodwin\s+Cast Votes\s+Undervotes\s+Overvotes\s+Absentee Voting Ballots Cast\s+Early Voting Ballots Cast\s+Election Day Ballots Cast\s+Total Ballots Cast\s+Registered Voters\s+Turnout Percentage\s+([0-9]{3})\s+([0-9,]+)\s+([0-9,]+)\s+([0-9,]+)', full_text)
            for m in matches:
                pct = m.group(1)
                velez = int(m.group(2).replace(',', ''))
                goodwin = int(m.group(3).replace(',', ''))
                cast = int(m.group(4).replace(',', ''))
                data.append({'Race': 'Lt Gov', 'Precinct': pct, 'Velez': velez, 'Goodwin': goodwin, 'Cast': cast})
                
            return full_text
    except Exception as e:
        return str(e)

full_text = extract_dem_races('/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/Elections_Data/Primary_Runoff_Canvas_Data_Drop/Canvass Results Report.pdf')
with open('raw_canvass.txt', 'w') as f:
    f.write(full_text)

