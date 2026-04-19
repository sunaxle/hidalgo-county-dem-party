import glob
import re

html_files = glob.glob('*.html')
count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already injected
    if "Protect The Vote 🚨" in content:
        continue

    # We want to inject protect.html into the "Issues" dropdown, targeting before "Share Your Story"
    # Looking for: <a href="share_stories.html" style="color: #ef4444; font-weight: 800;">Share Your Story 📢</a>
    
    content = re.sub(
        r'(<a href="share_stories\.html"[^>]*>Share Your Story 📢</a>)',
        r'<a href="protect.html" style="color: #ef4444; font-weight: 800;">Protect The Vote 🚨</a>\n            \1',
        content, flags=re.IGNORECASE)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        count += 1

print(f"Updated navigation on {count} active views for Voter Protection.")
