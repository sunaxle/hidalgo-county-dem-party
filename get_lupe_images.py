import urllib.request
from bs4 import BeautifulSoup
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://lupenet.org/marcha-del-pueblo-3/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    
    # Let's get og:image too
    og_image = soup.find('meta', property='og:image')
    if og_image:
        images.append(("OG Image", og_image.get('content')))
        
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and ('marcha' in src.lower() or 'pueblo' in src.lower() or 'lupe' in src.lower()):
            images.append(("Page Image", src))
            
    print(json.dumps(list(set(images)), indent=2))
except Exception as e:
    print(f"Error: {e}")
