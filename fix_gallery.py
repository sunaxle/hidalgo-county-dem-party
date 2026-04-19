import re

html_file = "hidalgo_orbital_gallery.html"

with open(html_file, 'r') as f:
    content = f.read()

# Limit the imageData array to the first 20 items to prevent GPU memory crash
pattern = r"(const imageData = \[)(.*?)(\];)"
match = re.search(pattern, content, re.DOTALL)
if match:
    items = match.group(2).strip().split(',\n')
    # only keep first 20 items
    limited_items = ',\n'.join(items[:20])
    new_array = f"{match.group(1)}\n{limited_items}\n{match.group(3)}"
    content = content[:match.start()] + new_array + content[match.end():]

# Add error handler to TextureLoader to prevent infinite loading screen
# original:
# textureLoader.load(data.url, (texture) => {
# replacement:
# textureLoader.load(data.url, (texture) => { ... }, undefined, (err) => { loadedCount++; checkLoad(); })

texture_load_str = """
    // We create a helper function to dismiss the loader
    function checkLoaded() {
        loadedCount++;
        if(loadedCount === imageData.length) {
          const loading = document.getElementById('loading');
          loading.style.opacity = 0;
          setTimeout(() => loading.style.display = 'none', 500);
        }
    }

    // Create the photo ring
    imageData.forEach((data, i) => {
      textureLoader.load(data.url, (texture) => {
        texture.colorSpace = THREE.SRGBColorSpace;
"""
content = content.replace("    // Create the photo ring\n    imageData.forEach((data, i) => {\n      textureLoader.load(data.url, (texture) => {\n        texture.colorSpace = THREE.SRGBColorSpace;", texture_load_str)

# replace the inside of textureLoader success:
# loadedCount++;
# if(loadedCount === imageData.length) {
#   const loading = document.getElementById('loading');
#   loading.style.opacity = 0;
#   setTimeout(() => loading.style.display = 'none', 500);
# }
old_loaded_check = """        loadedCount++;
        if(loadedCount === imageData.length) {
          const loading = document.getElementById('loading');
          loading.style.opacity = 0;
          setTimeout(() => loading.style.display = 'none', 500);
        }
      });"""
new_loaded_check = """
        checkLoaded();
      },
      undefined,
      (err) => {
          console.error("Error loading texture:", data.url, err);
          checkLoaded();
      });"""
content = content.replace(old_loaded_check, new_loaded_check)

with open(html_file, 'w') as f:
    f.write(content)

print(f"Fixed {html_file}")
