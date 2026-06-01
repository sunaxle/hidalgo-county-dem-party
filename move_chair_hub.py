import os
import glob

directory = "."
files_modified = 0

chair_hub_link = '          <a href="chair_onboarding.html" style="color: #fcd34d; font-weight: 800;">Chair Hub 🧭</a>\n'

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    modified = False
    in_action_dropdown = False
    action_dropdown_inserted = False
    
    for line in lines:
        if 'href="chair_onboarding.html"' in line:
            # We skip it, we are removing it from its current spot
            modified = True
            continue
            
        if '<span>Action ▼</span>' in line:
            in_action_dropdown = True
            new_lines.append(line)
            continue
            
        if in_action_dropdown and '<div class="dropdown-content">' in line:
            new_lines.append(line)
            # Insert our link right after the dropdown content div
            new_lines.append(chair_hub_link)
            action_dropdown_inserted = True
            in_action_dropdown = False
            modified = True
            continue
            
        new_lines.append(line)
            
    if modified and action_dropdown_inserted:
        with open(filepath, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Moved Chair Hub in {os.path.basename(filepath)}")
        files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
