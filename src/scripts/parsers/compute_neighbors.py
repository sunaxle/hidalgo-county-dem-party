import json
import os


def run():
    with open("hidalgo-election-map/hidalgo_precincts.js") as f:
        content = f.read()

    # Extract JSON
    json_str = content.replace("const hidalgoPrecinctsData =", "").strip()
    if json_str.endswith(";"):
        json_str = json_str[:-1]

    data = json.loads(json_str)

    precinct_coords = {}

    for feature in data["features"]:
        props = feature["properties"]
        prec_id = props.get("PREC", props.get("PRECINCT"))
        if not prec_id:
            continue

        try:
            prec_id = str(int(prec_id))  # normalize "0170" to "170"
        except ValueError:
            pass

        geom = feature.get("geometry")
        if not geom:
            continue

        coords = []

        def extract_coords(c):
            if not c:
                return
            if isinstance(c[0], (float, int)):
                # round to 4 decimals (~11 meters at equator) to account for slight geometry mismatches
                coords.append((round(c[0], 4), round(c[1], 4)))
            else:
                for sub_c in c:
                    extract_coords(sub_c)

        extract_coords(geom["coordinates"])

        if prec_id not in precinct_coords:
            precinct_coords[prec_id] = set()
        precinct_coords[prec_id].update(coords)

    neighbors = {}

    # Filter out non-numeric precincts for sorting
    precinct_list = sorted(
        [p for p in precinct_coords.keys() if p.isdigit()], key=lambda x: int(x)
    )

    for p1 in precinct_list:
        neighbors[p1] = []
        for p2 in precinct_list:
            if p1 != p2:
                if len(precinct_coords[p1].intersection(precinct_coords[p2])) > 0:
                    neighbors[p1].append(p2)

    # Generate Markdown table
    md_lines = [
        "# Precinct Neighbors Table",
        "",
        "This table lists every precinct alongside all of its geographically touching neighboring precincts.",
        "",
        "| Precinct | Touching Precincts |",
        "| :--- | :--- |",
    ]

    for p in precinct_list:
        touching = ", ".join(neighbors[p]) if neighbors[p] else "None"
        md_lines.append(f"| **{p}** | {touching} |")

    # Write to artifact
    artifact_path = "/Users/dr3/.gemini/antigravity/brain/231c903d-42ca-4076-90f2-1c2cc6b5e1c4/artifacts/precinct_neighbors.md"
    os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
    with open(artifact_path, "w") as f:
        f.write("\n".join(md_lines))

    print(f"Generated neighbors table at {artifact_path}")


if __name__ == "__main__":
    run()
