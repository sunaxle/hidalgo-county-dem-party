import json
import re
import os

cd15_exclusives = [1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 39, 40, 41, 42, 43, 44, 45, 46, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 81, 85, 87, 90, 91, 92, 96, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 121, 122, 123, 126, 127, 129, 130, 132, 137, 140, 142, 143, 144, 146, 147, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 162, 163, 166, 167, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 184, 186, 189, 190, 191, 192, 196, 199, 200, 201, 202, 206, 207, 213, 214, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 232, 235, 237, 238, 239, 242, 245, 249, 250, 251, 252, 253, 255, 259]

cd28_exclusives = [7, 9, 10, 11, 12, 26, 27, 28, 29, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 61, 63, 64, 66, 67, 78, 80, 82, 83, 86, 88, 89, 93, 94, 95, 97, 98, 99, 100, 101, 102, 103, 115, 125, 128, 131, 133, 135, 136, 138, 139, 141, 145, 148, 149, 161, 164, 165, 168, 170, 182, 183, 185, 187, 188, 193, 194, 195, 197, 198, 203, 204, 205, 208, 209, 210, 211, 212, 215, 216, 217, 218, 219, 220, 231, 233, 236, 241, 243, 244, 246, 247, 248, 254, 256, 257, 258]

splits = [8, 65, 84, 124, 134, 150, 234, 240]

cd15_full = sorted(list(set(cd15_exclusives + splits)))
cd28_full = sorted(list(set(cd28_exclusives + splits)))

# 1. Update data/cd15_precincts.json
with open('data/cd15_precincts.json', 'w') as f:
    json.dump(cd15_full, f, separators=(',', ':'))

# 2. Update data/cd28_precincts.json
with open('data/cd28_precincts.json', 'w') as f:
    json.dump(cd28_full, f, separators=(',', ':'))

# 3. Update data/index.html
def update_district(p):
    pid = int(p['precinct'])
    if pid in splits:
        p['CD'] = "SPLIT" # Or assign to one for math purposes? The dashboard has a toggle button for 15 and 28. If we assign "15|28", the map filter might break if it expects exact equality. Let's look at the JS.
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

# Check how precinct 8 was mapped previously to know if "SPLIT" is a new concept or not.
p8_old_cd = next((p['CD'] for p in uncontested_data if p['precinct'] == "8"), None)
print("Old CD for split precinct 8:", p8_old_cd)
