import csv

# Read old chairs
old_chairs = {}
with open('HCDP_Precinct_Contacts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row['email'].strip().lower()
        if email:
            old_chairs[email] = row

# Read new chairs from markdown table
new_chairs = {}
md_path = '/Users/dr3/.gemini/antigravity/brain/eac05406-9dfc-48ad-b10e-f032fa7b43e5/2026_2028_precinct_chairs.md'
with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('|') and 'Status' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 8:
                precinct = parts[2]
                last = parts[3]
                first = parts[4]
                phone = parts[5]
                email = parts[6].strip().lower()
                if email:
                    new_chairs[email] = {
                        'precinct': precinct,
                        'first': first,
                        'last': last,
                        'phone': phone,
                        'email': parts[6].strip()
                    }

old_emails = set(old_chairs.keys())
new_emails = set(new_chairs.keys())

staying_on = old_emails.intersection(new_emails)
leaving = old_emails - new_emails
brand_new = new_emails - old_emails
all_unique_emails = old_emails.union(new_emails)

print(f"Old Chairs Count (with emails): {len(old_emails)}")
print(f"New Chairs Count (with emails): {len(new_emails)}")
print(f"Chairs Staying On: {len(staying_on)}")
print(f"Chairs Leaving: {len(leaving)}")
print(f"Brand New Chairs: {len(brand_new)}")
print(f"Total Unique Emails for 'Passing the Torch' Blast: {len(all_unique_emails)}")

combined_list = []
combined_list.append(['Type', 'Precinct', 'First Name', 'Last Name', 'Email', 'Phone'])

for email in all_unique_emails:
    if email in new_chairs:
        row = new_chairs[email]
        ctype = 'Staying On' if email in staying_on else 'Brand New'
        combined_list.append([ctype, row['precinct'], row['first'], row['last'], row['email'], row['phone']])
    else:
        row = old_chairs[email]
        combined_list.append(['Leaving', row['precinct'], row['first'], row['last'], row['email'], row['phone']])

with open('Passing_the_Torch_List.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(combined_list)

print("Saved combined list to Passing_the_Torch_List.csv")
