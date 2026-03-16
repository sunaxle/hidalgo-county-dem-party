import os
import glob

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"

files_modified = 0

for filepath in glob.glob(os.path.join(directory, "*.html")):
    # Skip the new community_intake.html since it's already perfectly formed
    if "community_intake.html" in filepath:
        continue
        
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    modified = False
    
    for i, line in enumerate(lines):
        if 'href="share_stories.html"' in line:
            new_lines.append('          <a href="community_intake.html">Community Inbox</a>\n')
            modified = True
        elif 'href="call_it_out.html"' in line:
            # We completely drop this line because 'Community Inbox' replaces both
            modified = True
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Updated Navbar in {os.path.basename(filepath)}")
        files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
