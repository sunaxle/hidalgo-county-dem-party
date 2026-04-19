import urllib.request
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.facebook.com/share/p/1FK5gm7ptt/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for meta in soup.find_all('meta'):
        if meta.get('property') in ['og:title', 'og:description']:
            print(f"{meta.get('property')}: {meta.get('content')}")
except Exception as e:
    print(f"Error: {e}")
