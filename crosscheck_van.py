import csv
import json
import re
import glob

# Find the newest CSV file in the current directory
csv_files = glob.glob('*.csv')
if not csv_files:
    print("Error: Could not find any VAN export CSV files in this directory.")
    print("Please download the 'Users who have VAN Access' list from VAN as a CSV and drop it in this folder.")
    exit(1)

latest_csv = max(csv_files, key=lambda x: x)
print(f"Reading VAN export data from: {latest_csv}")

van_emails = set()
with open(latest_csv, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        for col in row:
            if '@' in col:
                van_emails.add(col.strip().lower())

print(f"Found {len(van_emails)} unique emails in the VAN export.")

# Read the chair_data.js
with open('js/chair_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const chairDataList2026 = (\[.*?\]);', content, re.DOTALL)
if not match:
    print("Could not find chairDataList2026 array.")
    exit(1)

json_str = match.group(1)
chairs = json.loads(json_str)

updated_count = 0
for chair in chairs:
    email = chair.get('email', '').strip().lower()
    if email and email in van_emails:
        if chair.get('vanStatus') != 'Has Access':
            chair['vanStatus'] = 'Has Access'
            updated_count += 1

updated_json_str = json.dumps(chairs, indent=2, ensure_ascii=False)
updated_content = content.replace(json_str, updated_json_str)

with open('js/chair_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"Success! Automatically updated {updated_count} precinct chairs to 'Has Access' based on the VAN CSV.")
