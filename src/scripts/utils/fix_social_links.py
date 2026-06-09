import glob
import os
import re

directory = "/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party"

files_modified = 0

# The patterns we want to match
twitter_pattern = r'(<svg[^>]*><path d="M23\.953 4\.57[^>]*></svg>)'
facebook_pattern = r'(<svg[^>]*><path d="M24 12\.073c0-6\.627[^>]*></svg>)'
instagram_pattern = r'(<svg[^>]*><path d="M12 2\.163c3\.204[^>]*></svg>)'

twitter_replacement = r'<a href="https://twitter.com/hidalgocountydp" target="_blank" rel="noopener noreferrer" aria-label="Twitter" style="color: inherit;">\1</a>'
facebook_replacement = r'<a href="https://www.facebook.com/hidalgocountydems" target="_blank" rel="noopener noreferrer" aria-label="Facebook" style="color: inherit;">\1</a>'
instagram_replacement = r'<a href="https://instagram.com/hidalgocountydems" target="_blank" rel="noopener noreferrer" aria-label="Instagram" style="color: inherit;">\1</a>'

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            modified = False
            
            # Check if links are already applied to avoid double wrapping
            if 'href="https://twitter.com/hidalgocountydp"' not in content and 'M23.953 4.57' in content:
                content, count = re.subn(twitter_pattern, twitter_replacement, content)
                if count > 0:
                    modified = True
                    
            if 'href="https://www.facebook.com/hidalgocountydems"' not in content and 'M24 12.073c0-6.627' in content:
                content, count = re.subn(facebook_pattern, facebook_replacement, content)
                if count > 0:
                    modified = True
                    
            if 'href="https://instagram.com/hidalgocountydems"' not in content and 'M12 2.163c3.204' in content:
                content, count = re.subn(instagram_pattern, instagram_replacement, content)
                if count > 0:
                    modified = True

            if modified:
                with open(filepath, 'w') as f:
                    f.write(content)
                files_modified += 1

print(f"Modified {files_modified} files to add social links.")
