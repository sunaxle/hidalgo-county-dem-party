import subprocess

# 1. Extract Local Tab from current file
with open('elected_officials.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "<!-- Local & Judicial Tab -->" in line:
        start_idx = i
    if start_idx != -1 and i > start_idx and '<p class="official-title">206th State District Court</p>' in line:
        end_idx = i - 2
        break

local_tab_lines = lines[start_idx:end_idx]

# 2. Get HEAD file
head_file = subprocess.check_output(['git', 'show', 'HEAD:elected_officials.html']).decode('utf-8')
head_lines = head_file.split('\n')

# 3. Find </section> in HEAD file to insert the new tab BEFORE it
section_end_idx = -1
for i, line in enumerate(head_lines):
    if "</section>" in line:
        section_end_idx = i
        break

# Combine: everything before </section>, then the local tab, then </section> and the rest
restored_lines = head_lines[:section_end_idx] + [line.rstrip() for line in local_tab_lines] + head_lines[section_end_idx:]

with open('elected_officials.html', 'w', encoding='utf-8') as f:
    f.write("\n".join(restored_lines))

print("Restored cleanly!")
