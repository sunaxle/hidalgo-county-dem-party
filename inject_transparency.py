import os
import glob
import re

def insert_transparency_link():
    html_files = glob.glob('*.html')
    
    # Target string to anchor our injection.
    # We want to insert the Transparency Portal link right after "Precinct Chairs" in the "About ▼" dropdown.
    target = '<a href="precinct_chairs.html">Precinct Chairs</a>'
    new_link = '\n          <a href="transparency.html">Transparency Portal</a>'
    
    modified_count = 0
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if target in content and 'href="transparency.html"' not in content:
            updated_content = content.replace(target, target + new_link)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            modified_count += 1
            print(f"Updated: {filename}")
            
    print(f"Injection complete. Modified {modified_count} files.")

if __name__ == "__main__":
    insert_transparency_link()
