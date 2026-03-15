import os
import re

directory_path = '.'

def find_html_files(dir_path):
    html_files = []
    for root, dirs, files in os.walk(dir_path):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

html_files = find_html_files(directory_path)

# Regex to find the Connect dropdown and the closing tags of the navbar
nav_target = re.compile(
    r'(<div class="nav-item dropdown">\s*<span>Connect ▼</span>\s*<div class="dropdown-content">\s*<a href="community_inbox\.html">Inbox</a>\s*<a href="contact\.html">Contact</a>\s*</div>\s*</div>)(\s*)(</div>\s*</nav>)',
    re.MULTILINE
)

# High contrast orange button styled similarly to the state party UI
donate_button_html = r'\1\2  <a href="https://secure.actblue.com/donate/hidalgo" class="btn btn-primary" style="margin-left: 1rem; padding: 0.5rem 1.25rem; font-size: 0.875rem; box-shadow: 0 4px 14px rgba(247, 104, 13, 0.4); background: linear-gradient(135deg, #F7680D, #d95a0b); border: none;">DONATE</a>\n    \3'

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if nav_target.search(content):
            new_content = nav_target.sub(donate_button_html, content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"Could not find Connect dropdown in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Donate button injection complete.")
