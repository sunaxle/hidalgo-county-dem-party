import csv

file_path = "p192demodataemail20260412-6063013339.xls"

def clean_nulls(file_obj):
    for line in file_obj:
        yield line.replace('\0', '')

try:
    with open(file_path, "r", encoding="utf-16") as f:
        reader = csv.DictReader(clean_nulls(f), delimiter='\t')
        
        last_primary = 0
        last_general = 0
        
        for row in reader:
            # Check 2024 Primary (Primary24Party or Primary24 or just any Primary in 24)
            # VAN usually exports Primary24 and Primary24Party depending on selections
            p24 = row.get('Primary24Party', '').strip()
            if not p24: p24 = row.get('Primary24', '').strip()
            
            if p24:
                last_primary += 1
                
            # Check 2024 General
            g24 = row.get('General24', '').strip()
            if g24:
                last_general += 1
            
        print(f"Voted in Last Primary (2024): {last_primary}")
        print(f"Voted in Last General (2024): {last_general}")

except Exception as e:
    print(f"Error: {e}")
