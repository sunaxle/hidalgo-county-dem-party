import csv

in_path = 'data/old volunteer list 24-25.csv'
out_path = 'data/prepped_old_volunteer_list.csv'

with open(in_path, 'r', encoding='utf-8') as f_in, open(out_path, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.DictReader(f_in)
    writer = csv.DictWriter(f_out, fieldnames=['first_name', 'last_name', 'email', 'phone', 'zipcode'])
    writer.writeheader()
    for row in reader:
        writer.writerow({
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'phone': row['phone'],
            'zipcode': row['zipcode']
        })

print(f"Extraction complete. Target compiled to {out_path}")
