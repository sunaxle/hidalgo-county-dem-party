import re

with open("index.html", "r") as f:
    content = f.read()

# Extract the tx-clone-nav block from index.html
nav_match = re.search(r'<nav class="tx-clone-nav">.*?</nav>', content, re.DOTALL)
if nav_match:
    nav_html = nav_match.group(0)
    
    with open("chair_onboarding.html", "r") as f2:
        onboarding_content = f2.read()
        
    # Replace the placeholder in chair_onboarding.html
    new_onboarding = re.sub(r'<nav class="tx-clone-nav">.*?</nav>', nav_html, onboarding_content, flags=re.DOTALL)
    
    with open("chair_onboarding.html", "w") as f2:
        f2.write(new_onboarding)
        
    print("Successfully copied navigation block into chair_onboarding.html")
else:
    print("Failed to find navigation block in index.html")
