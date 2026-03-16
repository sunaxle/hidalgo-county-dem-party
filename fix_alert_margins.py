import os
import glob
import re

print("Starting CSS/HTML Margin Adjustment for Alert Banner...")

# Define the HTML banner payload (unchanged)
banner_html = """  <!-- Global Office Hours Alert Banner -->
  <div class="office-alert-banner" style="background: linear-gradient(90deg, #ef4444, #b91c1c); color: white; text-align: center; padding: 0.75rem 1rem; position: fixed; top: 0; left: 0; width: 100%; z-index: 2000; font-weight: 500; font-size: 0.9rem; border-bottom: 2px solid #7f1d1d; display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap;">
    <span>🚨 <strong>URGENT:</strong> The Headquarters is operating By Appointment Only. We need 3-Hour Priority Shift Volunteers to keep the doors open!</span>
    <a href="contact.html" style="background: white; color: #b91c1c; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 700; text-decoration: none; font-size: 0.8rem; text-transform: uppercase;">Sign Up Now</a>
  </div>
"""

# The Navbar needs to be bumped down ~45px so the fixed banner at top:0 can sit above it.
# We will use regex to find `<nav class="navbar"` and inject a top position
nav_pattern = re.compile(r'(<nav\s+class="navbar[^>]*>)', re.IGNORECASE)

html_files = glob.glob('*.html')

fixed_count = 0

for filepath in html_files:
    if filepath == 'index.html':
        continue
        
    with open(filepath, 'r') as file:
        content = file.read()
        
    # Overwrite the old banner with the new fixed banner (if it exists)
    old_banner_regex = re.compile(r'<!-- Global Office Hours Alert Banner -->\s*<div class="office-alert-banner" style="[^>]+>(?:.*?</div>)', re.DOTALL)
    content = old_banner_regex.sub(banner_html, content)
    
    # We must push the navbar down from top:0 to top: 45px (the exact height of the banner)
    # The safest way is to inject an inline style into the navbar.
    if '<nav class="navbar"' in content or '<nav class="navbar scrolled"' in content:
        # Prevent double-bumping
        if 'style="top: 45px;"' not in content:
            # We'll inject style="top: 45px;" right after the class attribute
            content = re.sub(r'(class="navbar[^"]*")', r'\1 style="top: 45px;"', content)
            
    with open(filepath, 'w') as file:
        file.write(content)
    fixed_count += 1
    print(f"Repositioned Navbar in {filepath}")

print(f"\nMargin adjustment complete. Processed {fixed_count} files.")
