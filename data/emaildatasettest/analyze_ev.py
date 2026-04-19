import csv

file_path = "p192demodataemail20260412-6063013339.xls"

def clean_nulls(file_obj):
    for line in file_obj:
        yield line.replace('\0', '')

try:
    with open(file_path, "r", encoding="utf-16") as f:
        reader = csv.DictReader(clean_nulls(f), delimiter='\t')
        
        early_voters = 0
        polls_voters = 0
        mail_voters = 0
        
        for row in reader:
            g24 = row.get('General24', '').strip().upper()
            if g24 == 'E':
                early_voters += 1
            elif g24 == 'P':
                polls_voters += 1
            elif g24 == 'A' or g24 == 'M': # Absentee / Mail
                mail_voters += 1
                
        print(f"2024 General Early Voters (E): {early_voters}")
        print(f"2024 General Election Day Voters (P): {polls_voters}")
        print(f"2024 General Mail Voters: {mail_voters}")

except Exception as e:
    print(f"Error: {e}")
