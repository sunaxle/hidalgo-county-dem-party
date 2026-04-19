import os
import re
import urllib.parse

def main():
    img_dir = "images/tmp_hcdp"
    html_file = "hidalgo_orbital_gallery.html"

    # List all files
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
    
    # Generate imageData array elements
    image_data_strs = []
    for f in files:
        url_path = f"images/tmp_hcdp/{urllib.parse.quote(f)}"
        # Simple title generation from filename, removing extension and hyphens/underscores
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

    print(f"Injected {len(files)} photos into the gallery.")

if __name__ == '__main__':
    main()
