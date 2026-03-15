import os
import json
import re

def main():
    city_file = "Demographic data requests/city and precincts .xls"
    js_file = "js/precinct_mapping_data.js"
    
    # 1. Read the UTF-16 HTML file
    with open(city_file, 'r', encoding='utf-16') as f:
        html = f.read()
        
    # Find all rows looking like:
    # <td style="mso-number-format:'\@'">Alamo</td>
    # <td style="mso-number-format:'\@'">0044</td>
    
    # Let's extract td blocks
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE)
    
    city_map = {}
    
    for row in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
        if len(tds) >= 2:
            city_raw = tds[0].strip()
            pct_raw = tds[1].strip()
            
            # Skip header or totals if they get caught
            if city_raw.lower() == 'city' or 'total' in city_raw.lower():
                continue
                
            city_map[pct_raw] = city_raw
            
    print(f"Extracted {len(city_map)} precinct-to-city mappings.")
    
    # 2. Update precinct_mapping_data.js
    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()
        
    json_str = js_content.replace('const precinctDistricts = ', '').replace(';', '').strip()
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Error decoding JS JSON:", e)
        return
        
    updated_count = 0
    
    for item in data:
        pct = item.get("PRECINCT")
        if pct in city_map:
            item["CITY"] = city_map[pct]
            updated_count += 1
        elif pct and pct.isdigit():
            # If a precinct has no explicit city, we can label it "Rural / Unincorporated" or "None"
            # But let's leave it out or mark "Rural" if it's not in the list.
            item["CITY"] = "Rural"
            
    # Write back
    new_js = "const precinctDistricts = " + json.dumps(data, indent=4) + ";\n"
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(new_js)
        
    print(f"Successfully updated {updated_count} out of {len(data)} precincts in precinct_mapping_data.js")

if __name__ == "__main__":
    main()
