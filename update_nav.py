import glob
import os

target_dir = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"
link = '<a href="donation_scenarios.html" style="color: #ec4899; font-weight: 800;">Donation Goals 💸</a>'

for fp in glob.glob(os.path.join(target_dir, "*.html")):
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    if link in content:
        continue

    # target string can be:
    # <span>Action ▼</span>\n          <div class="dropdown-content">\n
    # <span>Action ▼</span>\n            <div class="dropdown-content">\n
    
    t1 = '<span>Action ▼</span>\n          <div class="dropdown-content">\n'
    t2 = '<span>Action ▼</span>\n            <div class="dropdown-content">\n'
    
    if t1 in content:
        content = content.replace(t1, t1 + f'            {link}\n')
    elif t2 in content:
        content = content.replace(t2, t2 + f'              {link}\n')
    else:
        continue

    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
