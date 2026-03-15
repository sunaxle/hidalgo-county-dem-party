import glob
import os

html_files = glob.glob('*.html')

target_link = '<a href="precinct_completion.html">Gap Tracker</a>'
new_link = '          <a href="volunteer_dashboard.html">Volunteer Metrics</a>'

for file_path in html_files:
    if file_path == 'volunteer_dashboard.html':
        continue # Avoid double injection in the file just created
        
    with open(file_path, 'r') as f:
        content = f.read()

    # Prevent double injection
    if 'href="volunteer_dashboard.html"' not in content and target_link in content:
        updated_content = content.replace(target_link, f'{target_link}\n{new_link}')
        
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated {file_path}")
