import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 3959.0 # miles
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# 1. Load Grocery Hubs
with open('data/hidalgo_grocery.geojson', 'r') as f:
    hubs = json.load(f)['features']

grocery_nodes = []
for h in hubs:
    lon, lat = h['geometry']['coordinates']
    grocery_nodes.append({
        'name': h['properties']['name'],
        'lat': lat,
        'lon': lon
    })

# Snap logic
print(f"Loaded {len(grocery_nodes)} HEB/Walmart anchors.")

