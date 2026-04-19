import json
import re
import os

cd15_exclusives = [1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 39, 40, 41, 42, 43, 44, 45, 46, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 81, 85, 87, 90, 91, 92, 96, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 121, 122, 123, 126, 127, 129, 130, 132, 137, 140, 142, 143, 144, 146, 147, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 162, 163, 166, 167, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 184, 186, 189, 190, 191, 192, 196, 199, 200, 201, 202, 206, 207, 213, 214, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 232, 235, 237, 238, 239, 242, 245, 249, 250, 251, 252, 253, 255, 259]
cd28_exclusives = [7, 9, 10, 11, 12, 26, 27, 28, 29, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 61, 63, 64, 66, 67, 78, 80, 82, 83, 86, 88, 89, 93, 94, 95, 97, 98, 99, 100, 101, 102, 103, 115, 125, 128, 131, 133, 135, 136, 138, 139, 141, 145, 148, 149, 161, 164, 165, 168, 170, 182, 183, 185, 187, 188, 193, 194, 195, 197, 198, 203, 204, 205, 208, 209, 210, 211, 212, 215, 216, 217, 218, 219, 220, 231, 233, 236, 241, 243, 244, 246, 247, 248, 254, 256, 257, 258]
splits = [8, 65, 84, 124, 134, 150, 234, 240]

def update_cd(p):
    pid = int(p['precinct'])
    if pid in splits:
        p['CD'] = "15,28"
    elif pid in cd15_exclusives:
        p['CD'] = "15"
    elif pid in cd28_exclusives:
        p['CD'] = "28"
    return p

with open('data/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

precinct_match = re.search(r"const precinctData = (\[.*?\]);", html)
uncontested_match = re.search(r"const uncontestedData = (\[.*?\]);", html)

precinct_data = json.loads(precinct_match.group(1))
uncontested_data = json.loads(uncontested_match.group(1))

# Update CD tags
precinct_data = [update_cd(p) for p in precinct_data]
uncontested_data = [update_cd(p) for p in uncontested_data]

# Calculate new averages
def calc_mean(data_list, cd):
    total_reg = 0
    total_cast = 0
    raw_turnouts = []
    
    for p in data_list:
        if cd in p['CD'].split(','):
            # some precincts have 0 registered, avoid div by zero
            if p['registered'] > 0:
                raw_turnouts.append(p['raw_turnout'])
    if len(raw_turnouts) == 0: return 0
    return sum(raw_turnouts) / len(raw_turnouts)

# all precincts
all_data = precinct_data + uncontested_data
cd15_mean = calc_mean(all_data, "15")
cd28_mean = calc_mean(all_data, "28")

print(f"New CD15 Mean: {cd15_mean:.2f}%")
print(f"New CD28 Mean: {cd28_mean:.2f}%")

# Generate new JSON
new_precinct_json = json.dumps(precinct_data)
new_uncontested_json = json.dumps(uncontested_data)

new_html = html[:precinct_match.start(1)] + new_precinct_json + html[precinct_match.end(1):uncontested_match.start(1)] + new_uncontested_json + html[uncontested_match.end(1):]

# Now string replacements for the logic and the text
new_html = new_html.replace('const cdContested = precinctData.filter(d => d.CD === cdVal);', 'const cdContested = precinctData.filter(d => String(d.CD).includes(cdVal));')
new_html = new_html.replace('const cdUncontested = uncontestedData.filter(d => d.CD === cdVal);', 'const cdUncontested = uncontestedData.filter(d => String(d.CD).includes(cdVal));')

# We need to replace the old hardcoded text "19.02%" and "19.04%" with the new means.
new_html = re.sub(r'<div class="metric-value"[^>]*>19\.02%</div>', f'<div class="metric-value" style="color: #eab308;">{cd15_mean:.2f}%</div>', new_html)
new_html = re.sub(r'<div class="metric-value"[^>]*>19\.04%</div>', f'<div class="metric-value" style="color: #eab308;">{cd28_mean:.2f}%</div>', new_html)

new_html = new_html.replace('CD15: 19.02% | CD28: 19.04%', f'CD15: {cd15_mean:.2f}% | CD28: {cd28_mean:.2f}%')

with open('data/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html successfully updated!")
