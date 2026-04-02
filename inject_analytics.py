import os
import glob

html_files = glob.glob('*.html')

ga_snippet = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Q577ZL75XM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Q577ZL75XM');
</script>
"""

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "G-Q577ZL75XM" in content or "googletagmanager.com/gtag/js" in content:
        continue
    
    if "</head>" in content:
        new_content = content.replace("</head>", ga_snippet + "</head>")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Successfully injected Google Analytics into {count} HTML files.")
