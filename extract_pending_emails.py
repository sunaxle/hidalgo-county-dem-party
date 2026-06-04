import json
import re

with open('js/chair_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const chairDataList2026 = (\[.*?\]);', content, re.DOTALL)
json_str = match.group(1)
chairs = json.loads(json_str)

pending_emails = []
for chair in chairs:
    email = chair.get('email', '').strip()
    status = chair.get('vanStatus', 'Pending')
    if email and status == 'Pending':
        pending_emails.append(f"{chair.get('name')}, {email}, {chair.get('precinct')}")

with open('pending_van_emails.csv', 'w', encoding='utf-8') as f:
    f.write("Name,Email,Precinct\n")
    for row in pending_emails:
        f.write(row + "\n")

print(f"Extracted {len(pending_emails)} pending chairs with emails.")
