import re

with open('js/app.js', 'r') as f:
    content = f.read()

# Remove Mobile Experience Warning Popup
pattern = r'// --- Mobile Experience Warning Popup ---.*?sessionStorage\.setItem\("mobile_warning_seen", "true"\);\n      \}\);\n  \}\n'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('js/app.js', 'w') as f:
    f.write(content)
print("Updated js/app.js")
