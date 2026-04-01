import json
import math
import sys

# Haversine formula to calculate straight-line distance between coords in miles
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_centroid(coords):
    # Flatten the coords array (assumes MultiPolygon or Polygon)
    points = []
    def extract_points(arr):
        if isinstance(arr[0], float) or isinstance(arr[0], int):
            points.append(arr)
        else:
            for item in arr:
                extract_points(item)
    extract_points(coords)
    
    avg_lon = sum(p[0] for p in points) / len(points)
    avg_lat = sum(p[1] for p in points) / len(points)
    return avg_lat, avg_lon

def calculate_drive_times(precinct_file, ev_locations_file, output_file):
    print("Calculating proxy drive distances...")
    
    with open(precinct_file, 'r') as f:
        precincts = json.load(f)
        
    with open(ev_locations_file, 'r') as f:
        ev_sites = json.load(f)
        
    # Read our generated turnout data
    try:
        with open("data_analysis/precinct_turnout.json", "r") as f:
            turnout_data = json.load(f)
    except FileNotFoundError:
        turnout_data = {}
        
    for feature in precincts['features']:
        # Get centroid
        try:
            p_lat, p_lon = calculate_centroid(feature['geometry']['coordinates'])
        except Exception:
            continue
            
        shortest_distance = float('inf')
        nearest_ev_site = None
        
        for ev in ev_sites['features']:
            try:
                ev_lon = ev['geometry']['coordinates'][0]
                ev_lat = ev['geometry']['coordinates'][1]
                
                dist = haversine(p_lat, p_lon, ev_lat, ev_lon)
                if dist < shortest_distance:
                    shortest_distance = dist
                    nearest_ev_site = ev['properties'].get('name', 'Unknown')
            except Exception:
                pass
                
        # Append data to precinct
        feature['properties']['nearest_ev_site'] = nearest_ev_site
        feature['properties']['distance_to_ev'] = shortest_distance
        
        # Add turnout data
        raw_p_num = str(feature['properties'].get('PCT', feature['properties'].get('PREC', '')))
        try:
            p_num = str(int(raw_p_num))
        except ValueError:
            p_num = raw_p_num
            
        if p_num in turnout_data:
            feature['properties']['early_voting_turnout_2026'] = turnout_data[p_num].get('early_voting', 0)
            feature['properties']['registered_voters'] = turnout_data[p_num].get('registered_voters', 0)
            rv = feature['properties']['registered_voters']
            dist = feature['properties']['distance_to_ev']
            feature['properties']['collective_mileage_penalty'] = rv * dist
        
    with open(output_file, 'w') as f:
        json.dump(precincts, f)
        
    print(f"Generated complete analysis file: {output_file}")
    
if __name__ == "__main__":
    calculate_drive_times(
        "hidalgo-election-map/hidalgo_precincts.geojson",
        "hidalgo-election-map/polling_locations.geojson", 
        "data_analysis/hidalgo_analysis_precincts.geojson"
    )
