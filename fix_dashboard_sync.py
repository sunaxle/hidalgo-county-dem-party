import csv
import json
import re
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 1. Read the real VAN export XLS file
print("Reading VAN export...")
df = pd.read_csv('Elections_Data/VAN_Access_Exports/UserListExport-9534069555.xls', sep='\t', encoding='utf-16')

# 2. Extract emails
van_emails = set()
cols = [c for c in df.columns if isinstance(c, str)]

for index, row in df.iterrows():
    # Look for email column
    for col in cols:
        if 'email' in col.lower():
            val = str(row[col]).strip().lower()
            if '@' in val:
                van_emails.add(val)
    
    # Also just scan all columns for anything looking like an email as backup
    for val in row.values:
        str_val = str(val).strip().lower()
        if '@' in str_val and '.' in str_val:
            van_emails.add(str_val)

print(f"Found {len(van_emails)} unique emails in the VAN export.")

# 3. Update the chair_data.js
print("Updating chair_data.js...")
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
        chair['vanStatus'] = 'Has Access'
        updated_count += 1
    else:
        chair['vanStatus'] = 'Pending'

updated_json_str = json.dumps(chairs, indent=2, ensure_ascii=False)
updated_content = content.replace(json_str, updated_json_str)

with open('js/chair_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"Success! Updated {updated_count} precinct chairs to 'Has Access' based on the true VAN export.")
