import re
import os

log_path = '/Users/dr3/.gemini/antigravity/brain/1555a48a-1d95-45bb-8d2e-cef227f0979d/.system_generated/logs/overview.txt'

with open(log_path, 'r', encoding='utf-8') as f:
    logs = f.read()

# We need to find the specific view_file response
# It contains: "Total Lines: 609" and "Showing lines 1 to 609"
# The lines are prefixed with "<line_number>: "
if "Showing lines 1 to 609" in logs:
    start_str = "Showing lines 1 to 609\nThe following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.\n"
    end_str = "\nThe above content shows the entire, complete file contents of the requested file."
    
    if start_str in logs and end_str in logs:
        block = logs.split(start_str)[-1].split(end_str)[0]
        
        cleaned_lines = []
        for line in block.split('\n'):
            # Strip the "1: ", "2: ", etc.
            match = re.match(r'^\d+:\s(.*)$', line)
            if match:
                cleaned_lines.append(match.group(1))
            elif re.match(r'^\d+:$', line): # empty lines
                cleaned_lines.append("")
                
        with open('/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/elected_officials.html', 'w', encoding='utf-8') as f:
            f.write("\n".join(cleaned_lines))
        print("Restored successfully from logs!")
    else:
        print("Could not find exact block bounds.")
else:
    print("Could not find the 609 lines response in logs.")
