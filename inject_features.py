import glob
import re

html_files = glob.glob('*.html')
count = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Inject internships into Connect dropdown
    if "Work With Us 💼" not in content:
        content = re.sub(
            r'(<a href="join\.html"[^>]*>Join the Party 🤝</a>)',
            r'\1\n            <a href="internships.html" style="color: #fbbf24; font-weight: 800;">Work With Us 💼</a>',
            content, flags=re.IGNORECASE)

    # 2. Inject press into About dropdown
    if "Press & Media 📰" not in content:
        content = re.sub(
            r'(<a href="about\.html".*?>About Us</a>)',
            r'\1\n            <a href="press.html">Press & Media 📰</a>',
            content, flags=re.IGNORECASE)

    # 3. Inject van_help into Action dropdown
    if "VAN Tech Support 💻" not in content:
        content = re.sub(
            r'(<a href="van_resources\.html".*?>VAN Resources</a>)',
            r'\1\n            <a href="van_help.html" style="color: #38bdf8; font-weight: 600;">VAN Tech Support 💻</a>',
            content, flags=re.IGNORECASE)

    if original != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Updated global navigation for the 3 new features across {count} files.")

# Fix van_resources.html specific block
with open('van_resources.html', 'r', encoding='utf-8') as f:
    van_content = f.read()

van_content = van_content.replace(
    '''<a href="#" onclick="alert('To submit a VAN help ticket, please email info@hidalgocountydems.org.'); return false;" class="van-block">''',
    '''<a href="van_help.html" class="van-block">'''
)

with open('van_resources.html', 'w', encoding='utf-8') as f:
    f.write(van_content)

print("Updated van_resources.html help ticket block routing.")

