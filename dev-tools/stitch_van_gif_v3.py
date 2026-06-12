import os
from PIL import Image

images = [
    Image.open("/Users/dr3/.gemini/antigravity/brain/a63f0c29-784e-4624-bc0f-e967bbec9a33/van_dashboard_list_texas_1781228099404.png"),
    Image.open("/Users/dr3/.gemini/antigravity/brain/a63f0c29-784e-4624-bc0f-e967bbec9a33/van_map_turf_texas_1781228108389.png"),
    Image.open("/Users/dr3/.gemini/antigravity/brain/a63f0c29-784e-4624-bc0f-e967bbec9a33/minivan_mobile_texas_1781228118697.png")
]

resized = [img.resize((800, 800)) for img in images]

frames = []
for img in resized:
    for _ in range(10): # Hold each frame for 1 second total (10 * 100ms)
        frames.append(img)

output_path = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/images/van_tutorial_v3.gif"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)
print(f"Generated {output_path}")
