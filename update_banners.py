import os
import re

files = ['index.html', 'home.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the old banner
        old_banner = r'🚨 <strong>Upcoming Event:</strong> Notice of Canvass for the May 26, 2026 Primary Election on June 4th at 1 p.m\. \s*<a href="events\.html" style="color: #0f172a; text-decoration: underline; margin-left: 0\.5rem;">Click here for details & Zoom link</a>'
        new_banner = '🔥 <strong>BREAKING:</strong> The Hidalgo County Democratic Party officially launches the "Road to 500k" Voter Registration Drive! <a href="road_to_500k_press_release.html" style="color: #0f172a; text-decoration: underline; margin-left: 0.5rem; font-weight: 800;">Read the Chairman\'s Press Release</a>'
        
        content = re.sub(old_banner, new_banner, content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated banner in {file}")
