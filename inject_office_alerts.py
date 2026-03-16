import os
import glob
import re

print("Starting Site-Wide Office Hours Alert Injection...")

# Define the HTML banner payload to be injected immediately after <body>
banner_html = """  <!-- Global Office Hours Alert Banner -->
  <div class="office-alert-banner" style="background: linear-gradient(90deg, #ef4444, #b91c1c); color: white; text-align: center; padding: 0.75rem 1rem; position: relative; z-index: 1000; font-weight: 500; font-size: 0.9rem; border-bottom: 2px solid #7f1d1d; display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap;">
    <span>🚨 <strong>URGENT:</strong> The Headquarters is operating By Appointment Only. We need 3-Hour Priority Shift Volunteers to keep the doors open!</span>
    <a href="contact.html" style="background: white; color: #b91c1c; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 700; text-decoration: none; font-size: 0.8rem; text-transform: uppercase;">Sign Up Now</a>
  </div>
"""

# Define the regex pattern to find the exact injection point (the <body> tag and its potential classes)
body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)

# Define directories to search
html_files = glob.glob('*.html')

injected_count = 0
skipped_count = 0

for filepath in html_files:
    # Skip the index/splash page as it usually has a unique raw aesthetic
    if filepath == 'index.html':
        continue
        
    with open(filepath, 'r') as file:
        content = file.read()
        
    # Check if the banner is already present to prevent duplicate stacking
    if "<!-- Global Office Hours Alert Banner -->" in content:
        print(f"Skipping {filepath}: Alert banner already exists.")
        skipped_count += 1
        continue
        
    # Check for the secondary demo banner to ensure we inject ABOVE it
    if "<!-- Demonstration Mode Disclaimer Banner -->" in content:
        # If the DEMO banner exists, we want to inject OUR alert banner right above it
        # The demo banner is usually placed near the top, often right under the nav or body
        # We will still just target the <body> tag so it sits at the absolute ceiling.
        pass

    # Perform the injection at the top of the body
    new_content = body_pattern.sub(r'\1\n' + banner_html, content, count=1)
    
    # If the content actually changed (i.e. we found a body tag)
    if new_content != content:
        with open(filepath, 'w') as file:
            file.write(new_content)
        print(f"Successfully injected Alert Banner into {filepath}")
        injected_count += 1
    else:
        print(f"Warning: Could not locate <body> tag in {filepath}")

print(f"\nInjection Complete! Processed {injected_count} files. Skipped {skipped_count} files.")
