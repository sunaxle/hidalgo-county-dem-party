import os
import re

def process_files():
    with open('state_party_clone.html', 'r', encoding='utf-8') as f:
        master_html = f.read()

    nav_match = re.search(r'<nav class="tx-clone-nav">.*?</nav>\s*<div class="tx-clone-nav-accent-bar"></div>', master_html, re.DOTALL)
    footer_match = re.search(r'<footer class="tx-clone-footer">.*?</footer>', master_html, re.DOTALL)

    if not nav_match or not footer_match:
        print("Could not find nav or footer in master file.")
        return

    nav_str = nav_match.group(0).replace('\\', '\\\\')
    footer_str = footer_match.group(0).replace('\\', '\\\\')

    head_additions = """
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Inter:wght@400;600;800&family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="css/state_party_clone.css" />
""".replace('\\', '\\\\')

    nav_regex = re.compile(r'<nav.*?</nav>', re.DOTALL)
    footer_regex = re.compile(r'<footer.*?</footer>', re.DOTALL)
    head_regex = re.compile(r'</head>', re.IGNORECASE)
    body_regex = re.compile(r'<body(.*?)>', re.IGNORECASE)

    updated_count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs: dirs.remove('.git')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        if 'Demographic data requests' in dirs: dirs.remove('Demographic data requests')
        
        for file in files:
            if file.endswith('.html') and file not in ['state_party_clone.html', 'precinct.html']:
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace first Nav
                if nav_regex.search(content):
                    content = nav_regex.sub(nav_str, content, count=1)
                
                # Replace first Footer
                if footer_regex.search(content):
                    content = footer_regex.sub(footer_str, content, count=1)
                
                # Add CSS
                if 'css/state_party_clone.css' not in content:
                    content = head_regex.sub(head_additions + '\n</head>', content, count=1)
                
                # Add body class
                if 'class="tx-clone"' not in content:
                    def body_repl(m):
                        attrs = m.group(1)
                        if 'class="' in attrs:
                            new_attrs = attrs.replace('class="', 'class="tx-clone ')
                            return f"<body{new_attrs}>"
                        else:
                            return f'<body class="tx-clone"{attrs}>'
                    content = body_regex.sub(body_repl, content, count=1)
                
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {path}")
                    updated_count += 1

    print(f"Nav replacement complete. Updated {updated_count} files.")

if __name__ == '__main__':
    process_files()
