import re

# Read template file (we use volunteer.html as it is clean)
with open('volunteer.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract segments
head_match = re.search(r'(<!DOCTYPE html>.*?<body class="tx-clone">)', html, re.DOTALL)
nav_match = re.search(r'(<!-- Dynamic Background Shapes -->.*?<div class="tx-clone-nav-accent-bar"></div>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="tx-clone-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1) if head_match else ""
nav = nav_match.group(1) if nav_match else ""
footer = footer_match.group(1) if footer_match else ""

# 1. clubs.html
clubs_content = """
  <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">
    <h1>Affiliated Clubs & Organizations</h1>
    <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">Join a local Democratic club to connect with your community, organize around specific issues, and build lasting power.</p>
  </header>
  <main class="container fade-in" style="min-height: 50vh; text-align: center; margin-bottom: 4rem;">
    <div class="glass-card" style="padding: 4rem 2rem; border-color: var(--accent);">
      <h2 style="font-size: 2rem; margin-bottom: 1rem; color: white;">Register Your Club!</h2>
      <p style="font-size: 1.25rem; color: #94a3b8; max-width: 600px; margin: 0 auto 2rem;">
        We are actively looking to build and partner with local groups (Young Democrats, Texas Democratic Women, Stonewall Democrats, Tejano Democrats). Need to create groups like these and put the links here.
      </p>
      <p style="font-size: 1.25rem; color: white; background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; display: inline-block;">
        Please reach out to the webmaster at <strong style="color: var(--accent);">info@hidalgocountydems.org</strong> to officially register your affiliated club or organization.
      </p>
    </div>
  </main>
"""

# 2. events.html
events_content = """
  <header class="page-header container fade-in" style="padding: 4rem 2rem;">
    <h1>Upcoming Events</h1>
    <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">A unified calendar of County Executive Committee meetings, block walks, and community events.</p>
  </header>
  <main class="container fade-in" style="min-height: 50vh; margin-bottom: 4rem;">
    <div class="glass-card" style="padding: 2rem; text-align: center;">
      <h3 style="margin-bottom: 2rem; color: white;">Unified Events Calendar</h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; text-align: left;">
        
        <!-- Placeholder Event 1 -->
        <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--accent);">
          <div style="color: var(--accent); font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.5rem;">March 15, 2026 - 6:00 PM</div>
          <h4 style="color: white; margin-bottom: 0.5rem;">County Executive Committee Meeting</h4>
          <p style="color: #94a3b8; font-size: 0.9rem;">Hidalgo County Democratic HQ. Open to all Precinct Chairs and interested public.</p>
        </div>

        <!-- Placeholder Event 2 -->
        <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #34d399;">
          <div style="color: #34d399; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.5rem;">April 2, 2026 - 9:00 AM</div>
          <h4 style="color: white; margin-bottom: 0.5rem;">Weekend Block Walk</h4>
          <p style="color: #94a3b8; font-size: 0.9rem;">McAllen Public Library. Join us targeting high-propensity Democratic households.</p>
        </div>

      </div>
    </div>
  </main>
"""

# 3. election_workers.html
workers_content = """
  <header class="page-header container fade-in" style="padding: 4rem 2rem;">
    <h1>Become an Election Worker</h1>
    <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">Democracy runs on people. Step up to serve your community by staffing the polls during early voting and Election Day.</p>
  </header>
  <main class="container fade-in" style="min-height: 50vh; margin-bottom: 4rem;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
      <div class="glass-card" style="padding: 2.5rem;">
        <h2 style="color: white; margin-bottom: 1.5rem;">Election Judges & Clerks Needed</h2>
        <p style="color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6;">
          Hidalgo County is always looking for dedicated citizens to manage our polling locations. Election Judges are the officials in charge of a polling site, ensuring fair access and security. Election Clerks assist with checking in voters and managing lines.
        </p>
        <ul style="color: #94a3b8; padding-left: 1.5rem; margin-bottom: 2rem;">
          <li style="margin-bottom: 0.5rem;">Paid positions managed directly by Hidalgo County Elections Dept.</li>
          <li style="margin-bottom: 0.5rem;">Mandatory paid training provided prior to elections.</li>
          <li style="margin-bottom: 0.5rem;">Bilingual (English/Spanish) applicants highly encouraged!</li>
        </ul>
        <a href="https://www.hidalgocounty.us/105/Elections-Department" target="_blank" class="btn btn-primary" style="display: inline-block;">Apply via Hidalgo County Jobs &rarr;</a>
      </div>
      
      <div class="glass-card" style="padding: 2.5rem; background: rgba(34, 211, 238, 0.05); border-color: rgba(34, 211, 238, 0.2);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🇺🇸</div>
        <h3 style="color: white; margin-bottom: 1rem;">Why It Matters</h3>
        <p style="color: #cbd5e1; line-height: 1.6;">
          By working the elections, you are the front-line defense for voter access. You ensure that our neighbors wait in shorter lines, experience fewer technical issues, and find friendly faces when they arrive to exercise their constitutional rights.
        </p>
      </div>
    </div>
  </main>
"""

# 4. run_for_office.html
run_content = """
  <header class="page-header container fade-in" style="padding: 4rem 2rem;">
    <h1>Run For Local Office</h1>
    <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">Don't just vote. Lead. Find everything you need to file as a Democratic candidate in Hidalgo County.</p>
  </header>
  <main class="container fade-in" style="min-height: 50vh; margin-bottom: 4rem;">
    
    <div class="glass-card" style="padding: 2.5rem; margin-bottom: 2rem; border-left: 4px solid var(--accent);">
      <h2 style="color: white; margin-bottom: 1rem;">Candidate Filing Period</h2>
      <p style="color: #cbd5e1; font-size: 1.1rem;">
        The filing window to run as a Democrat in the upcoming Primary Election is strictly enforced by state law. You must submit your filing application and fee (or petition in lieu of fee) to the County Chair by the deadline.
      </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
      <div class="glass-card" style="padding: 2rem;">
        <h3 style="color: white; margin-bottom: 1rem;">1. Determine Eligibility</h3>
        <p style="color: #94a3b8; margin-bottom: 1rem; line-height: 1.5;">Check the Texas SOS guidelines for the office you seek. Requirements vary for age, residency, and professional licensure (e.g., district judges).</p>
        <a href="https://www.sos.state.tx.us/elections/candidates/guide/2026/index.shtml" target="_blank" style="color: var(--accent); font-weight: 600;">View SOS Qualifications &rarr;</a>
      </div>

      <div class="glass-card" style="padding: 2rem;">
        <h3 style="color: white; margin-bottom: 1rem;">2. Campaign Finance</h3>
        <p style="color: #94a3b8; margin-bottom: 1rem; line-height: 1.5;">Before raising a single dollar, you must designate a Campaign Treasurer using Form CTA filed with the appropriate Ethics Commission authority.</p>
        <a href="https://www.ethics.state.tx.us/forms/coh/" target="_blank" style="color: var(--accent); font-weight: 600;">Download Form CTA &rarr;</a>
      </div>

      <div class="glass-card" style="padding: 2rem;">
        <h3 style="color: white; margin-bottom: 1rem;">3. Official Filing Application</h3>
        <p style="color: #94a3b8; margin-bottom: 1rem; line-height: 1.5;">Complete the official Application for a Place on the Primary Ballot. This must be notarized and submitted directly to the Hidalgo County Democratic Party Chair.</p>
        <a href="https://www.sos.state.tx.us/elections/forms/pol-sub/2-2f.pdf" target="_blank" style="color: var(--accent); font-weight: 600;">Download SOS Filing Form &rarr;</a>
      </div>
    </div>

  </main>
"""

pages = {
    'clubs.html': clubs_content,
    'events.html': events_content,
    'election_workers.html': workers_content,
    'run_for_office.html': run_content
}

for filename, content in pages.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{head}\n{nav}\n{content}\n{footer}")

print("Successfully created the 4 foundation HTML pages.")
