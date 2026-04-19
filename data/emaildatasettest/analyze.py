import csv

file_path = "p192demodataemail20260412-6063013339.xls"

def clean_nulls(file_obj):
    for line in file_obj:
        yield line.replace('\0', '')

try:
    with open(file_path, "r", encoding="utf-16") as f:
        reader = csv.DictReader(clean_nulls(f), delimiter='\t')
        
        total_rows = 0
        dem_primary = 0
        rep_primary = 0
        gen_voters = 0
        non_voters = 0
        
        for row in reader:
            total_rows += 1
            has_dem = False
            has_rep = False
            has_gen = False
            has_any = False
            
            # Check Primary History
            primary_party_cols = [k for k in row.keys() if k and 'Primary' in k and 'Party' in k]
            for col in primary_party_cols:
                val = row.get(col, '').strip()
                if val == 'D': has_dem = True
                if val == 'R': has_rep = True
                if val: has_any = True
                
            # Check General History
            gen_cols = [k for k in row.keys() if k and 'General' in k]
            for col in gen_cols:
                if row.get(col, '').strip():
                    has_gen = True
                    has_any = True
            
            if has_dem: dem_primary += 1
            if has_rep: rep_primary += 1
            if has_gen: gen_voters += 1
            if not has_any: non_voters += 1
            
        print(f"Total Rows: {total_rows}")
        print(f"Dem Primary History: {dem_primary}")
        print(f"Rep Primary History: {rep_primary}")
        print(f"General Election Turnout History: {gen_voters}")
        print(f"No Voting History (True Non-Voters): {non_voters}")

except Exception as e:
    print(f"Error: {e}")
