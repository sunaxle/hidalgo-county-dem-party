import os
import re

perfect_nav = """  <nav class="tx-clone-nav">
    <div id="google_translate_element" style="position: absolute; right: 1rem; top: 0rem; z-index: 1000; transform: scale(0.8); transform-origin: top right;"></div>
    <div class="tx-clone-nav-socials">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.88z"/></svg>
    </div>
    <div class="tx-clone-nav-center">
      <a href="home.html" class="tx-clone-logo" id="main-party-logo">
        <img src="images/facebook_1656248751972_6946810765393131439.webp" alt="Hidalgo County Democratic Party Logo" class="tx-clone-logo-img">
      </a>
      <div class="tx-clone-nav-links">
        <a href="home.html" class="nav-item">Home</a>
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
            <a href="sustaining_members.html" style="color: #f59e0b; font-weight: 600;">Sustaining Members ⭐</a>
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
        </div>
<!-- TOGGLE_PLACEHOLDER -->
      </div>
    </div>
    <div class="tx-clone-nav-right">
      <a href="https://secure.actblue.com/donate/hidalgocountydems" class="tx-clone-btn-donate" target="_blank">DONATE</a>
    </div>
  </nav>
  <div class="tx-clone-nav-accent-bar"></div>"""

toggle_html = """        <div class="nav-item dropdown" style="margin-left: 1rem; border: 1px solid rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 8px; background: rgba(255,255,255,0.05);">
          <span id="term-toggle-label" style="font-size: 0.85rem; color: #b3c6ff;">Term: 2026-2028 ▼</span>
          <div class="dropdown-content" style="min-width: 150px;">
            <a href="#" onclick="toggleTerm('2026')">2026-2028 (300+ Members)</a>
            <a href="#" onclick="toggleTerm('2024')">2024-2026 (97 Members)</a>
          </div>
        </div>"""

def fix_all():
    nav_regex = re.compile(r'<nav class="tx-clone-nav">.*?</nav>\s*<div class="tx-clone-nav-accent-bar".*?></div>', re.DOTALL)
    
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
                
                if nav_regex.search(content):
                    custom_nav = perfect_nav
                    if file == 'precinct_chairs.html':
                        custom_nav = custom_nav.replace('<!-- TOGGLE_PLACEHOLDER -->', '\n' + toggle_html)
                    else:
                        custom_nav = custom_nav.replace('<!-- TOGGLE_PLACEHOLDER -->', '')
                        
                    content = nav_regex.sub(custom_nav, content, count=1)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated += 1

    print(f"Completely reset nav avoiding regex duplication on {updated} files.")

if __name__ == '__main__':
    fix_all()
