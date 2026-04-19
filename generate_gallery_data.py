import os
import urllib.parse
import json

def main():
    img_dir = "images/tmp_hcdp"
    js_file = "js/gallery_data.js"
    
    os.makedirs("js", exist_ok=True)

    files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
    files.sort() # Ensure consistent ordering

    image_data = []
    
    for f in files:
        url_path = f"images/tmp_hcdp/{urllib.parse.quote(f)}"
        title = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
        # Cap title length
        if len(title) > 30:
            title = title[:27] + "..."
            
        image_data.append({
            "url": url_path,
            "title": title,
            "desc": "Action Album"
        })

    # Exactly 125 items if we have more
    if len(image_data) > 125:
        image_data = image_data[:125]

    js_content = "export const galleryData = " + json.dumps(image_data, indent=2) + ";\n"

    with open(js_file, 'w') as file:
        file.write(js_content)

    print(f"Generated {js_file} with {len(image_data)} photos.")

if __name__ == '__main__':
    main()
