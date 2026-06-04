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
chairs = json.loads(json_str)

# Reset all chairs to Pending
for chair in chairs:
    chair['vanStatus'] = "Pending"

# Serialize back to JSON
updated_json_str = json.dumps(chairs, indent=2, ensure_ascii=False)

# Replace in original content
updated_content = content.replace(json_str, updated_json_str)

# Write back to file
with open('js/chair_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"Successfully reset all {len(chairs)} precinct chairs to 'Pending' status.")
