import re

with open('home.html', 'r', encoding='utf-8') as f:
    html = f.read()

head_match = re.search(r'(<!DOCTYPE html>.*?<body class="tx-clone">)', html, re.DOTALL)
nav_match = re.search(r'(<nav class="tx-clone-nav">.*?<div class="tx-clone-nav-accent-bar"></div>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="tx-clone-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1) if head_match else ""
nav = nav_match.group(1) if nav_match else ""
footer = footer_match.group(1) if footer_match else ""

protect_content = """
  <!-- Visually Urgent Red/Black Background to indicate crisis/importance -->
  <div style="background-color: white; border-top: 10px solid #ef4444; min-height: 80vh; padding-bottom: 4rem;">
      <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem 2rem 2rem;">
        <h1 style="color: var(--tx-navy); font-size: 3.5rem; text-transform: uppercase;">Protect The Vote</h1>
        <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #475569;">If you experience intimidation, machine failures, or are turned away at the polls—report it immediately.</p>
      </header>
      
      <main class="container fade-in" style="margin-bottom: 4rem; max-width: 1000px; padding: 0 2rem;">
        
        <!-- Emergency Crisis Banner -->
        <div style="background: var(--tx-navy); border-left: 8px solid #ef4444; padding: 3rem; border-radius: 8px; margin-bottom: 3rem; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
            <h2 style="color: white; margin-bottom: 0.5rem; font-size: 2rem;">🚨 STATEWIDE DEMOCRATIC HOTLINE</h2>
            <p style="color: #cbd5e1; font-size: 1.15rem; line-height: 1.6; margin-bottom: 1.5rem;">
                Don't leave the polling place without casting a ballot. If you have questions about your ID, registration, or your rights, call the legal team right now.
            </p>
            <a href="tel:18448986837" style="display: inline-block; background: #ef4444; color: white; padding: 1.5rem 3rem; font-size: 2.5rem; font-weight: 800; text-decoration: none; border-radius: 8px; letter-spacing: 2px;">1-844-TX-VOTES</a>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 2rem; margin-bottom: 3rem;">
            
            <!-- Alternate Hotlines -->
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 2.5rem;">
                <h3 style="color: var(--tx-navy); margin-bottom: 1.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem;">Non-Partisan Support Lines</h3>
                
                <div style="margin-bottom: 1.5rem;">
                    <h4 style="color: var(--tx-orange); margin-bottom: 0.2rem;">Español (Ve y Vota)</h4>
                    <a href="tel:18888398682" style="font-size: 1.25rem; color: var(--tx-navy); font-weight: 600; text-decoration: none;">1-888-839-8682</a>
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <h4 style="color: var(--tx-sky); margin-bottom: 0.2rem;">Disability Rights Texas</h4>
                    <a href="tel:18887968683" style="font-size: 1.25rem; color: var(--tx-navy); font-weight: 600; text-decoration: none;">1-888-796-VOTE (8683)</a>
                </div>
                
                <div style="margin-bottom: 1.5rem;">
                    <h4 style="color: #10b981; margin-bottom: 0.2rem;">English (ACLU / Election Protect)</h4>
                    <a href="tel:18666878683" style="font-size: 1.25rem; color: var(--tx-navy); font-weight: 600; text-decoration: none;">1-866-OUR-VOTE (8683)</a>
                </div>
            </div>

            <!-- Know Your Rights -->
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 2.5rem;">
                <h3 style="color: var(--tx-navy); margin-bottom: 1.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem;">Know Your Rights Checklist</h3>
                <ul style="color: #334155; line-height: 1.8; padding-left: 1.5rem;">
                    <li style="margin-bottom: 0.75rem;"><strong>STAY IN LINE.</strong> If you are in line before the polls close at 7:00 PM, you legally must be allowed to vote.</li>
                    <li style="margin-bottom: 0.75rem;">If your name isn't on the list, immediately ask the clerk to search the statewide database.</li>
                    <li style="margin-bottom: 0.75rem;">If you forgot your Photo ID, ask to fill out a <strong>Reasonable Impediment Declaration</strong> and cast a regular ballot using a supporting document (like a utility bill).</li>
                    <li style="margin-bottom: 0.75rem;">Do not accept a provisional ballot unless a judge forces you. Provisional ballots are a last resort.</li>
                </ul>
            </div>

        </div>

      </main>
  </div>
"""

with open('protect.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{protect_content}\n{footer}")

print("Voter protection (protect.html) layout isolated and pre-compiled based on the plan.")
