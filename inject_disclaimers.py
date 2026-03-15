import os
import re

def insert_disclaimer():
    target_files = [
        "transparency.html",
        "volunteer_dashboard.html",
        "demographic_map.html",
        "interactive_precincts.html"
    ]
    
    banner_html = """
  <!-- Demonstration Mode Disclaimer Banner -->
  <div class="demo-banner" style="background-color: #ef4444; color: white; text-align: center; padding: 1rem; margin-top: 4rem; z-index: 50; position: relative; font-weight: 500; font-size: 0.95rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-bottom: 2px solid #b91c1c;">
    <span style="font-size: 1.1rem; margin-right: 8px;">⚠️</span>
    <strong>DEMONSTRATION MODE:</strong> The metrics and individual records displayed on this page are simulated mock data generated for layout testing purposes only. They do not represent official Hidalgo County Democratic Party figures or personnel.
  </div>
"""

    # We want to insert this directly underneath the closing </nav> tag.
    target_tag = "</nav>"
    
    for filename in target_files:
        path = os.path.join("/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party", filename)
        
        if not os.path.exists(path):
            print(f"Skipping {filename} - File not found.")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "DEMONSTRATION MODE" not in content and target_tag in content:
            updated_content = content.replace(target_tag, target_tag + banner_html, 1)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Injected Disclaimer Banner into: {filename}")
        else:
            print(f"Disclaimer already exists or </nav> not found in: {filename}")

if __name__ == "__main__":
    insert_disclaimer()
