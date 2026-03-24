import os
import glob
import re

new_community_block = """        <div class="nav-item dropdown">
          <a href="community.html" style="color: inherit; text-decoration: none; font-weight: inherit;">Community ▼</a>
          <div class="dropdown-content">
            <a href="civics_101.html" style="color: #fcd34d; font-weight: 800;">Civics 101 📚</a>
            <a href="civics_102.html" style="color: #fca5a5; font-weight: 800;">Civics 102 🎓</a>
            <a href="vdr_portal.html" style="color: #a78bfa; font-weight: 800;">VDR Portal 📝</a>
            <a href="chat.html" style="color: #2dd4bf; font-weight: 800;">Grassroots Live Chat ⚡</a>
            <a href="social_wall.html">Social Wall</a>
            <a href="county_websites.html">TX Dems</a>
            <a href="south_texas_region.html">South TX</a>
          </div>
        </div>"""

html_files = glob.glob('*.html')
updated_count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'<div class="nav-item dropdown">\s*<(?:span|a)[^>]*>Community ▼</(?:span|a)>\s*<div class="dropdown-content">.*?</div>\s*</div>'
    
    new_content = re.sub(pattern, new_community_block, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"Updated {file}")

print(f"Total files updated: {updated_count}")
