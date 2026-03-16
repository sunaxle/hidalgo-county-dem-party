import os
import glob

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"

# Target the Connect dropdown
target_connect = """      <div class="nav-item dropdown">
        <span>Connect ▼</span>
        <div class="dropdown-content">
          <a href="contact.html">Contact Us</a>
        </div>"""

# What we want it to become
replacement_block = """      <div class="nav-item dropdown">
        <span>Connect ▼</span>
        <div class="dropdown-content">
          <a href="community_inbox.html">Inbox</a>
          <a href="contact.html">Contact Us</a>
        </div>"""

print("Initializing Community Inbox Restoration...")

files_modified = 0

for filepath in glob.glob(os.path.join(directory, "*.html")):
    # Skip the internal admin files which already have raw links
    if "admin" in os.path.basename(filepath):
        continue

    with open(filepath, "r") as f:
        content = f.read()
        
    # Skip if we've already done it
    if 'href="community_inbox.html"' in content:
        continue
        
    if target_connect in content:
        new_content = content.replace(target_connect, replacement_block)
        
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"✅ Restored Inbox to {os.path.basename(filepath)}")
            files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
