import re
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from collections import Counter

# Read URLs
with open('/Users/dr3/.gemini/antigravity/brain/5b53f512-c9a5-4fdd-b1e0-acdcbb2d9a4b/active_county_websites.md', 'r') as f:
    text = f.read()

urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_data(url):
    try:
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a'):
            txt = a.get_text(strip=True)
            if txt and len(txt) > 3 and len(txt) < 35:
                # Clean up string
                cleaned = re.sub(r'[^a-zA-Z\s]', '', txt).strip().title()
                if len(cleaned) > 3:
                    links.append(cleaned)
                    
        desc = ""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            desc = meta.get('content', '')
            
        return {"url": url, "links": list(set(links)), "desc": desc}
    except:
        return None

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_data, u) for u in urls]
    for f in concurrent.futures.as_completed(futures):
        if f.result():
            results.append(f.result())

all_links = []
unique_insights = []

for r in results:
    all_links.extend(r['links'])

counter = Counter(all_links)

with open('/Users/dr3/.gemini/antigravity/brain/5b53f512-c9a5-4fdd-b1e0-acdcbb2d9a4b/deep_scan_results.md', 'w') as out:
    out.write("# Deep AI Web Crawl: All 54 Texas County Sites\n\n")
    out.write(f"**Total Successfully Scraped:** {len(results)} out of {len(urls)} live websites.\n\n")
    
    out.write("## 🏆 Rare & Unique Pages (The Insights!)\n")
    out.write("Here are highly specific pages/features that only 2 to 6 of the 54 county parties possess. These are unique strategies we could steal:\n\n")
    
    for item, count in counter.most_common():
        # Only highlight moderately rare ones (not basic "Home", "About", "Donate")
        if 2 <= count <= 6:
            # Filter out generic words
            generic = ['Home', 'About Us', 'Contact', 'Donate', 'Volunteer', 'Facebook', 'Twitter', 'Privacy Policy', 'Login', 'Sign Up', 'Search', 'More', 'Skip To Content']
            if item not in generic and "County" not in item:
                out.write(f"* **{item}** (Found on {count} sites)\n")
                unique_insights.append(item)
        if len(unique_insights) > 20:
            break
            
    out.write("\n## 🎯 Mega-County Meta Statements\n")
    out.write("A look at how they position their SEO descriptions:\n")
    for r in results[:10]:
        if r['desc']:
            out.write(f"* **{r['url']}**: _{r['desc']}_\n")

