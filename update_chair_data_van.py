import json
import re

# Read the file
with open('js/chair_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON array string
match = re.search(r'const chairDataList2026 = (\[.*?\]);', content, re.DOTALL)
if not match:
    print("Could not find chairDataList2026 array.")
    exit(1)

json_str = match.group(1)

# Parse the JSON
try:
    chairs = json.loads(json_str)
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    exit(1)

# Update each chair
for chair in chairs:
    if 'vanStatus' not in chair:
        chair['vanStatus'] = "Pending"
    if 'contactLog' not in chair:
        chair['contactLog'] = []

# Serialize back to JSON
updated_json_str = json.dumps(chairs, indent=2, ensure_ascii=False)

# Replace in original content
updated_content = content.replace(json_str, updated_json_str)

# Write back to file
with open('js/chair_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"Successfully added VAN tracking fields to {len(chairs)} precinct chairs/captains.")
