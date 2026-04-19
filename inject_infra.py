import glob
import re

html_files = glob.glob('*.html')

about_replacement = r'\1\n            <a href="run_for_office.html" style="color: #fca5a5; font-weight: 800;">Run for Office 🏛️</a>\n          </div>\n        </div>\n\n        <div class="nav-item dropdown">\n          <span>Action ▼</span>'
action_replacement = r'\1\n            <a href="election_workers.html" style="color: #c084fc; font-weight: 800;">Election Workers 📋</a>\n          </div>\n        </div>\n\n                <div class="nav-item dropdown">'
community_replacement = r'\1\n            <a href="clubs.html" style="color: #60a5fa; font-weight: 800;">Affiliated Clubs 🤝</a>\n            <a href="events.html" style="color: #fb923c; font-weight: 800;">Events Calendar 📅</a>\n          </div>\n        </div>\n\n        <div class="nav-item dropdown">\n          <span>Issues ▼</span>'

count = 0
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files that don't have the main navigation structure (like the new ones might have slightly different spacing, but they were built from home.html so it should work)
    # Actually wait, since some files might already have it or might miss a block, use careful regex.
    
    if "Run for Office 🏛️" in content:
        continue

    # About
    # Regex find `<a href="admin.html" ...>Portal 🌻</a> \n </div> \n </div> \n\n <div class="nav-item dropdown"> \n <span>Action ▼</span>`
    content = re.sub(
        r'(<a href="admin\.html"[^>]*>Portal 🌻</a>\s*</div>\s*</div>\s*<div class="nav-item dropdown">\s*<span>Action ▼</span>)',
        r'<a href="admin.html" style="color: #3b82f6; font-weight: 600;">Portal 🌻</a>\n            <a href="run_for_office.html" style="color: #fca5a5; font-weight: 800;">Run for Office 🏛️</a>\n          </div>\n        </div>\n\n        <div class="nav-item dropdown">\n          <span>Action ▼</span>',
        content, flags=re.IGNORECASE)

    # Action
    content = re.sub(
        r'(<a href="sustaining_members\.html"[^>]*>Sustaining Members ⭐</a>\s*</div>\s*</div>\s*<div class="nav-item dropdown">\s*(?:<a href="community\.html"|<span))',
        r'<a href="sustaining_members.html" style="color: #f59e0b; font-weight: 600;">Sustaining Members ⭐</a>\n            <a href="election_workers.html" style="color: #c084fc; font-weight: 800;">Election Workers 📋</a>\n          </div>\n        </div>\n\n                <div class="nav-item dropdown">\n          ',
        content, flags=re.IGNORECASE)

    # Community
    content = re.sub(
        r'(<a href="south_texas_region\.html"[^>]*>South TX</a>\s*</div>\s*</div>\s*<div class="nav-item dropdown">\s*<span>Issues ▼</span>)',
        r'<a href="south_texas_region.html">South TX</a>\n            <a href="clubs.html" style="color: #60a5fa; font-weight: 800;">Affiliated Clubs 🤝</a>\n            <a href="events.html" style="color: #fb923c; font-weight: 800;">Events Calendar 📅</a>\n          </div>\n        </div>\n\n        <div class="nav-item dropdown">\n          <span>Issues ▼</span>',
        content, flags=re.IGNORECASE)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        count += 1

print(f"Updated navigation on {count} active views.")
