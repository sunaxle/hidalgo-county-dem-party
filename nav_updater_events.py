import os
import glob

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"

# We are going to target the "Action ▼" dropdown, specifically right below the "Volunteer" link.
target_volunteer = '<a href="volunteer.html">Volunteer</a>'

# The new dropdown block including the two events
replacement_block = """          <a href="volunteer.html">Volunteer</a>
          <a href="convention.html" style="color: var(--accent); font-weight: 600;">County Convention</a>
          <a href="runoff_election.html" style="color: var(--primary); font-weight: 600;">Runoff Election</a>"""

print("Initializing Election Events Navigation Update...")

files_modified = 0

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r") as f:
        content = f.read()
        
    # Skip if we've already done it
    if 'href="convention.html"' in content:
        continue
        
    if target_volunteer in content:
        # Perform exact string replacement
        new_content = content.replace(target_volunteer, replacement_block)
        
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"✅ Added Events to {os.path.basename(filepath)}")
            files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
