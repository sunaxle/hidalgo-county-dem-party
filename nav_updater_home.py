import os
import glob
import shutil

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"
original_index = os.path.join(directory, "index.html")
new_home = os.path.join(directory, "home.html")

print("Initializing Urgent Maintenance & Compliance Routines...")

# 1. Rename existing index.html -> home.html
if os.path.exists(original_index):
    shutil.move(original_index, new_home)
    print("✅ Renamed index.html -> home.html")
else:
    print("⚠️ index.html not found! Execution Aborted to prevent loop.")
    exit()

# Setup target replacements
target_index = 'href="index.html"'
replace_home = 'href="home.html"'

# Lawsuit Compliance Targets (Removing from public navigation loops)
target_transparency = '<a href="transparency.html">Transparency Portal</a>'
target_inbox = '<a href="community_inbox.html">Community Inbox</a>'
target_intake = '<a href="community_intake.html">Community Inbox</a>'

# Gatekeeper Injection Target
target_head = '</head>'
gatekeeper_script = '  <script src="js/gatekeeper.js"></script>\n</head>'

files_modified = 0

# 2. Iterate and Replace
for filepath in glob.glob(os.path.join(directory, "*.html")):
    # Skip the new gatekeeper index if it already exists (we'll rebuild it anyway)
    if os.path.basename(filepath) == "index.html":
        continue
        
    with open(filepath, "r") as f:
        content = f.read()
    
    modified_content = content
    
    # Global Nav Redirection
    if target_index in modified_content:
        modified_content = modified_content.replace(target_index, replace_home)
        
    # Lawsuit Menu Suspensions
    if target_transparency in modified_content:
        modified_content = modified_content.replace(target_transparency, '')
    if target_inbox in modified_content:
        modified_content = modified_content.replace(target_inbox, '')
    if target_intake in modified_content:
        modified_content = modified_content.replace(target_intake, '')
        
    # Gatekeeper Security Injection
    if target_head in modified_content and 'js/gatekeeper.js' not in modified_content:
        modified_content = modified_content.replace(target_head, gatekeeper_script)
        
    if modified_content != content:
        with open(filepath, "w") as f:
            f.write(modified_content)
        print(f"🔒 Secured {os.path.basename(filepath)}")
        files_modified += 1

print(f"\nOperation Complete. Restructured {files_modified} files behind the Gatekeeper.")
