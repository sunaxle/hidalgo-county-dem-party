import re

# Read template file
with open('home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract segments
head_match = re.search(r'(<!DOCTYPE html>.*?<body class="tx-clone">)', html, re.DOTALL)
nav_match = re.search(r'(<!-- Dynamic Background Shapes -->.*?<div class="tx-clone-nav-accent-bar"></div>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="tx-clone-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1) if head_match else ""
nav = nav_match.group(1) if nav_match else ""
footer = footer_match.group(1) if footer_match else ""

vbm_content = """
  <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">
    <h1>Vote By Mail</h1>
    <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">A step-by-step guide to securing your Mail-In Ballot in Hidalgo County.</p>
  </header>
  
  <main class="container fade-in" style="min-height: 50vh; margin-bottom: 4rem; max-width: 1000px;">
    
    <!-- Info Banner -->
    <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 1.5rem; border-radius: 4px; margin-bottom: 3rem;">
        <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1.1rem;">⚠️ Important Notice Regarding Signatures</h4>
        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
            <strong>Electronic signatures are NOT permitted.</strong> Your application must contain an original, wet-ink signature. If you submit your application via email or fax, you <strong>must also mail the original hardcopy</strong> to the Hidalgo County Early Voting Clerk so that it is received no later than the 4th business day after your electronic submission.
        </p>
    </div>

    <!-- 1. Eligibility -->
    <div class="glass-card" style="padding: 2.5rem; margin-bottom: 2rem;">
      <h2 style="color: white; margin-bottom: 1.5rem;">1. Check Your Eligibility</h2>
      <p style="color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6;">
        To be eligible to vote early by mail in Texas, you must meet at least one of the following criteria:
      </p>
      <ul style="color: #94a3b8; padding-left: 1.5rem; line-height: 1.8; margin-bottom: 1rem;">
        <li><strong style="color: white;">65 Years of Age or Older:</strong> You will be 65 or older on Election Day.</li>
        <li><strong style="color: white;">Sick or Disabled:</strong> You have a sickness or physical condition that prevents you from appearing at the polling place on Election Day without a likelihood of needing personal assistance or of injuring your health.</li>
        <li><strong style="color: white;">Expected Absence:</strong> You will be absent from Hidalgo County during both the early voting period and on Election Day.</li>
        <li><strong style="color: white;">Confined in Jail:</strong> You are confined in jail, but otherwise eligible.</li>
      </ul>
    </div>

    <!-- 2. Application Download -->
    <div class="glass-card" style="padding: 2.5rem; margin-bottom: 2rem; border-color: var(--accent);">
      <h2 style="color: white; margin-bottom: 1.5rem;">2. Download & Print the Application</h2>
      <p style="color: #cbd5e1; margin-bottom: 2rem; line-height: 1.6;">
        Download the official Application for a Ballot By Mail (ABBM). Print the document, fill it out completely, and sign it with an ink pen.
      </p>
      <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <a href="https://www.sos.texas.gov/elections/voter/reqabbm.shtml" target="_blank" class="btn btn-primary" style="background: var(--accent); color: white;">Download Form (English) ➔</a>
        <a href="https://www.sos.texas.gov/elections/voter/reqabbm.shtml" target="_blank" class="btn btn-primary" style="background: transparent; border: 1px solid rgba(255,255,255,0.2); color: white;">Descargar Formulario (Español) ➔</a>
      </div>
    </div>

    <!-- 3. Submission -->
    <div class="glass-card" style="padding: 2.5rem; margin-bottom: 2rem;">
      <h2 style="color: white; margin-bottom: 1.5rem;">3. Submit Your Application</h2>
      <p style="color: #cbd5e1; margin-bottom: 2rem; line-height: 1.6;">
        Once your application is completed and signed, you must submit it directly to the Hidalgo County Elections Department.
      </p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
        
        <div>
            <h4 style="color: var(--accent); margin-bottom: 0.5rem; font-size: 1.1rem;">📬 By Mail</h4>
            <p style="color: #94a3b8; line-height: 1.6; font-size: 0.95rem;">
                Hidalgo County Elections Dept.<br>
                P.O. Box 659<br>
                Edinburg, TX 78540-0659
            </p>
        </div>

        <div>
            <h4 style="color: var(--accent); margin-bottom: 0.5rem; font-size: 1.1rem;">📧 By Email</h4>
            <p style="color: #94a3b8; line-height: 1.6; font-size: 0.95rem;">
                <a href="mailto:elections@co.hidalgo.tx.us" style="color: inherit; text-decoration: underline;">elections@co.hidalgo.tx.us</a><br>
                <em>(Must also mail original within 4 days)</em>
            </p>
        </div>

        <div>
            <h4 style="color: var(--accent); margin-bottom: 0.5rem; font-size: 1.1rem;">🖨️ By Fax</h4>
            <p style="color: #94a3b8; line-height: 1.6; font-size: 0.95rem;">
                956-393-2039<br>
                <em>(Must also mail original within 4 days)</em>
            </p>
        </div>

      </div>
    </div>

  </main>
"""

with open('vbm.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{vbm_content}\n{footer}")

print("vbm.html generation complete.")
