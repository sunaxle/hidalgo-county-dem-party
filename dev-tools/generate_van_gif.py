import os
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 600
frames = []

def create_frame(text, step_num):
    # Base canvas
    img = Image.new('RGB', (W, H), color=(240, 245, 250))
    draw = ImageDraw.Draw(img)
    
    # UI Header
    draw.rectangle([(0, 0), (W, 60)], fill=(15, 23, 42))
    draw.text((20, 20), "VAN | Voter Activation Network", fill=(255, 255, 255))
    
    # Sidebar
    draw.rectangle([(0, 60), (200, H)], fill=(226, 232, 240))
    draw.text((20, 100), "My List", fill=(15, 23, 42))
    draw.text((20, 140), "Create A List", fill=(37, 99, 235) if step_num==1 else (15, 23, 42))
    draw.text((20, 180), "Cut Turf", fill=(37, 99, 235) if step_num==2 else (15, 23, 42))
    draw.text((20, 220), "MiniVAN", fill=(37, 99, 235) if step_num==3 else (15, 23, 42))
    
    # Main Content Area
    content_x, content_y = 220, 80
    draw.text((content_x, content_y), text, fill=(15, 23, 42))
    
    if step_num == 1:
        # Drawing a mock table of voters
        draw.rectangle([(content_x, content_y + 40), (W - 40, H - 40)], fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        draw.rectangle([(content_x, content_y + 40), (W - 40, content_y + 70)], fill=(241, 245, 249))
        for i in range(8):
            y = content_y + 80 + (i * 40)
            draw.line([(content_x, y), (W - 40, y)], fill=(226, 232, 240), width=1)
            draw.rectangle([(content_x + 15, y + 10), (content_x + 35, y + 30)], fill=(37, 99, 235)) # Checkbox
            draw.text((content_x + 60, y + 15), f"Voter {i+1} - Strong Democrat - Consistent Voter", fill=(100, 116, 139))
    
    elif step_num == 2:
        # Map view for turf cutting
        draw.rectangle([(content_x, content_y + 40), (W - 40, H - 40)], fill=(226, 232, 240), outline=(203, 213, 225), width=2)
        # Draw streets
        draw.line([(content_x + 100, content_y + 100), (W - 100, H - 200)], fill=(255, 255, 255), width=15)
        draw.line([(content_x + 400, content_y + 50), (content_x + 200, H - 100)], fill=(255, 255, 255), width=15)
        draw.line([(content_x + 50, content_y + 250), (W - 50, content_y + 300)], fill=(255, 255, 255), width=15)
        
        # Polygon (Turf)
        poly = [(content_x + 150, content_y + 120), (content_x + 450, content_y + 150), (content_x + 350, content_y + 350), (content_x + 100, content_y + 300)]
        draw.polygon(poly, fill=(147, 197, 253), outline=(37, 99, 235), width=3)
        draw.rectangle([(content_x + 200, content_y + 200), (content_x + 320, content_y + 240)], fill=(255, 255, 255), outline=(15, 23, 42))
        draw.text((content_x + 210, content_y + 210), "Turf 1 (45 Doors)", fill=(15, 23, 42))
        
    elif step_num == 3:
        # Mobile phone mockup
        phone_x = content_x + 180
        phone_y = content_y + 40
        draw.rectangle([(phone_x, phone_y), (phone_x + 220, phone_y + 420)], fill=(15, 23, 42), outline=(100, 116, 139), width=8) # Phone body
        # Screen
        draw.rectangle([(phone_x + 10, phone_y + 30), (phone_x + 210, phone_y + 390)], fill=(255, 255, 255))
        draw.rectangle([(phone_x + 10, phone_y + 30), (phone_x + 210, phone_y + 70)], fill=(37, 99, 235))
        draw.text((phone_x + 75, phone_y + 45), "MiniVAN", fill=(255, 255, 255))
        
        draw.text((phone_x + 45, phone_y + 100), "Turf 1 Downloaded!", fill=(15, 23, 42))
        draw.text((phone_x + 75, phone_y + 130), "45 Doors", fill=(100, 116, 139))
        
        draw.rectangle([(phone_x + 30, phone_y + 180), (phone_x + 190, phone_y + 230)], fill=(37, 99, 235))
        draw.text((phone_x + 65, phone_y + 200), "Start Canvass", fill=(255, 255, 255))

    return img

# Generate frames
for i in range(8):
    frames.append(create_frame("Step 1: Create a List of Super Democrats", 1))
for i in range(8):
    frames.append(create_frame("Step 2: Cut the Map into Walkable Turf", 2))
for i in range(8):
    frames.append(create_frame("Step 3: Send Directly to MiniVAN on your Phone", 3))

output_path = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/images/van_tutorial.gif"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=800, loop=0)
print(f"Generated {output_path}")
