import re

with open('precinct_chairs.html', 'r') as f:
    content = f.read()

# 1. Remove the Open Precinct Chair Guide button
pattern_btn = r'\s*<button onclick="document\.getElementById\(\'guideModal\'\)\.style\.display=\'flex\'".*?</button>'
content = re.sub(pattern_btn, '', content, flags=re.DOTALL)

# 2. Extract resources and place above CTA
resources_html = '''
  <section class="container fade-in" style="margin-bottom: 2rem;">
    <div class="glass-card" style="text-align: center; padding: 2.5rem 2rem; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px;">
      <h3 style="color: #38bdf8; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.5rem;">Precinct Chair Resources</h3>
      <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
        <a href="resources/TDP-2021-Precinct-Chair-Guide (9).pdf" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: #e2e8f0; text-decoration: none; padding: 1rem 1.5rem; font-weight: 600; transition: all 0.2s;">
          📄 TDP Precinct Chair Guide (PDF)
        </a>
        <a href="resources/county-chair-handbook (1).pdf" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: #e2e8f0; text-decoration: none; padding: 1rem 1.5rem; font-weight: 600; transition: all 0.2s;">
          📘 County Chair Handbook (PDF)
        </a>
      </div>
    </div>
  </section>
'''

# Find the CTA section
pattern_cta = r'(<!-- CTA Section -->\s*<section class="container fade-in" style="margin-bottom: 5rem;">)'
content = re.sub(pattern_cta, resources_html + r'\n  \1', content)

# 3. Remove the entire guideModal and associated scripts
pattern_modal = r'<!-- Guide Modal Structure -->.*?</script>'
content = re.sub(pattern_modal, '', content, flags=re.DOTALL)

with open('precinct_chairs.html', 'w') as f:
    f.write(content)
print("Done updating.")
