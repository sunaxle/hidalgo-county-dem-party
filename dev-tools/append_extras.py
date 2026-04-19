import csv

MASTER_CSV = 'dev-tools/curated_precinct_chairs.csv'
EXTRA_TXT = 'dev-tools/extra_emails.txt'

existing_emails = set()
with open(MASTER_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get('Email', '').strip().lower()
        if email:
            existing_emails.add(email)

new_entries = []
with open(EXTRA_TXT, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip().strip(',')
    if not line:
        continue
    
    if '<' in line and '>' in line:
        name_part = line.split('<')[0].strip().strip('"')
        email = line.split('<')[1].replace('>', '').strip().lower()
        
        # Simple name splitting logic
        parts = name_part.split(' ')
        if len(parts) > 1:
            first_name = parts[0]
            last_name = " ".join(parts[1:])
        else:
            first_name = name_part
            last_name = ''
    else:
        first_name = "Friend"
        last_name = ''
        email = line.strip().strip('"').lower()

    if email and email not in existing_emails:
        new_entries.append({
            'FirstName': first_name,
            'LastName': last_name,
            'Email': email,
            'Tags': 'Extra_List'
        })
        existing_emails.add(email)

if new_entries:
    with open(MASTER_CSV, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['FirstName', 'LastName', 'Email', 'Tags']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for entry in new_entries:
            writer.writerow(entry)
    print(f"✅ Successfully appended {len(new_entries)} new unique people to the master CSV!")
else:
    print("No new unique emails found to append.")
