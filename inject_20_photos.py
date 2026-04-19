import os
import re
import urllib.parse
import random

def main():
    img_dir = "images/tmp_hcdp"
    html_file = "hidalgo_orbital_gallery.html"

    # List all files
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
    
    # We want exactly 20. Include the 5 from earlier to be safe, then random others.
    # The 5 we used were:
    # 'Call for Volunteers - 1000 calls.jpeg',
    # 'Purple Geometric Donate Today Fundraising Goal Instagram Story.jpeg'
    # Plus blockwalk, community, meeting.
    
    safe_picks = [f for f in files if "for Volunteers" in f or "Purple Geometric" in f or "Insta" in f or "Story" in f]
    other_picks = [f for f in files if f not in safe_picks]
    
    selected = safe_picks + other_picks
    selected = selected[:17] # We take 17 from tmp
    
    image_data_strs = []
    
    # Add the 3 core ones
    image_data_strs.append("      { url: 'images/blockwalk.jpg', title: 'Blockwalking', desc: 'Connecting with voters' }")
    image_data_strs.append("      { url: 'images/community.jpg', title: 'Community Outreach', desc: 'Building relationships' }")
    image_data_strs.append("      { url: 'images/meeting.jpg', title: 'Strategy Meeting', desc: 'Planning the road ahead' }")
    
    for f in selected:
        url_path = f"images/tmp_hcdp/{urllib.parse.quote(f)}"
        title = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
        image_data_strs.append(f"      {{ url: '{url_path}', title: '{title}', desc: 'Action Album' }}")

    image_data_js = "[\n" + ",\n".join(image_data_strs) + "\n    ]"

    # Read original HTML
    with open(html_file, 'r') as file:
        content = file.read()

    # Regex to find and replace the imageData array
    pattern = r"const imageData = \[.*?\];"
    replacement = f"const imageData = {image_data_js};"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write it back
    with open(html_file, 'w') as file:
        file.write(new_content)

    print(f"Injected {len(image_data_strs)} photos into the gallery.")

if __name__ == '__main__':
    main()
