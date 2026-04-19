import re

html_files = [
    'home.html', 'about.html', 'contact.html', 'volunteer.html', 'donate.html',
    'vote.html', 'events.html', 'admin.html', 'vbm.html', 'clubs.html', 
    'election_workers.html', 'run_for_office.html'
]

urls = []
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract absolute URLs to see where we point existing "Report Voting Issues" style external links
            matches = re.findall(r'href="(http.*?)"', content)
            urls.extend(matches)
    except:
        pass

for url in set(urls):
    if "protect" in url.lower() or "issue" in url.lower() or "incident" in url.lower():
        print("Found potentially related external link:", url)

