import os
import glob

html_files = glob.glob('*.html') + glob.glob('**/*.html', recursive=True)

old_footer_contact = """    <div style="margin-bottom: 2rem; font-weight: 500; font-size: 1.1rem;">
      <p>info@hidalgocountydems.org</p>
      <p>800 N. Main St. Suite 110</p>
      <p>McAllen, TX 78501</p>
      <p>(956) 672-7274</p>
    </div>"""

# Ensure exact spacing might vary, so let's do a more robust replacement if needed.
# Alternatively, we replace the exact block if it matches.
new_footer_contact = """    <div style="margin-bottom: 2rem; font-weight: 500; font-size: 1.1rem;">
      <p>info@hidalgocountydems.org</p>
      <p>(956) 672-7274</p>
      <p style="margin-top: 1.5rem; color: #38bdf8;">Questions About Voting?<br>Call us at 1-844-TX-VOTES</p>
      <p style="margin-top: 1.5rem; color: #a3e635;">Send Checks to:<br>Hidalgo County Democratic Party<br>800 N. Main St. Suite 110<br>McAllen, TX 78501</p>
    </div>"""

count = 0

for filepath in html_files:
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_footer_contact in content:
            content = content.replace(old_footer_contact, new_footer_contact)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
print(f"Updated footer contact information in {count} files.")
