import os
import re

directory_path = '.'

def find_html_files(dir_path):
    html_files = []
    for root, dirs, files in os.walk(dir_path):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

html_files = find_html_files(directory_path)

new_nav_links = """    <div class="nav-links">
      <a href="index.html" class="nav-item">Home</a>
      
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
      </div>
    </div>\n  </nav>"""

nav_regex = re.compile(r'<div class="nav-links">.*?</nav>', re.DOTALL)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if nav_regex.search(content):
            new_content = nav_regex.sub(new_nav_links, content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"Could not find nav component in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Nav replacement complete.")
