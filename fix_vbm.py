import re

# Read template file
with open('home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The main block missing from vbm was the nav bar.
# In home.html, the nav starts at <nav class="tx-clone-nav">
# But the original script used (<!-- Dynamic Background Shapes -->.*?<div class="tx-clone-nav-accent-bar"></div>)
# And home.html does NOT have an HTML comment "<!-- Dynamic Background Shapes -->". It was pulling an empty string!

# Correct segment extraction:
head_match = re.search(r'(<!DOCTYPE html>.*?<body class="tx-clone">)', html, re.DOTALL)
nav_match = re.search(r'(<nav class="tx-clone-nav">.*?<div class="tx-clone-nav-accent-bar"></div>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="tx-clone-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1) if head_match else ""
nav = nav_match.group(1) if nav_match else ""
footer = footer_match.group(1) if footer_match else ""

with open('vbm.html', 'r', encoding='utf-8') as f:
    vbm_full = f.read()

# Extract just the main content
main_match = re.search(r'(<header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">.*?</main>)', vbm_full, re.DOTALL)
vbm_content = main_match.group(1)

with open('vbm.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{vbm_content}\n{footer}")

print("vbm.html strictly repaired with proper navigation bar extracted.")
