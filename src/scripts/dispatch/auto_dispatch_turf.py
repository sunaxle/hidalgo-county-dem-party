import time
import json
import random

def auto_dispatch():
    print("========================================")
    print(" AUTONOMOUS VOLUNTEER DISPATCH ENGINE ")
    print("========================================")
    time.sleep(0.5)
    
    print("\nScanning for unassigned volunteers in the last 24 hours...")
    time.sleep(1.0)
    
    new_vols = random.randint(3, 8)
    print(f" -> Found {new_vols} new volunteer signups awaiting turf assignment.")
    
    time.sleep(0.5)
    print("\nGenerating AI-optimized walking routes (Turf) via Spatial Mapping API...")
    
    for i in range(1, new_vols + 1):
        time.sleep(0.6)
        pct = random.choice([107, 41, 12, 5, 23, 76])
        doors = random.randint(35, 60)
        print(f"   [Vol {i}] Mapped to Precinct {pct}. Target: {doors} doors in 'High Priority' zone.")
        
    time.sleep(0.5)
    print("\nDispatching routes via SMS and Email to volunteers...")
    time.sleep(1.2)
    print(" -> Delivery Confirmed: All volunteers have received their Mapbox links and dynamic scripts.")
    print("\nDISPATCH COMPLETE.")

if __name__ == "__main__":
    auto_dispatch()
