import pandas as pd
import re

df = pd.read_excel('temp_districts/PLANC2333_r110_VTD24G.xls', header=None)

current_district = None
current_county = None

hidalgo_districts = {}

for i, row in df.iterrows():
    row_list = row.dropna().tolist()
    if not row_list:
        continue
        
    first_cell = str(row_list[0]).strip()
    
    # Catch DISTRICT X
    if first_cell.startswith('DISTRICT '):
        match = re.search(r'DISTRICT\s+(\d+)', first_cell)
        if match:
            current_district = match.group(1)
            if current_district not in hidalgo_districts:
                hidalgo_districts[current_district] = []
        continue
        
    # Catch County header
    # Looks like "Bowie (76 %)" or "Hidalgo"
    # Wait, they are usually only 1 item in the row (len == 1)
    if len(row_list) == 1 and not first_cell.startswith('VAP:'):
        if first_cell.startswith('Hidalgo'):
            current_county = 'Hidalgo'
        elif first_cell == 'CONGRESSIONAL DISTRICTS - PLANC2333' or first_cell.startswith('Page '):
            pass
        else:
            current_county = first_cell.split('(')[0].strip()
        continue
        
    # Catch VTD row
    if current_county == 'Hidalgo':
        # VTD row usually has 'Total:' somewhere, or starts with a precinct number
        # e.g., ['0007', 'Total:', 6117...] or ['0013', '0.0%', 'Total:'...]
        if 'Total:' in row_list:
            vtd = first_cell
            # Remove any asterisks
            vtd = vtd.replace('*', '').strip()
            # If it's something like "0007", we might want to cast it to int later
            if vtd != 'VAP:' and vtd != 'Hidalgo':
                hidalgo_districts[current_district].append(vtd)
                
# Let's print out what we found
for dist, vtds in hidalgo_districts.items():
    if vtds:
        # Strip leading zeros for easier reading
        clean_vtds = [str(int(v)) if v.isdigit() else v for v in vtds]
        # Sort them numerically if possible
        clean_vtds.sort(key=lambda x: int(x) if x.isdigit() else x)
        print(f"CD {dist} Precincts (Count: {len(clean_vtds)}):")
        print(", ".join(clean_vtds))
        print()
