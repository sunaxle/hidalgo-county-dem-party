import os
import glob
import re

REPO_DIR = "."
MOBILE_DIR = os.path.join(REPO_DIR, "mobile")
TEMPLATE_FILE = os.path.join(REPO_DIR, "mobile_template.html")

# Create mobile directory if it doesn't exist
if not os.path.exists(MOBILE_DIR):
    os.makedirs(MOBILE_DIR)

# Load template
with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_html = f.read()

# Get all HTML files in root
exclude_list = ["mobile_template.html", "index.html", "events.html", "volunteer.html", "precinct_lookup.html", 
                "demographic_map.html", "issues_map.html", "interactive_precincts.html", "political_strategy_dashboard.html", 
                "admin_dashboard.html", "volunteer_dashboard.html", "hidalgo_orbital_gallery.html", 
                "precinct_107_case_study.html", "mockup_c_dashboard.html", "visualizations_demo.html", 
                "live_results.html", "social_wall.html", "van_resources.html"]

html_files = glob.glob(os.path.join(REPO_DIR, "*.html"))
html_files = [f for f in html_files if os.path.basename(f) not in exclude_list]

success_count = 0

for file_path in html_files:
    filename = os.path.basename(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {filename} due to encoding error.")
        continue

    # Attempt to extract the core content. 
    # Strategy 1: Look for tx-clone-content-inner
    match = re.search(r'<div class="tx-clone-content-inner[^>]*>(.*?)</div>\s*</section>', content, re.IGNORECASE | re.DOTALL)
    if not match:
        # Strategy 2: Look for anything between </header> and <footer
        match = re.search(r'</header>(.*?)<footer', content, re.IGNORECASE | re.DOTALL)
    if not match:
        # Strategy 3: Just grab body excluding nav
        match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
        if match:
            body_content = match.group(1)
            # Remove navs
            body_content = re.sub(r'<nav.*?</nav>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
            # Remove footers
            body_content = re.sub(r'<footer.*?</footer>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
            match_str = body_content
        else:
            match_str = "<p>Content could not be parsed.</p>"
    else:
        match_str = match.group(1)

    # Format the title
    title = filename.replace(".html", "").replace("_", " ").title()
    
    # Inject into template
    output_html = template_html.replace("{{TITLE}}", title)
    output_html = output_html.replace("{{CONTENT}}", match_str)

    # Save to mobile directory
    output_path = os.path.join(MOBILE_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)
    
    success_count += 1
    print(f"Compiled: {filename} -> mobile/{filename}")

print(f"\n✅ SUCCESSFULLY COMPILED {success_count} PAGES INTO MOBILE UI SHELL!")
