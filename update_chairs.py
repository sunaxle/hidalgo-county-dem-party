import json
import re

# 1. Parse the TSV
new_chairs = []
with open("new_chairs.tsv", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        cols = line.split("\t")
        if len(cols) < 3:
            continue
            
        status = cols[0].strip().lower()
        precinct = cols[1].strip()
        last_name = cols[2].strip()
        first_name = cols[3].strip() if len(cols) > 3 else ""
        phone = cols[4].strip() if len(cols) > 4 else ""
        email = cols[5].strip() if len(cols) > 5 else ""
        # Format name
        name = f"{first_name} {last_name}".strip()
        # Clean phone
        phone = re.sub(r"[^\d]", "", phone)
        
        role = "Precinct Chair"
        if status == "runoff":
            role = "Precinct Chair (Runoff)"
            
        new_chairs.append({
            "precinct": precinct,
            "name": name,
            "role": role,
            "phone": phone,
            "email": email
        })

# 2. Extract Existing Block Captains from chair_data.js
with open("js/chair_data.js", "r") as f:
    js_content = f.read()

match = re.search(r"const chairDataList2026 = (\[.*?\]);", js_content, re.DOTALL)
if not match:
    print("Could not find chairDataList2026 array.")
    exit(1)

old_data_json = match.group(1)
try:
    old_data = json.loads(old_data_json)
except json.JSONDecodeError as e:
    print("JSON Decode Error", e)
    exit(1)

block_captains = [c for c in old_data if c.get("role") == "Block Captain"]

# 3. Combine and replace
combined_data = new_chairs + block_captains

# Sort by precinct number (just for neatness)
combined_data.sort(key=lambda x: int(x["precinct"]) if x["precinct"].isdigit() else 999)

new_json_str = json.dumps(combined_data, indent=2)

new_js_content = js_content[:match.start(1)] + new_json_str + js_content[match.end(1):]

with open("js/chair_data.js", "w") as f:
    f.write(new_js_content)

print(f"Successfully processed {len(new_chairs)} chairs and kept {len(block_captains)} block captains. Total: {len(combined_data)}")
