import os
import re

real_links = """        <a href="index.html" class="nav-item">Home</a>
        <div class="nav-item dropdown">
          <span>About ▼</span>
          <div class="dropdown-content">
            <a href="about.html">About Us</a>
            <a href="bylaws.html">Bylaws</a>
            <a href="elected_officials.html">Elected Reps</a>
            <a href="precinct_chairs.html">Precinct Chairs</a>
          </div>
        </div>
        <div class="nav-item dropdown">
          <span>Action ▼</span>
          <div class="dropdown-content">
            <a href="volunteer.html">Volunteer</a>
            <a href="arena_training.html">The Arena</a>
            <a href="vote.html">Resources</a>
          </div>
        </div>
        <div class="nav-item dropdown">
          <span>Community ▼</span>
          <div class="dropdown-content">
            <a href="social_wall.html">Social Wall</a>
            <a href="county_websites.html">TX Dems</a>
            <a href="south_texas_region.html">South TX</a>
          </div>
        </div>
        <div class="nav-item dropdown">
          <span>Issues ▼</span>
          <div class="dropdown-content">
            <a href="issues_map.html">Issues Data Map</a>
            <a href="call_it_out.html">Call It Out Board</a>
            <a href="share_stories.html">Share Our Stories</a>
          </div>
        </div>
        <div class="nav-item dropdown">
          <span>Connect ▼</span>
          <div class="dropdown-content">
            <a href="community_inbox.html">Inbox</a>
            <a href="contact.html">Contact</a>
          </div>
        </div>"""

def fix_all():
    target_regex = re.compile(r'<div class="tx-clone-nav-links">.*?</div>', re.DOTALL)
    new_block = '<div class="tx-clone-nav-links">\n' + real_links + '\n      </div>'
    
    updated = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs: dirs.remove('.git')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if target_regex.search(content):
                    new_content = target_regex.sub(new_block, content, count=1)
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        updated += 1
    print(f"Restored real links on {updated} files.")

if __name__ == '__main__':
    fix_all()
