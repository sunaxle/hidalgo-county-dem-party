import re

with open("precinct_profiles.html", "r", encoding="utf-8") as f:
    html = f.read()

# extract head and nav
head_match = re.search(r'(<!DOCTYPE html>.*?<main)', html, re.DOTALL)
footer_match = re.search(r'(<!-- Footer -->.*</html>)', html, re.DOTALL)

if head_match and footer_match:
    head = head_match.group(1)
    footer = footer_match.group(1)
    
    # fix the main tag opening since we grabbed up to <main
    head = head.replace('<main', '<main class="content-section" style="max-width: 1100px; margin: 0 auto; padding: 4rem 1rem;">\n')
    
    content = """
    <a href="precinct_profiles.html" style="color: #38bdf8; text-decoration: none; margin-bottom: 2rem; display: inline-block;">&larr; Back to Profiles</a>
    <h1 style="color: #fff; font-size: 3rem; margin-bottom: 1rem; text-align: center;">Precinct 107: The Power of Grassroots Organizing</h1>
    <p style="text-align: center; color: var(--accent); font-size: 1.25rem; font-weight: 600; margin-bottom: 4rem;">A Strategic Case Study in Base Building</p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 4rem; align-items: start;">
      
      <!-- Data Column -->
      <div>
        <h2 style="color: #cbd5e1; font-size: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; margin-bottom: 2rem;">Past Precinct Performance</h2>
        <div style="display: grid; grid-template-columns: 1fr; gap: 1rem; margin-bottom: 3rem;">
          <div style="background: #1e293b; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2.5rem; color: var(--accent); font-weight: 800; margin-bottom: 0.5rem;">~2,400</div>
            <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Registered Voters</div>
          </div>
          <div style="background: #1e293b; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2.5rem; color: var(--accent); font-weight: 800; margin-bottom: 0.5rem;">240</div>
            <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Average Midterm Turnout</div>
          </div>
          <div style="background: rgba(56, 189, 248, 0.05); border: 1px solid var(--accent); border-radius: 8px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2.5rem; color: #10b981; font-weight: 800; margin-bottom: 0.5rem;">70+</div>
            <div style="color: #94a3b8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Organized Base (Alma's Team)</div>
          </div>
        </div>

        <div style="background: #0f172a; padding: 2rem; border-radius: 8px; border-left: 4px solid var(--accent);">
          <h3 style="color: #fff; margin-top: 0; font-size: 1.5rem;">The Impact</h3>
          <p style="color: #94a3b8; line-height: 1.6; font-size: 1.1rem;">
            In a typical cycle, Precinct 107 turns out around 240 voters. Because Precinct Chair Alma Vera and her team have cultivated a direct network of over 70 consistent voters, <strong>they have effectively locked in 30% of the required turnout</strong> before early voting even begins.
          </p>
        </div>
      </div>

      <!-- Strategy Column -->
      <div>
        <h2 style="color: #cbd5e1; font-size: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; margin-bottom: 2rem;">The Leadership Network</h2>
        <p style="color: #94a3b8; line-height: 1.6; margin-bottom: 2rem; font-size: 1.1rem;">
          Alma Vera doesn't do it alone. She has established a multi-tiered leadership structure utilizing the official TDP Precinct Chair model. By recruiting Neighborhood Captains (Chris Vera, Jason Delattre) who in turn recruit Block Workers, the work is distributed. Nobody is overwhelmed, and the network grows exponentially.
        </p>

        <h2 style="color: #cbd5e1; font-size: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; margin-bottom: 2rem;">Growth Opportunities</h2>
        <ul style="color: #94a3b8; line-height: 1.7; padding-left: 1.5rem; margin-bottom: 3rem; font-size: 1.1rem;">
          <li style="margin-bottom: 0.5rem;"><strong>Pending Captains:</strong> There are at least 2 more major subdivisions/colonias in this precinct. The immediate goal is identifying Neighborhood Captains 3 and 4 to cover those areas.</li>
          <li><strong>Neighborhood Mapping:</strong> We are currently mapping out exactly how many neighborhoods and colonias exist in Precinct 107 to identify geographic blind spots.</li>
        </ul>

        <h2 style="color: #cbd5e1; font-size: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; margin-bottom: 1rem;">Precinct Map</h2>
        <div style="width: 100%; height: 300px; background: #1e293b; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8; border: 2px dashed #475569; margin-bottom: 2rem;">
          [ MAP PLACEHOLDER - INSERT PRECINCT 107 MAP HERE ]
        </div>

      </div>

    </div>
    </main>
    """
    
    full_html = head + content + footer
    with open("precinct_107_case_study.html", "w", encoding="utf-8") as out:
        out.write(full_html)
    print("Created precinct_107_case_study.html")
else:
    print("Failed to match")
