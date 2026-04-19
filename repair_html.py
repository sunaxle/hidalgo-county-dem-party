import subprocess

# 1. Extract the perfect Local Tab from current file
with open('elected_officials.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
# From my view_file above, the Local Tab starts at line 558 ("        <!-- Local & Judicial Tab -->")
# and ends at line 926 ("    </div>")
# Let's find them reliably by string matching since line numbers can shift slightly
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "<!-- Local & Judicial Tab -->" in line:
        start_idx = i
    if start_idx != -1 and i > start_idx and '<p class="official-title">206th State District Court</p>' in line:
        # The line before 206th State District Court is the end of the clean Local Tab.
        # Wait, the end of the clean Local Tab is "    </div>" and then "    </div>"
        end_idx = i - 2
        break

local_tab_lines = lines[start_idx:end_idx]

# 2. Extract original Federal and State tabs from Git
head_file = subprocess.check_output(['git', 'show', 'HEAD:elected_officials.html']).decode('utf-8')
head_lines = head_file.split('\n')

# Find where the Local Tab starts in the HEAD file
head_local_start = -1
for i, line in enumerate(head_lines):
    if "<!-- Local & Judicial Tab -->" in line:
        head_local_start = i
        break

head_top = head_lines[:head_local_start]

# Also grab everything after Local Tab in the HEAD file (Footer, etc)
head_local_end = -1
for i in range(head_local_start, len(head_lines)):
    if "</section>" in head_lines[i]:
        head_local_end = i
        break

head_bottom = head_lines[head_local_end:]

# Combine!
restored = "\n".join(head_top) + "\n" + "".join(local_tab_lines) + "\n".join(head_bottom)

with open('elected_officials.html', 'w', encoding='utf-8') as f:
    f.write(restored)

print("Restored successfully!")
