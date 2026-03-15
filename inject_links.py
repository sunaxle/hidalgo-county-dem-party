import glob
import os

html_files = glob.glob('*.html')

target_link = '<a href="vote.html">Resources</a>'
new_link = '          <a href="precinct_completion.html">Gap Tracker</a>'

for file_path in html_files:
    if file_path == 'precinct_completion.html':
        continue # Already mapped inside itself during creation
        
    with open(file_path, 'r') as f:
        content = f.read()

    # Prevent double injection
    if 'href="precinct_completion.html"' not in content and target_link in content:
        # Find the Resources link under the Action dropdown and inject the new tool under it
        updated_content = content.replace(target_link, f'{target_link}\n{new_link}')
        
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated {file_path}")
