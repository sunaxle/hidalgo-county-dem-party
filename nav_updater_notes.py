import os
import glob

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"

# Target the Issues dropdown exactly as it exists right now
target_issues = """      <div class="nav-item dropdown">
        <span>Issues ▼</span>
        <div class="dropdown-content">
          <a href="issues_map.html">Issues Data Map</a>
          <a href="interactive_precincts.html">Live Precinct Issues</a>
          <a href="share_stories.html">Share Our Stories</a>
        </div>"""

# What we want it to become
replacement_block = """      <div class="nav-item dropdown">
        <span>Issues ▼</span>
        <div class="dropdown-content">
          <a href="issues_map.html">Issues Data Map</a>
          <a href="interactive_precincts.html">Live Precinct Issues</a>
          <a href="share_stories.html">Share Our Stories</a>
          <a href="county_chair_notes.html">County Chair Notes</a>
        </div>"""

print("Initializing County Chair Notes Restoration...")

files_modified = 0

for filepath in glob.glob(os.path.join(directory, "*.html")):
    # Skip the internal admin files which already have raw links
    if "admin" in os.path.basename(filepath):
        continue

    with open(filepath, "r") as f:
        content = f.read()
        
    # Skip if we've already done it
    if 'href="county_chair_notes.html"' in content:
        continue
        
    if target_issues in content:
        new_content = content.replace(target_issues, replacement_block)
        
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"✅ Restored Notes to {os.path.basename(filepath)}")
            files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
