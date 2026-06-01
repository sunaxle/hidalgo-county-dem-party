import urllib.request
import re

url = "https://www.facebook.com/photo?fbid=1974268900160998&set=a.126554571599116"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if match:
        print("FOUND:", match.group(1))
    else:
        print("NO OG IMAGE")
except Exception as e:
    print("ERROR:", e)
