import glob
import re

html_files = glob.glob('*.html')

count = 0
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to inject vbm.html into the "Action" dropdown, right after "Election Workers"
    # Looking for: <a href="election_workers.html" style="color: #c084fc; font-weight: 800;">Election Workers 📋</a>\n          </div>
    
    if "Vote by Mail 📬" in content:
        continue

    content = re.sub(
        r'(<a href="election_workers\.html"[^>]*>Election Workers 📋</a>\s*</div>)',
        r'<a href="election_workers.html" style="color: #c084fc; font-weight: 800;">Election Workers 📋</a>\n            <a href="vbm.html" style="color: #34d399; font-weight: 800;">Vote by Mail 📬</a>\n          </div>',
        content, flags=re.IGNORECASE)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        count += 1

print(f"Updated navigation on {count} active views for Vote By Mail.")
