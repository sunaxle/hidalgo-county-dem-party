import os

# Define the target directory containing the HTML files
directory = '/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party'

# The exact target string we want to search for inside the `About ▼` dropdown
target_string = '<a href="transparency.html">Transparency Portal</a>'

# The new hyperlink we want to inject immediately after the Transparency Portal
injection_string = '          <a href="admin.html" style="color: #3b82f6; font-weight: 600;">Executive Portal 🔒</a>'

print("Initializing Admin Portal Injection Sequence...")

# Counter for tracking successful injections
files_modified = 0

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        # Read the file contents
        with open(filepath, 'r') as file:
            lines = file.readlines()
            
        modified = False
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            # If we find the exact target string
            if target_string in line:
                # Check if we already injected the Admin link to avoid duplicates
                if i + 1 < len(lines) and 'href="admin.html"' in lines[i+1]:
                    print(f"Skipping {filename} - Admin Portal already present.")
                    continue
                else:
                    # Inject the new link on the very next line
                    new_lines.append(injection_string + '\n')
                    modified = True
                    
        # Write the modified contents back to the file
        if modified:
            with open(filepath, 'w') as file:
                file.writelines(new_lines)
            print(f"✅ Successfully injected Admin Portal into {filename}")
            files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} HTML files.")
