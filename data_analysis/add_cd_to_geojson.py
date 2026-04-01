import json
import re

# 1. Read the raw HTML to extract the precinctData arrays
html_path = "data/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_text = f.read()

# Very basic regex to grab the two JSON arrays
m1 = re.search(r'const precinctData = (\[.*?\]);', html_text)
m2 = re.search(r'const uncontestedData = (\[.*?\]);', html_text)

precinct_cd_map = {}

if m1 and m2:
    data1 = json.loads(m1.group(1))
    data2 = json.loads(m2.group(1))
    
    for item in data1:
        precinct_cd_map[str(item.get("precinct", ""))] = str(item.get("CD", "Unknown"))
    for item in data2:
        precinct_cd_map[str(item.get("precinct", ""))] = str(item.get("CD", "Unknown"))

# 2. Inject into GeoJSON
geo_path = "data_analysis/hidalgo_analysis_precincts.geojson"
with open(geo_path, "r", encoding="utf-8") as f:
    geojson = json.load(f)

for feature in geojson['features']:
    props = feature['properties']
    p_num = str(props.get('PCT', props.get('PREC', '')))
    props['CD'] = precinct_cd_map.get(p_num, "Unknown")

with open(geo_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f)

print("CD lines successfully injected into geojson!")
