import glob
import re
import os

print("Starting to move Alert Banners to the bottom...")

banner_html = """
<!-- Global Office Hours Alert Banner -->
<div class="office-alert-banner" style="background: linear-gradient(90deg, #ef4444, #b91c1c); color: white; text-align: center; padding: 0.75rem 1rem; position: fixed; bottom: 0; left: 0; width: 100%; z-index: 2000; font-weight: 500; font-size: 0.9rem; border-top: 2px solid #7f1d1d; display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap; box-shadow: 0 -4px 10px rgba(0,0,0,0.3);">
  <span>🚨 <strong>URGENT:</strong> The Headquarters is operating By Appointment Only. We need 3-Hour Priority Shift Volunteers to keep the doors open!</span>
  <a href="contact.html" style="background: white; color: #b91c1c; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 700; text-decoration: none; font-size: 0.8rem; text-transform: uppercase;">Sign Up Now</a>
</div>
"""

html_files = glob.glob('*.html')
# Regex to match the entire old banner block
old_banner_pattern = re.compile(r'\s*<!-- Global Office Hours Alert Banner -->\s*<div class="office-alert-banner".*?</div>\s*', re.DOTALL)
# Regex to match closing body tag
body_close_pattern = re.compile(r'(</body>)', re.IGNORECASE)

processed = 0

for file in html_files:
    if file == 'index.html':  # Skip the raw splash/redirect page entirely
        continue
        
    with open(file, 'r') as f:
        content = f.read()
        
    # 1. Strip out the old banner anywhere it exists
    content = old_banner_pattern.sub('\n', content)
    
    # 2. Reset the navbar margin (removes the top: 45px injected previously)
    content = content.replace(' style="top: 45px;"', '')
    
    # 3. Inject new banner before </body>
    content = body_close_pattern.sub(banner_html + r'\1', content, count=1)
    
    with open(file, 'w') as f:
        f.write(content)
        
    processed += 1
    print(f"Moved banner in: {file}")

print(f"\nSuccessfully moved the alert banner to the bottom on {processed} pages!")
