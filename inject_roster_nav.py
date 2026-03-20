import os
import glob

html_files = glob.glob("*.html")
updates = 0

for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Target injection point
        target = '<a href="volunteer_dashboard.html">Volunteer Metrics</a>'
        injection = '<a href="volunteer_dashboard.html">Volunteer Metrics</a>\n            <a href="volunteer_roster.html" style="color: #4ade80; font-weight: 600;">Volunteer Roster</a>'
        
        if target in content and injection not in content:
            content = content.replace(target, injection)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            updates += 1
    except Exception as e:
        pass

print(f"Successfully injected Volunteer Roster link into {updates} HTML views.")
