import glob
import os

with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

parts = html.split('  <div class="tx-clone-nav-accent-bar"></div>')
top_nav = parts[0] + '  <div class="tx-clone-nav-accent-bar"></div>\n'
footer_split = parts[1].split('<!-- Footer -->')
footer = '<!-- Footer -->' + footer_split[1]

body = """
  <main class="container fade-in" style="padding-top: 120px; padding-bottom: 60px;">
    <div style="max-width: 900px; margin: 0 auto;">
      <h1 style="color: var(--accent); font-size: 3.5rem; margin-bottom: 3rem; line-height:1.1; text-align:center;">Disclaimers &<br/>Community Standards</h1>
      
      <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 3rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
         
         <div style="margin-bottom: 3rem;">
            <h3 style="color: #38bdf8; font-size: 1.5rem; margin-top: 0; border-bottom: 1px solid rgba(56,189,248,0.3); padding-bottom: 0.5rem;">1. The Decentralized "Sandbox" Environment</h3>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              <strong>Expect Messiness.</strong> This platform is purposefully engineered as a non-hierarchical, decentralized sandbox driven directly by grassroots Precinct Chairs and local volunteers. Because data is sourced actively from the ground-up—rather than filtered perfectly through top-down leadership—the information ecosystem is constantly shifting. 
            </p>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              <strong>Nothing Here is Binding.</strong> Please take everything you read, including meeting times and localized announcements, with a grain of salt. Do not hold any single post or dashboard as absolute, official truth. While we strive for accuracy, the experimental nature of crowd-sourced civic organizing means human error and outdated information will occur.
            </p>
         </div>

         <div style="margin-bottom: 3rem;">
            <h3 style="color: #10b981; font-size: 1.5rem; margin-top: 0; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 0.5rem;">2. Data Privacy & Protection</h3>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              <strong>Protect Your Information.</strong> Please be incredibly mindful of the data you submit into the universal intake forms, contact pages, and public profile hubs. Protect your personal privacy to whatever degree you deem necessary. Do not post highly sensitive, secure, or unencrypted identifiable information if you are not comfortable having it cataloged or displayed in party databases. 
            </p>
         </div>

         <div style="margin-bottom: 3rem;">
            <h3 style="color: #f59e0b; font-size: 1.5rem; margin-top: 0; border-bottom: 1px solid rgba(245,158,11,0.3); padding-bottom: 0.5rem;">3. Clean & Respectful Baseline</h3>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              <strong>No Profanity Allowed.</strong> We fundamentally understand that fighting for democracy is exhausting, and civic organizing can generate immense frustration. Regardless, this website is a public platform accessible to children, families, and community members of all ages.
            </p>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              We require everyone to maintain a clean, courteous, and respectful environment at all times. Do not use bad words, hostile attacks, or abusive language in your submissions or on the "Share Our Stories" portal.
            </p>
         </div>

         <div style="margin-bottom: 3rem;">
            <h3 style="color: #ef4444; font-size: 1.5rem; margin-top: 0; border-bottom: 1px solid rgba(239,68,68,0.3); padding-bottom: 0.5rem;">4. Accountability & Enforcement (Banning)</h3>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              <strong>Your Access Can Be Revoked.</strong> The webmasters and Party Administration reserve the absolute right to ban users, block IP addresses, and permanently revoke digital access for any individual who violates these community standards. Harassment, spam submission algorithms, and continuous disruption of the digital infrastructure will result in automatic bans.
            </p>
         </div>

         <div>
            <h3 style="color: #a855f7; font-size: 1.5rem; margin-top: 0; border-bottom: 1px solid rgba(168,85,247,0.3); padding-bottom: 0.5rem;">5. Independent Fact-Checking</h3>
            <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
              <strong>Verify Before You Commute.</strong> Volunteers are highly encouraged to independently verify all precinct rally times, venue locations, and election law deadlines outlined by individual chairs. While this infrastructure empowers local leaders, the Hidalgo County Democratic Party assumes no liability for local scheduling miscommunications.
            </p>
         </div>

      </div>
    </div>
  </main>
"""

standards = top_nav.replace("<title>Who We Are", "<title>Community Standards & Disclaimers") + body + footer

with open('standards.html', 'w', encoding='utf-8') as f:
    f.write(standards)
print("Created standards.html")

modified_count = 0
for filename in glob.glob('*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    inject_str = """<p style="font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.3); display: inline-block; padding: 1.5rem; border-radius: 4px; color: white;">Pol. Adv. paid for by the Hidalgo County Democratic Party. Not authorized by any candidate or candidate's committee.</p>"""
    
    if "standards.html" not in content and inject_str in content:
        new_inject = inject_str + '\n    <div style="margin-top: 1.5rem;"><a href="standards.html" style="color: #94a3b8; text-decoration: underline; font-size: 0.85rem;">Platform Disclaimers & Community Standards</a></div>'
        content = content.replace(inject_str, new_inject)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1

print(f"Injected Disclaimers into {modified_count} footers.")
