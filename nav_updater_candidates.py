import os
import glob

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"

# We are going to target the "About ▼" dropdown, specifically right below the "Elected Reps" link.
target_elected_reps = '<a href="elected_officials.html">Elected Reps</a>'

# The new dropdown block including the Local Candidates directory
replacement_block = """          <a href="elected_officials.html">Elected Reps</a>
          <a href="local_candidates.html" style="color: #fff;">Local Candidates</a>"""

print("Initializing Local Candidates Navigation Update...")

files_modified = 0

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r") as f:
        content = f.read()
        
    # Skip if we've already done it
    if 'href="local_candidates.html"' in content:
        continue
        
    if target_elected_reps in content:
        # Perform exact string replacement
        new_content = content.replace(target_elected_reps, replacement_block)
        
        if new_content != content:
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"✅ Added Local Candidates to {os.path.basename(filepath)}")
            files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
