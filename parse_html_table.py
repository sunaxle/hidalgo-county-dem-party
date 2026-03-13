import json
import re

html_content_3 = """
        <tr class="directory-row" data-precinct="265" data-name="marisa d. salinas" data-role="precinct chair">
          <td><span class="pct-badge">265</span></td>
          <td class="name-cell"><strong>Marisa D. Salinas</strong></td>
          <td><span class="role-badge badge-chair">Precinct Chair</span></td>
          <td class="action-cell">
             <a href="contact.html" class="btn btn-sm btn-outline">Contact</a>
          </td>
        </tr>
        
        <tr class="directory-row" data-precinct="265" data-name="jessica n. pena" data-role="block captain">
          <td><span class="pct-badge">265</span></td>
          <td class="name-cell"><strong>Jessica N. Pena</strong></td>
          <td><span class="role-badge badge-captain">Block Captain</span></td>
          <td class="action-cell">
             <a href="contact.html" class="btn btn-sm btn-outline">Contact</a>
          </td>
        </tr>
"""

rows = html_content_3.split('tr class="directory-row"')
parsed_3 = []
for row in rows[1:]:
    pct_match = re.search(r'data-precinct="(\d+)"', row)
    name_match = re.search(r'<td class="name-cell"><strong>(.*?)</strong>', row)
    role_match = re.search(r'data-role="(.*?)"', row)
    
    if pct_match and name_match and role_match:
        parsed_3.append({
            "precinct": pct_match.group(1),
            "name": name_match.group(1).title(),
            "role": role_match.group(1).title(),
            "phone": "",
            "email": ""
        })

file_path = '/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/js/chair_data.js'
with open(file_path, 'r') as f:
    content = f.read()

# remove 'const chairDataList = ' and ';'
content_clean = content.replace("const chairDataList = ", "").replace(";", "").strip()
current_data = json.loads(content_clean)

current_names_lower = [m['name'].lower() for m in current_data]

for h in parsed_3:
    found = False
    for cName in current_names_lower:
        if h['name'].lower() in cName or cName in h['name'].lower():
            found = True
            break
    if not found:
        current_data.append(h)

# Check for duplicates by name and precinct since there might be exact dupes
unique_data = []
seen = set()
for d in current_data:
    key = f"{int(d['precinct'])}_{d['name'].lower().strip()}"
    if key not in seen:
        seen.add(key)
        unique_data.append(d)

unique_data.sort(key=lambda x: (int(x['precinct']), 0 if x['role'] == 'Precinct Chair' else 1))

with open(file_path, 'w') as f:
    f.write('const chairDataList = ')
    json.dump(unique_data, f, indent=2)
    f.write(';')

print(f"Total merged and unique: {len(unique_data)}")
