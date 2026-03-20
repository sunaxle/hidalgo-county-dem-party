import glob
import os

with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

parts = html.split('  <div class="tx-clone-nav-accent-bar"></div>')
top_nav = parts[0] + '  <div class="tx-clone-nav-accent-bar"></div>\n'

footer_split = parts[1].split('<!-- Footer -->')
footer = '<!-- Footer -->' + footer_split[1]

body = """
  <main class="container" style="padding-top: 120px; padding-bottom: 60px; max-width: 100vw; overflow-x: hidden; box-sizing: border-box;">
    <div style="text-align: center; max-width: 900px; margin: 0 auto 4rem auto; padding: 0 1rem;">
      <h1 style="color: var(--accent); font-size: clamp(2.2rem, 8vw, 3.5rem); margin-bottom: 1rem; line-height:1.1;">Democracy Coded:</h1>
      <h2 style="color: #fff; font-size: clamp(1.4rem, 5vw, 2rem); margin-top:0;">The Architecture of Grassroots Power</h2>
      <p style="color: #cbd5e1; font-size: 1.2rem; line-height: 1.7; margin-top: 2rem;">
        This platform represents a fundamental shift in political organizing. We have stripped away traditional hierarchical bottlenecks and engineered a completely autonomous sandbox environment—directly driven by the organizers themselves. No input required from the top; raw empowerment given to the base.
      </p>
    </div>

    <!-- Scale -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 4rem;">
      <div style="background: rgba(15,23,42,0.6); padding: 2rem; border-radius: 12px; border: 1px solid rgba(56,189,248,0.2); text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
         <div style="font-size: 3rem; color: #38bdf8; font-weight: 800; font-family: 'Alfa Slab One', sans-serif;">300+</div>
         <div style="color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.5rem;">Core Precinct Chairs</div>
      </div>
      <div style="background: rgba(15,23,42,0.6); padding: 2rem; border-radius: 12px; border: 1px solid rgba(16,185,129,0.2); text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
         <div style="font-size: 3rem; color: #10b981; font-weight: 800; font-family: 'Alfa Slab One', sans-serif;">600+</div>
         <div style="color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.5rem;">Second-Tier Organizers</div>
      </div>
      <div style="background: rgba(15,23,42,0.6); padding: 2rem; border-radius: 12px; border: 1px solid rgba(245,158,11,0.2); text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
         <div style="font-size: 3rem; color: #f59e0b; font-weight: 800; font-family: 'Alfa Slab One', sans-serif;">2,000+</div>
         <div style="color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.5rem;">Total Field Volunteers</div>
      </div>
      <div style="background: rgba(15,23,42,0.6); padding: 2rem; border-radius: 12px; border: 1px solid rgba(239,68,68,0.2); text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
         <div style="font-size: 3rem; color: #ef4444; font-weight: 800; font-family: 'Alfa Slab One', sans-serif;">100k+</div>
         <div style="color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.5rem;">Local Democrats</div>
      </div>
    </div>

    <!-- Explainer Cards -->
    <div style="display: flex; flex-direction: column; gap: 3rem; max-width: 900px; margin: 0 auto;">
      
      <!-- Component 1 -->
      <div style="background: linear-gradient(145deg, rgba(30,58,138,0.4), rgba(15,23,42,0.8)); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 2.5rem; position: relative; overflow: hidden;">
         <div style="position: absolute; top: -20px; right: -20px; opacity: 0.05; font-size: 10rem;">🌐</div>
         <h3 style="color: #38bdf8; font-size: 1.8rem; margin-top: 0;">Dynamic Precinct Profiles</h3>
         <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.6;">
            <strong>What it does:</strong> Allows any of our 300+ Precinct Chairs to instantly update their public profile, post announcements, and set meeting times without ever needing approval from a web developer.
         </p>
         <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
            <strong>How it works:</strong> The site operates a native JavaScript data-pipeline that automatically parses a live Google Sheet and injects layout overrides straight into our universal routing blueprint. 
         </p>
         <a href="precinct_profiles.html" style="display: inline-block; margin-top: 1rem; color: #38bdf8; font-weight: bold; text-decoration: none;">View Precinct Profiles →</a>
      </div>

      <!-- Component 2 -->
      <div style="background: linear-gradient(145deg, rgba(16,185,129,0.15), rgba(15,23,42,0.8)); border: 1px solid rgba(16,185,129,0.2); border-radius: 16px; padding: 2.5rem; position: relative; overflow: hidden;">
         <div style="position: absolute; top: -20px; right: -20px; opacity: 0.05; font-size: 10rem;">🛡️</div>
         <h3 style="color: #10b981; font-size: 1.8rem; margin-top: 0;">Interactive Volunteer Gravity Engine (D3)</h3>
         <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.6;">
            <strong>What it does:</strong> A privacy-first interactive directory housing our 1,200+ legacy volunteers in a gamified, physics-based UI array that can be instantly filtered by Alphabet or Master Zip Code.
         </p>
         <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
            <strong>How it works:</strong> By anonymizing Personally Identifiable Information out of the frontend and processing raw nodes via D3 gravity logic, organizers can securely visualize and isolate field density exactly where they need to deploy blocks.
         </p>
         <a href="volunteer_roster.html" style="display: inline-block; margin-top: 1rem; color: #10b981; font-weight: bold; text-decoration: none;">View Volunteer Roster →</a>
      </div>

      <!-- Component 3 -->
      <div style="background: linear-gradient(145deg, rgba(239,68,68,0.15), rgba(15,23,42,0.8)); border: 1px solid rgba(239,68,68,0.2); border-radius: 16px; padding: 2.5rem; position: relative; overflow: hidden;">
         <div style="position: absolute; top: -20px; right: -20px; opacity: 0.05; font-size: 10rem;">📊</div>
         <h3 style="color: #ef4444; font-size: 1.8rem; margin-top: 0;">The Gap Tracker & Map Infrastructure</h3>
         <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.6;">
            <strong>What it does:</strong> Identifies which precincts are overperforming their historical baselines, and flags vacant regions where high Democratic voter ceilings are being ignored.
         </p>
         <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
            <strong>How it works:</strong> Custom Python scripts compile raw primary data straight from the Texas Secretary of State into mathematical JSON algorithms. This allows our grassroots base to surgically redirect volunteers away from safely held areas into competitive "Premium" target zones.
         </p>
         <a href="precinct_completion.html" style="display: inline-block; margin-top: 1rem; color: #ef4444; font-weight: bold; text-decoration: none;">View Gap Tracker →</a>
      </div>

    </div>
  </main>
"""

explainer = top_nav.replace("<title>Who We Are", "<title>Democracy Coded | About The Platform") + body + footer

with open('explainer.html', 'w', encoding='utf-8') as f:
    f.write(explainer)

print("Created explainer.html")

# Inject link site-wide into all dropdowns
modified_count = 0
for filename in glob.glob('*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # insert before <a href="about.html">About Us</a>
    if "explainer.html" not in content and "<a href=\"about.html\">About Us</a>" in content:
        content = content.replace(
            '<a href="about.html">About Us</a>', 
            '<a href="explainer.html" style="color: #38bdf8; font-weight: 800;">Democracy Coded 🧠</a>\\n            <a href="about.html">About Us</a>'
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1

print(f"Injected Explainer into {modified_count} navigation menus.")
