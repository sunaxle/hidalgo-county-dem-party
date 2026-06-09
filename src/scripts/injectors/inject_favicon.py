import os

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"
favicon_root = '  <link rel="icon" type="image/webp" href="images/facebook_1656248751972_6946810765393131439.webp">\n'
favicon_mobile = '  <link rel="icon" type="image/webp" href="../images/facebook_1656248751972_6946810765393131439.webp">\n'

modified_count = 0

# Fix broken image ref in van_dashboard.html if present
van_dash_path = os.path.join(directory, "van_dashboard.html")
if os.path.exists(van_dash_path):
    with open(van_dash_path, 'r') as f:
        van_dash_content = f.read()
    if 'images/favicon.png' in van_dash_content:
        van_dash_content = van_dash_content.replace('images/favicon.png', 'images/facebook_1656248751972_6946810765393131439.webp')
        with open(van_dash_path, 'w') as f:
            f.write(van_dash_content)
        print("Fixed broken images/favicon.png reference in van_dashboard.html")

for root, _, files in os.walk(directory):
    if '.git' in root or '.gstack' in root or 'node_modules' in root or '.agents' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            if 'rel="icon"' in content or 'rel="shortcut icon"' in content:
                continue # already has an icon
            
            if '<head>' in content:
                unix_filepath = filepath.replace('\\', '/')
                if '/mobile/' in unix_filepath:
                    new_content = content.replace('<head>', '<head>\n' + favicon_mobile, 1)
                else:
                    new_content = content.replace('<head>', '<head>\n' + favicon_root, 1)
                
                with open(filepath, 'w') as f:
                    f.write(new_content)
                modified_count += 1

print(f"Added favicon to {modified_count} HTML files.")
