import re

with open('precinct_chairs.html', 'r') as f:
    content = f.read()

# 1. Remove Roster Disclaimer and Organizing Model
pattern1 = r'\s*<div style="background: rgba\(239, 68, 68, 0\.15\).*?</div>\s*<!-- Precinct Organizing Model -->.*?</div>\s*<h1>Precinct Chair Directory</h1>'
content = re.sub(pattern1, '\n    <h1>Precinct Chair Directory</h1>', content, flags=re.DOTALL)

# 2. Replace Map and Directory sections
pattern2 = r'<!-- Interactive Map Section -->.*?<!-- CTA Section -->'
replacement2 = '''<!-- Interactive Map Section removed -->

  <!-- Directory Section -->
  <section class="container" style="margin-bottom: 5rem;">
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 2rem 1rem;">
      <div class="glass-card" style="padding: 2.5rem; text-align: center; max-width: 550px; background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(56, 189, 248, 0.3);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🏛️</div>
        <h3 style="color: #38bdf8; margin-top: 0; margin-bottom: 1rem; font-size: 1.5rem;">Official State Rosters</h3>
        <p style="color: #e2e8f0; font-size: 1rem; margin-bottom: 1.5rem;">Due to privacy and security concerns, direct contact information for Precinct Chairs is no longer hosted publicly on this website. You can find the official, public rosters maintained by the State of Texas below.</p>
        
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <a href="https://www.sos.state.tx.us/elections/voter/current.shtml" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); width: 100%; text-decoration: none; padding: 1rem;">
            <strong style="display: block; color: #fff; margin-bottom: 0.25rem;">TX Secretary of State</strong>
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">Current Election Information & Rosters</span>
          </a>
          
          <a href="https://emr.sos.texas.gov/cpc-filings/cpc-contact-report.aspx" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); width: 100%; text-decoration: none; padding: 1rem;">
            <strong style="display: block; color: #fff; margin-bottom: 0.25rem;">SOS Election Management System</strong>
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: normal;">Precinct Chair Contact Report Search</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->'''
content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# 3. Remove unnecessary scripts at the end
pattern3 = r'<!-- Map Data and Scripts -->.*?</script>\s*<script src="js/value_counter\.js"></script>'
replacement3 = '<script src="js/value_counter.js"></script>'
content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)

with open('precinct_chairs.html', 'w') as f:
    f.write(content)
print("Done rewriting.")
