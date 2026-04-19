import re

with open('home.html', 'r', encoding='utf-8') as f:
    html = f.read()

head_match = re.search(r'(<!DOCTYPE html>.*?<body class="tx-clone">)', html, re.DOTALL)
nav_match = re.search(r'(<nav class="tx-clone-nav">.*?<div class="tx-clone-nav-accent-bar"></div>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="tx-clone-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1) if head_match else ""
nav = nav_match.group(1) if nav_match else ""
footer = footer_match.group(1) if footer_match else ""

vbm_content = """
  <!-- Background Image Wrapper for Light Text Readability -->
  <div style="background-image: linear-gradient(rgba(0, 45, 84, 0.85), rgba(0, 45, 84, 0.95)), url('images/hidalgo-exterior-d2100-675.avif'); background-size: cover; background-position: center; min-height: 80vh; padding-bottom: 4rem;">
      <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">
        <h1 style="color: white; font-size: 3.5rem; text-transform: uppercase;">Vote By Mail</h1>
        <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">A step-by-step guide to securing your Mail-In Ballot in Hidalgo County.</p>
      </header>
      
      <main class="container fade-in" style="margin-bottom: 4rem; max-width: 1000px; padding: 0 2rem;">
        
        <!-- Info Banner -->
        <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 2rem; border-radius: 8px; margin-bottom: 3rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h4 style="color: #fca5a5; margin-bottom: 0.5rem; font-size: 1.25rem;">⚠️ Important Notice Regarding Signatures</h4>
            <p style="color: #f1f5f9; font-size: 1.05rem; line-height: 1.6;">
                <strong>Electronic signatures are NOT permitted.</strong> Your application must contain an original, wet-ink signature. If you submit your application via email or fax, you <strong style="color: white; text-decoration: underline;">must also mail the original hardcopy</strong> to the Hidalgo County Early Voting Clerk so that it is received no later than the 4th business day after your electronic submission.
            </p>
        </div>

        <!-- 1. Eligibility -->
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 2.5rem; margin-bottom: 2rem; backdrop-filter: blur(10px);">
          <h2 style="color: white; margin-bottom: 1.5rem;">1. Check Your Eligibility</h2>
          <p style="color: #cbd5e1; margin-bottom: 1rem; line-height: 1.6; font-size: 1.1rem;">
            To be eligible to vote early by mail in Texas, you must meet at least one of the following criteria:
          </p>
          <ul style="color: #e2e8f0; padding-left: 1.5rem; line-height: 1.8; margin-bottom: 1rem; font-size: 1.05rem;">
            <li><strong style="color: #38bdf8;">65 Years of Age or Older:</strong> You will be 65 or older on Election Day.</li>
            <li><strong style="color: #38bdf8;">Sick or Disabled:</strong> You have a sickness or physical condition that prevents you from appearing at the polling place on Election Day without a likelihood of needing personal assistance or of injuring your health.</li>
            <li><strong style="color: #38bdf8;">Expected Absence:</strong> You will be absent from Hidalgo County during both the early voting period and on Election Day.</li>
            <li><strong style="color: #38bdf8;">Confined in Jail:</strong> You are confined in jail, but otherwise eligible.</li>
          </ul>
        </div>

        <!-- 2. Application Download -->
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid var(--tx-orange); border-radius: 8px; padding: 2.5rem; margin-bottom: 2rem; backdrop-filter: blur(10px);">
          <h2 style="color: white; margin-bottom: 1.5rem;">2. Download & Print the Application</h2>
          <p style="color: #cbd5e1; margin-bottom: 2rem; line-height: 1.6; font-size: 1.1rem;">
            Download the official Application for a Ballot By Mail (ABBM). Print the document, fill it out completely, and sign it with an ink pen.
          </p>
          <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <a href="https://www.sos.texas.gov/elections/voter/reqabbm.shtml" target="_blank" style="background: var(--tx-orange); color: white; padding: 1rem 2rem; font-weight: 800; text-transform: uppercase; text-decoration: none; border-radius: 4px; display: inline-block;">Download Form (English) ➔</a>
            <a href="https://www.sos.texas.gov/elections/voter/reqabbm.shtml" target="_blank" style="background: transparent; border: 2px solid rgba(255,255,255,0.4); color: white; padding: 1rem 2rem; font-weight: 800; text-transform: uppercase; text-decoration: none; border-radius: 4px; display: inline-block;">Descargar Formulario (Español) ➔</a>
          </div>
        </div>

        <!-- 3. Submission -->
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid var(--tx-sky); border-radius: 8px; padding: 2.5rem; margin-bottom: 2rem; backdrop-filter: blur(10px);">
          <h2 style="color: white; margin-bottom: 1.5rem;">3. Submit Your Application</h2>
          <p style="color: #cbd5e1; margin-bottom: 2rem; line-height: 1.6; font-size: 1.1rem;">
            Once your application is completed and signed, you must submit it directly to the Hidalgo County Elections Department.
          </p>
          
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
            
            <div>
                <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1.25rem;">📬 By Mail</h4>
                <p style="color: #94a3b8; line-height: 1.6; font-size: 1.05rem;">
                    Hidalgo County Elections Dept.<br>
                    P.O. Box 659<br>
                    Edinburg, TX 78540-0659
                </p>
            </div>

            <div>
                <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1.25rem;">📧 By Email</h4>
                <p style="color: #94a3b8; line-height: 1.6; font-size: 1.05rem;">
                    <a href="mailto:elections@co.hidalgo.tx.us" style="color: #38bdf8; text-decoration: underline;">elections@co.hidalgo.tx.us</a><br>
                    <em style="color: #ef4444;">(Must also mail original within 4 days)</em>
                </p>
            </div>

            <div>
                <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1.25rem;">🖨️ By Fax</h4>
                <p style="color: #94a3b8; line-height: 1.6; font-size: 1.05rem;">
                    956-393-2039<br>
                    <em style="color: #ef4444;">(Must also mail original within 4 days)</em>
                </p>
            </div>

          </div>
        </div>

      </main>
  </div>
"""

with open('vbm.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{vbm_content}\n{footer}")

print("vbm.html styling repaired for global white theme.")
