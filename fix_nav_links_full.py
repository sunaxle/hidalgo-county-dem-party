import os
import re

real_links = """        <a href="home.html" class="nav-item">Home</a>
      <a href="data/index.html" class="nav-item" style="color: #c084fc; font-weight: 600;">Data 🔒</a>
      
      <div class="nav-item dropdown">
        <span>About ▼</span>
        <div class="dropdown-content">
          <a href="about.html">About Us</a>
          <a href="bylaws.html">Bylaws</a>
          <a href="elected_officials.html">Elected Reps</a>
          <a href="local_candidates.html" style="color: #fff;">Local Candidates</a>
          <a href="precinct_chairs.html">Precinct Chairs</a>
          <a href="admin.html" style="color: #3b82f6; font-weight: 600;">Portal 🌻</a>
        </div>
      </div>

      <div class="nav-item dropdown">
        <span>Action ▼</span>
        <div class="dropdown-content">
          <a href="volunteer.html">Volunteer</a>
          <a href="arena_training.html">The Arena</a>
          <a href="van_resources.html">VAN Resources</a>
          <a href="vote.html">Resources</a>
          <a href="precinct_completion.html">Gap Tracker</a>
          <a href="volunteer_dashboard.html">Volunteer Metrics</a>
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
          <a href="interactive_precincts.html">Live Precinct Issues</a>
          <a href="share_stories.html">Share Our Stories</a>
          <a href="county_chair_notes.html">County Chair Notes</a>
        </div>
      </div>

      <div class="nav-item dropdown">
        <span>Connect ▼</span>
        <div class="dropdown-content">
          <a href="community_inbox.html">Inbox</a>
          <a href="community_intake.html">Community Notes</a>
          <a href="contact.html">Contact Us</a>
        </div>
      </div>"""

toggle_html = """      <div class="nav-item dropdown" style="margin-left: 1rem; border: 1px solid rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 8px; background: rgba(255,255,255,0.05);">
        <span id="term-toggle-label" style="font-size: 0.85rem; color: #b3c6ff;">Term: 2026-2028 ▼</span>
        <div class="dropdown-content" style="min-width: 150px;">
          <a href="#" onclick="toggleTerm('2026')">2026-2028 (300+ Members)</a>
          <a href="#" onclick="toggleTerm('2024')">2024-2026 (97 Members)</a>
        </div>
      </div>"""

def fix_all():
    target_regex = re.compile(r'<div class="tx-clone-nav-links">.*?</div>', re.DOTALL)
    translate_widget = '<div id="google_translate_element" style="position: absolute; right: 1rem; top: 0rem; z-index: 1000; transform: scale(0.8); transform-origin: top right;"></div>'
    nav_open_regex = re.compile(r'(<nav class="tx-clone-nav">)')

    updated = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs: dirs.remove('.git')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                if not target_regex.search(content):
                    continue

                links_to_insert = real_links
                if file == 'precinct_chairs.html':
                    links_to_insert += "\n" + toggle_html
                
                new_block = '<div class="tx-clone-nav-links">\n' + links_to_insert + '\n      </div>'
                content = target_regex.sub(new_block, content, count=1)
                
                if 'id="google_translate_element"' not in content:
                    content = nav_open_regex.sub(r'\1\n    ' + translate_widget, content, count=1)

                if content != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated += 1

    print(f"Fully restored accurate links and translate widgets on {updated} files.")

if __name__ == '__main__':
    fix_all()
