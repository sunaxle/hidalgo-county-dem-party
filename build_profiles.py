import os
import re

def build_hub():
    path = "precinct_profiles.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_main = """
  <main class="container fade-in" style="padding-top: 120px; padding-bottom: 60px;">
    <div style="text-align: center; max-width: 800px; margin: 0 auto 3rem auto;">
      <h1 style="color: var(--accent); font-size: 3rem; margin-bottom: 1rem;">Precinct Profiles</h1>
      <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
        Meet the grassroots leaders of your neighborhood. Select your precinct below to view the dedicated Chair's profile, contact info, and localized announcements.
      </p>
      
      <!-- Dynamic Search -->
      <div style="margin-top: 3rem; background: rgba(0,0,0,0.3); padding: 3rem 2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <h3 style="margin-top: 0; color: #fff; font-size: 1.5rem;">Find Your Precinct</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem;">Enter your precinct number to view your local representatives.</p>
        <div style="display: flex; gap: 1rem; max-width: 500px; margin: 0 auto;">
          <input type="number" id="precinct-search-input" placeholder="e.g. 14" style="flex: 1; padding: 1rem 1.5rem; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #fff; font-size: 1.2rem; outline: none; text-align: center;">
          <button id="precinct-search-btn" class="btn btn-primary" style="border: none; cursor: pointer; padding: 1rem 2rem; font-size: 1.1rem; font-weight: bold; background: var(--accent); color: #020617;">Search</button>
        </div>
        <div id="precinct-search-error" style="color: #ef4444; margin-top: 1rem; display: none; font-weight: 600;"></div>
      </div>
    </div>

    <!-- Active Profiles Hook -->
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 4rem; margin-top: 5rem;">
      <h2 style="text-align: center; color: #fff; margin-bottom: 3rem;">Recently Updated Profiles</h2>
      <div id="recent-profiles-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
        <p style="color: #94a3b8; text-align: center; grid-column: 1/-1;">Loading live data...</p>
      </div>
    </div>
  </main>
  
  <script src="js/volunteer_sync.js"></script>
  <script src="js/precinct_hub.js"></script>
"""
    start_idx = content.find('<div class="tx-clone-nav-accent-bar"></div>')
    end_idx = content.find('<!-- Footer -->')
    if start_idx != -1 and end_idx != -1:
        part1 = content[:start_idx + len('<div class="tx-clone-nav-accent-bar"></div>')]
        part2 = content[end_idx:]
        final_content = part1 + new_main + part2
        final_content = final_content.replace('<title>Sustaining Members | Hidalgo Dems</title>', '<title>Precinct Profiles | Hidalgo Dems</title>')
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
def inject_sync_scripts():
    # Inject volunteer sync into precinct.html
    p = "precinct.html"
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    if '<script src="js/volunteer_sync.js"></script>' not in c:
        c = c.replace('<script src="js/precinct.js"></script>', '<script src="js/volunteer_sync.js"></script>\\n  <script src="js/precinct.js"></script>')
        with open(p, "w", encoding="utf-8") as fi:
            fi.write(c)
            
    # Inject volunteer sync into precinct_completion.html
    p2 = "precinct_completion.html"
    with open(p2, "r", encoding="utf-8") as f:
        c2 = f.read()
    if '<script src="js/volunteer_sync.js"></script>' not in c2:
        c2 = c2.replace('<script src="js/precinct_completion.js"></script>', '<script src="js/volunteer_sync.js"></script>\\n  <script src="js/precinct_completion.js"></script>')
        with open(p2, "w", encoding="utf-8") as fi:
            fi.write(c2)

if __name__ == '__main__':
    build_hub()
    inject_sync_scripts()
    print("HTML Wiring Complete!")
