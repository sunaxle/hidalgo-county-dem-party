import csv
import re
from collections import defaultdict

file_path = "p192demodataemail20260412-6063013339.xls"
output_csv = "p192_non_voters.csv"

def clean_nulls(file_obj):
    for line in file_obj:
        yield line.replace('\0', '')

def is_hardcore_dem(row):
    # Has democratic primary history
    primary_cols = [k for k in row.keys() if k and 'Primary' in k and 'Party' in k]
    for col in primary_cols:
        if row.get(col, '').strip() == 'D':
            return True
    return False

def has_any_history(row):
    primary_cols = [k for k in row.keys() if k and 'Primary' in k and 'Party' in k]
    gen_cols = [k for k in row.keys() if k and 'General' in k]
    for col in primary_cols:
        if row.get(col, '').strip(): return True
    for col in gen_cols:
        if row.get(col, '').strip(): return True
    return False

try:
    hardcore_dem_addresses = set()
    all_rows = []
    
    with open(file_path, "r", encoding="utf-16") as f:
        reader = csv.DictReader(clean_nulls(f), delimiter='\t')
        for row in reader:
            all_rows.append(row)
            if is_hardcore_dem(row):
                address = row.get('Address', '').strip().upper()
                if address:
                    hardcore_dem_addresses.add(address)
    
    # Now process non-voters
    non_voters_list = []
    lives_with_dem_count = 0
    
    age_brackets = {
        'Under 30': 0,
        '30 to 49': 0,
        '50 to 64': 0,
        '65+': 0,
        'Unknown': 0
    }
    
    for row in all_rows:
        if not has_any_history(row):
            # It's a true non-voter
            address = row.get('Address', '').strip().upper()
            lives_with_dem = "Yes" if address in hardcore_dem_addresses else "No"
            
            if lives_with_dem == "Yes":
                lives_with_dem_count += 1
                
            # Calculate Age
            age_str = row.get('Age', '').strip()
            age_val = 0
            if age_str.isdigit():
                age_val = int(age_str)
                if age_val < 30: age_brackets['Under 30'] += 1
                elif age_val < 50: age_brackets['30 to 49'] += 1
                elif age_val < 65: age_brackets['50 to 64'] += 1
                else: age_brackets['65+'] += 1
            else:
                age_brackets['Unknown'] += 1
                
            non_voters_list.append({
                'FirstName': row.get('FirstName', ''),
                'LastName': row.get('LastName', ''),
                'Age': age_str,
                'Address': row.get('Address', ''),
                'City': row.get('City', ''),
                'Zip': row.get('Zip5', ''),
                'Lives_With_Super_Dem': lives_with_dem
            })

    # Save CSV
    with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['FirstName', 'LastName', 'Age', 'Address', 'City', 'Zip', 'Lives_With_Super_Dem'])
        writer.writeheader()
        writer.writerows(non_voters_list)
        
    print(f"Total Non-Voters Found: {len(non_voters_list)}")
    print(f"Non-Voters living with a Hardcore Dem: {lives_with_dem_count}")
    print(f"Age Brackets for Non-Voters:")
    for k, v in age_brackets.items():
        print(f"  {k}: {v}")
    print(f"Successfully saved to {output_csv}")

except Exception as e:
    print(f"Error: {e}")
