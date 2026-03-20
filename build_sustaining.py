import os
import re

def update_sustaining():
    path = "sustaining_members.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_main = """  <main class="container fade-in" style="padding-top: 120px; padding-bottom: 60px;">
    <div style="text-align: center; max-width: 800px; margin: 0 auto 3rem auto;">
      <h1 style="color: var(--accent); font-size: 3rem; margin-bottom: 1rem;">Sustaining Members</h1>
      <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.7;">
        Elections are a multi-year battle. The Democratic Party cannot survive on last-minute massive fundraising alone. To build resilient, persistent infrastructure, we need reliable monthly commitments. Chip in $5, $10, or $25 a month.
      </p>
      <div style="margin-top: 2rem; display: flex; gap: 1rem; justify-content: center;">
        <a href="https://secure.actblue.com/donate/hidalgocountydems" target="_blank" class="btn btn-primary" style="background: white; color: #1e3a8a; font-weight: bold; border: none; padding: 1rem 2rem; font-size: 1.1rem;">Chip In $5 / month</a>
      </div>
    </div>

    <!-- Hall of Fame -->
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 3rem;">
      <h2 style="text-align: center; margin-top: 0; color: #fff;">Sustaining Member Hall of Fame</h2>
      <p style="text-align: center; color: #94a3b8; margin-bottom: 2rem;">A special thank you to our monthly donors who keep these servers running.</p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
        <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
          <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
          <strong style="color: #fff; font-size: 1.1rem;">Jane Doe</strong>
          <div style="color: var(--accent); font-size: 0.85rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Founding Sustainer</div>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
          <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
          <strong style="color: #fff; font-size: 1.1rem;">John Smith</strong>
          <div style="color: var(--accent); font-size: 0.85rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Precinct Captain</div>
        </div>
        <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
          <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
          <strong style="color: #fff; font-size: 1.1rem;">Maria Garcia</strong>
          <div style="color: var(--accent); font-size: 0.85rem; text-transform: uppercase; margin-top: 0.5rem; letter-spacing: 1px;">Volunteer Force</div>
        </div>
      </div>
      <div style="text-align: center; margin-top: 3rem;">
        <p style="color: #64748b; font-style: italic;">Will your name be next?</p>
      </div>
    </div>
  </main>"""

    content = re.sub(r'<main class="container fade-in">.*?</main>', new_main, content, flags=re.DOTALL)
    content = re.sub(r'<title>.*?</title>', '<title>Sustaining Members | Hidalgo Dems</title>', content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def update_tracker():
    path = "precinct_completion.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    injection = """    <!-- Sustaining Member Projection -->
    <div class="projection-callout" style="background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 12px; padding: 2rem; margin-bottom: 2rem; text-align: center;">
      <h2 style="color: #0ea5e9; margin-top: 0; font-size: 1.5rem;">Sustaining the Infrastructure</h2>
      <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.6; max-width: 800px; margin: 0 auto;">
        Can you imagine if everyone here donated just $5? If all precinct captains donated $5/month, plus all our volunteers donated $5/month, look at the kind of sustained funding we could bring in to build out this digital infrastructure.
      </p>
      <a href="sustaining_members.html" class="btn btn-primary" style="margin-top: 1.5rem; display: inline-block;">Become a Sustaining Member</a>
    </div>

    <!-- The "Adopt 5" Quota & Even Spread Strategy -->"""

    content = content.replace('    <!-- The "Adopt 5" Quota & Even Spread Strategy -->', injection)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == '__main__':
    update_sustaining()
    update_tracker()
    print("Done")
