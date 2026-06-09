import json
import re

with open("js/chair_data.js") as f:
    data = f.read()
    # Strip javascript variable declaration
    data = re.sub(r"^const\s+precinctChairs\s*=\s*", "", data)
    data = re.sub(r";\s*$", "", data)

    try:
        chairs = json.loads(data)
        targets = ["13", "14", "108", "109", "151", "152"]
        for c in chairs:
            pct = str(c.get("precinct", ""))
            if pct in targets:
                print(
                    f"Precinct {pct}: {c.get('first_name')} {c.get('last_name')} - {c.get('email')}"
                )
    except Exception as e:
        print("JSON parse error:", e)
