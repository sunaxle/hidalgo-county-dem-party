import os
import glob

html_files = glob.glob('*.html') + glob.glob('**/*.html', recursive=True)

target_str = '<div style="margin-top: 1.5rem;"><a href="standards.html"'
replacement_str = '''<div style="margin-top: 0.5rem;"><a href="precinct_toolkit.html" style="color: #64748b; text-decoration: none; font-size: 0.85rem;">🔒 Chair Toolkit</a></div>
    <div style="margin-top: 1.5rem;"><a href="standards.html"'''

count = 0
for filepath in html_files:
    # Skip the new toolkit itself
    if "precinct_toolkit.html" in filepath:
        continue
        
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if target_str in content and "precinct_toolkit.html" not in content:
            content = content.replace(target_str, replacement_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
print(f"Injected Chair Toolkit link into {count} footers.")
