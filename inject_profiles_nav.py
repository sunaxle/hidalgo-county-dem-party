import os
import glob

def inject_profiles_nav():
    html_files = glob.glob("*.html")
    updated_count = 0
    
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Target the About dropdown block
        target_str = '<a href="precinct_chairs.html">Precinct Chairs</a>'
        new_str = '<a href="precinct_chairs.html">Precinct Chairs</a>\\n            <a href="precinct_profiles.html" style="color: var(--accent); font-weight: 600;">Precinct Profiles</a>'
        
        # Only inject if it isn't already there
        if target_str in content and "precinct_profiles.html" not in content[content.find(target_str):content.find(target_str)+200]:
            new_content = content.replace(target_str, new_str)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated_count += 1
            
    print(f"Successfully injected the Precinct Profiles link into {updated_count} HTML files!")

if __name__ == "__main__":
    inject_profiles_nav()
