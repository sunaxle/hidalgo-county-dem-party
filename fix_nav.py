import glob
import re

html_files = glob.glob('*.html')
count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_content = content
    
    # Fix broken community link
    content = re.sub(
        r'<div class="nav-item dropdown">\s*style="color: inherit; text-decoration: none; font-weight: inherit;">Community ▼</a>',
        r'<div class="nav-item dropdown">\n          <a href="community.html" style="color: inherit; text-decoration: none; font-weight: inherit;">Community ▼</a>',
        content
    )
    
    if old_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
            
print(f"Fixed community html bug in {count} active views.")
