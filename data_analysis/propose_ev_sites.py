import json
import math
import random
from collections import defaultdict

def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # Radius of earth in miles
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_centroid(geom):
    coords = []
    if geom['type'] == 'Polygon':
        for ring in geom['coordinates']:
            coords.extend(ring)
    elif geom['type'] == 'MultiPolygon':
        for poly in geom['coordinates']:
            for ring in poly:
                coords.extend(ring)
    if not coords: return 0,0
    avg_lon = sum(c[0] for c in coords)/len(coords)
    avg_lat = sum(c[1] for c in coords)/len(coords)
    return avg_lon, avg_lat

print("Loading data...")
with open('data_analysis/hidalgo_analysis_precincts.geojson') as f:
    precincts = json.load(f)

with open('hidalgo-election-map/polling_locations.geojson') as f:
    ev_sites = json.load(f)

# Extract existing EV site coordinates
existing_ev_coords = []
for site in ev_sites['features']:
    lon, lat = site['geometry']['coordinates']
    existing_ev_coords.append((lon, lat))

# Filter target precincts (>2.3 miles penalty and has RV)
targets = []
for f in precincts['features']:
    props = f['properties']
    dist = props.get('distance_to_ev', 0)
    rv = props.get('registered_voters', 0)
    if dist > 2.3 and rv > 0:
        lon, lat = get_centroid(f['geometry'])
        targets.append({'lon': lon, 'lat': lat, 'weight': rv, 'precinct': props})

print(f"Running Weighted K-Means on {len(targets)} high-friction precincts to find 10 new sites...")

# 1. Initialize 10 random centroids from heavy targets
targets.sort(key=lambda x: x['weight'], reverse=True)
centroids = [{'lon': t['lon'], 'lat': t['lat']} for t in targets[:10]]

# 2. Iterate
k = 10
for iteration in range(50):
    clusters = defaultdict(list)
    # Assign to nearest centroid
    for t in targets:
        distances = [haversine(t['lon'], t['lat'], c['lon'], c['lat']) for c in centroids]
        min_idx = distances.index(min(distances))
        clusters[min_idx].append(t)
    
    # Update centroids
    moved = 0
    for i in range(k):
        if not clusters[i]: continue
        total_weight = sum(t['weight'] for t in clusters[i])
        new_lon = sum(t['lon'] * t['weight'] for t in clusters[i]) / total_weight
        new_lat = sum(t['lat'] * t['weight'] for t in clusters[i]) / total_weight
        
        if abs(new_lon - centroids[i]['lon']) > 0.0001 or abs(new_lat - centroids[i]['lat']) > 0.0001:
            moved += 1
            
        centroids[i]['lon'] = new_lon
        centroids[i]['lat'] = new_lat
        
    if moved == 0:
        print(f"Algorithm converged at iteration {iteration}")
        break

# Setup Proposed Sites GeoJSON
proposed_features = []
for idx, c in enumerate(centroids):
    proposed_features.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [c['lon'], c['lat']]},
        "properties": {"name": f"Proposed Early Voting Site #{idx+1}"}
    })

with open("data_analysis/proposed_ev_sites.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": proposed_features}, f)

print("Updating Master Precinct file with simulated metrics...")
for f in precincts['features']:
    props = f['properties']
    lon, lat = get_centroid(f['geometry'])
    rv = props.get('registered_voters', 0)
    
    # Find nearest site including new ones
    min_dist = props.get('distance_to_ev', 999)
    for c in centroids:
        d = haversine(lon, lat, c['lon'], c['lat'])
        if d < min_dist:
            min_dist = d
            
    props['simulated_distance'] = min_dist
    props['simulated_penalty'] = min_dist * rv

with open("data_analysis/hidalgo_analysis_precincts.geojson", "w") as f:
    json.dump(precincts, f)

print("Simulation Engine Successfully Generated.")
