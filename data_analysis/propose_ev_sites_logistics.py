import json
import math
import random

def haversine(lat1, lon1, lat2, lon2):
    R = 3959.0 # miles
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# 1. Load the original precinct dataset to get Deserts
with open('data_analysis/hidalgo_analysis_precincts.geojson', 'r') as f:
    geojson = json.load(f)

# 2. Extract precinct centroids and registered voters for K-Means weighting
precinct_points = []
for feature in geojson['features']:
    props = feature['properties']
    if 'distance_to_ev' not in props or props['distance_to_ev'] is None:
        continue
        
    voters = props.get('registered_voters', 0)
    if voters is None: voters = 0
    # Provide a baseline weight for all precincts, heavy focus on dense deserts
    voters_weight = max(voters, 10)
        
    geom = feature['geometry']
    if geom['type'] == 'Polygon':
        coords = geom['coordinates'][0]
        lon = sum(p[0] for p in coords) / len(coords)
        lat = sum(p[1] for p in coords) / len(coords)
        precinct_points.append({'lat': lat, 'lon': lon, 'weight': voters_weight, 'desert_severity': props['distance_to_ev'] * voters_weight})

# A simple Weighted K-Means
k = 10
random.seed(42)
centroids = random.sample(precinct_points, k)
centroids = [{'lat': c['lat'], 'lon': c['lon']} for c in centroids]

for _ in range(15): # 15 iterations is usually enough
    clusters = [[] for _ in range(k)]
    for p in precinct_points:
        distances = [haversine(p['lat'], p['lon'], c['lat'], c['lon']) for c in centroids]
        closest_idx = distances.index(min(distances))
        clusters[closest_idx].append(p)
    
    for i in range(k):
        if not clusters[i]: continue
        total_weight = sum(p['weight'] for p in clusters[i])
        new_lat = sum(p['lat'] * p['weight'] for p in clusters[i]) / total_weight
        new_lon = sum(p['lon'] * p['weight'] for p in clusters[i]) / total_weight
        centroids[i] = {'lat': new_lat, 'lon': new_lon}

# 3. Load the Grocery Hubs for Logistics Snapping
with open('data/hidalgo_grocery.geojson', 'r') as f:
    hubs = json.load(f)['features']

grocery_nodes = []
for h in hubs:
    lon, lat = h['geometry']['coordinates']
    grocery_nodes.append({'name': h['properties']['name'], 'lat': lat, 'lon': lon})

# 4. Snap centroids to nearest Commerce Hub if within 5 miles
snapped_centroids = []
for center in centroids:
    distances_to_hubs = [(haversine(center['lat'], center['lon'], g['lat'], g['lon']), g) for g in grocery_nodes]
    distances_to_hubs.sort(key=lambda x: x[0])
    closest_dist, closest_hub = distances_to_hubs[0]
    
    # If the mathematical center of the desert is within 5 miles of an HEB/Walmart, move the site to the HEB
    if closest_dist <= 5.0:
        snapped_centroids.append({
            'lat': closest_hub['lat'], 
            'lon': closest_hub['lon'], 
            'is_snapped': True, 
            'snapped_to': closest_hub['name'],
            'drift_distance': closest_dist
        })
    else:
        # Otherwise keep the mathematical site
        snapped_centroids.append({
            'lat': center['lat'], 
            'lon': center['lon'], 
            'is_snapped': False, 
            'snapped_to': 'None',
            'drift_distance': 0
        })

# 5. Inject the snapped distances into the GeoJSON
for feature in geojson['features']:
    geom = feature['geometry']
    if geom['type'] == 'Polygon':
        coords = geom['coordinates'][0]
        lon = sum(p[0] for p in coords) / len(coords)
        lat = sum(p[1] for p in coords) / len(coords)
        
        sim_distances = [haversine(lat, lon, sc['lat'], sc['lon']) for sc in snapped_centroids]
        closest_sim_dist = min(sim_distances)
        
        # We assume the voter will go to the real EV site OR the newly simulated one if closer
        current_ev = feature['properties'].get('distance_to_ev', 999)
        if current_ev is None: current_ev = 999
        feature['properties']['simulated_logistics_distance'] = min(closest_sim_dist, current_ev)

# Save output
with open('data_analysis/hidalgo_logistics_precincts.geojson', 'w') as f:
    json.dump(geojson, f)

# Save the snapped sites for rendering
with open('data_analysis/logistics_sites.json', 'w') as f:
    json.dump(snapped_centroids, f)

snapped_count = sum(1 for c in snapped_centroids if c['is_snapped'])
print(f"Generated {k} sites. {snapped_count} sites successfully snapped to Commerce Hubs!")
