import re

with open('home.html', 'r', encoding='utf-8') as f:
    html = f.read()

head_match = re.search(r'(<!DOCTYPE html>.*?<body class="tx-clone">)', html, re.DOTALL)
nav_match = re.search(r'(<nav class="tx-clone-nav">.*?<div class="tx-clone-nav-accent-bar"></div>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="tx-clone-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1) if head_match else ""
nav = nav_match.group(1) if nav_match else ""
footer = footer_match.group(1) if footer_match else ""

van_help_content = """
  <!-- Background Image Wrapper -->
  <div style="background-image: linear-gradient(rgba(0, 45, 84, 0.85), rgba(0, 45, 84, 0.95)), url('images/hidalgo-exterior-d2100-675.avif'); background-size: cover; background-position: center; min-height: 80vh; padding-bottom: 4rem;">
      <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">
        <h1 style="color: white; font-size: 3.5rem; text-transform: uppercase;">VAN Support Pipeline</h1>
        <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">A dedicated technical support hub for Precinct Chairs and Candidates using the Texas Democratic Voter File.</p>
      </header>
      <main class="container fade-in" style="max-width: 800px; padding: 0 2rem;">
          <div style="background: white; border-radius: 8px; padding: 3rem; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
              <h2 style="color: var(--tx-navy); margin-bottom: 2rem;">Submit a Technical Ticket</h2>
              <form>
                  <div style="margin-bottom: 1.5rem; text-align: left;">
                      <label style="color: var(--tx-navy); font-weight: 600; display: block; margin-bottom: 0.5rem;">Your Name & Precinct</label>
                      <input type="text" placeholder="Jane Doe, Pct 143" style="width: 100%; padding: 1rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;" required>
                  </div>
                  <div style="margin-bottom: 1.5rem; text-align: left;">
                      <label style="color: var(--tx-navy); font-weight: 600; display: block; margin-bottom: 0.5rem;">Issue Type</label>
                      <select style="width: 100%; padding: 1rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;">
                          <option>MiniVAN Canvassing App</option>
                          <option>Cutting Turf / Lists</option>
                          <option>Login / Password Reset</option>
                          <option>Virtual Phone Bank</option>
                          <option>Other</option>
                      </select>
                  </div>
                  <div style="margin-bottom: 1.5rem; text-align: left;">
                      <label style="color: var(--tx-navy); font-weight: 600; display: block; margin-bottom: 0.5rem;">Describe The Issue</label>
                      <textarea placeholder="I keep getting an error when I try to sync my MiniVAN app..." style="width: 100%; padding: 1rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; min-height: 150px;" required></textarea>
                  </div>
                  <button type="submit" style="background: var(--tx-orange); color: white; border: none; padding: 1.25rem 2rem; font-size: 1.15rem; font-weight: 800; border-radius: 4px; cursor: pointer; width: 100%; text-transform: uppercase;">Submit Ticket</button>
              </form>
          </div>
      </main>
  </div>
"""

press_content = """
  <div style="background-color: #f8fafc; min-height: 80vh; padding-bottom: 4rem;">
      <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">
          <h1 style="color: var(--tx-navy); font-size: 3.5rem; text-transform: uppercase;">Press & Media</h1>
          <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #475569;">Official statements, press releases, and commentary from the Hidalgo County Democratic Party.</p>
      </header>
      <main class="container fade-in" style="max-width: 1000px; padding: 0 2rem;">
          
          <div style="display: flex; flex-direction: column; gap: 2rem;">
              <!-- Article 1 -->
              <div style="background: white; border-radius: 8px; padding: 2rem; border-left: 6px solid var(--tx-sky); box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                  <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 600;">MAY 1, 2026 • OFFICIAL STATEMENT</p>
                  <h3 style="color: var(--tx-navy); font-size: 1.5rem; margin-bottom: 1rem;">Hidalgo County Democrats Stand With LUPE's "Marcha del Pueblo"</h3>
                  <p style="color: #475569; line-height: 1.6; margin-bottom: 1.5rem;">For over twenty years, LUPE has organized the annual Marcha del Pueblo. The Hidalgo County Democratic Party proudly stands with working families advocating for fair wages and comprehensive infrastructure across the Rio Grande Valley...</p>
                  <a href="#" style="color: var(--tx-sky); font-weight: 800; text-decoration: none;">Read Full Statement ➔</a>
              </div>

              <!-- Article 2 -->
              <div style="background: white; border-radius: 8px; padding: 2rem; border-left: 6px solid var(--tx-sky); box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                  <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 600;">APRIL 14, 2026 • PRESS RELEASE</p>
                  <h3 style="color: var(--tx-navy); font-size: 1.5rem; margin-bottom: 1rem;">Voter Protection Task Force Officially Activated for 2026 Midterms</h3>
                  <p style="color: #475569; line-height: 1.6; margin-bottom: 1.5rem;">Ensuring the right to vote remains the cornerstone of our democracy. Today, the local party announces the rollout of its dedicated emergency issue reporting pipeline...</p>
                  <a href="#" style="color: var(--tx-sky); font-weight: 800; text-decoration: none;">Read Full Statement ➔</a>
              </div>
          </div>
      </main>
  </div>
"""

internships_content = """
  <div style="background-image: linear-gradient(rgba(0, 45, 84, 0.85), rgba(0, 45, 84, 0.95)), url('images/hidalgo-exterior-d2100-675.avif'); background-size: cover; background-position: center; min-height: 80vh; padding-bottom: 4rem;">
      <header class="page-header container fade-in" style="text-align: center; padding: 4rem 2rem;">
          <h1 style="color: white; font-size: 3.5rem; text-transform: uppercase;">Work With Us</h1>
          <p style="max-width: 800px; margin: 0 auto; font-size: 1.15rem; color: #cbd5e1;">Join a movement that matters. Explore fellowships, internships, and staff opportunities with the Hidalgo County Dem Party.</p>
      </header>
      <main class="container fade-in" style="max-width: 1000px; padding: 0 2rem;">
          
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
              
              <!-- Fellowship -->
              <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 2.5rem; backdrop-filter: blur(10px);">
                  <span style="background: var(--tx-sky); color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">SUMMER 2026</span>
                  <h3 style="color: white; font-size: 1.5rem; margin-top: 1.5rem; margin-bottom: 1rem;">Organizing Fellowship</h3>
                  <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 2rem;">A 10-week intensive program for college students looking to learn grassroots field organizing, voter persuasion, and digital campaign strategy.</p>
                  <a href="#" style="display: block; text-align: center; background: white; color: var(--tx-navy); padding: 1rem; border-radius: 4px; font-weight: 800; text-decoration: none;">Apply Now</a>
              </div>

              <!-- Internship -->
              <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 2.5rem; backdrop-filter: blur(10px);">
                  <span style="background: var(--tx-orange); color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">FALL 2026</span>
                  <h3 style="color: white; font-size: 1.5rem; margin-top: 1.5rem; margin-bottom: 1rem;">Data & Analytics Intern</h3>
                  <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 2rem;">Work directly with the VAN database to model electorate targets, process precinct files, and assist the County Chair in executing direct communication campaigns.</p>
                  <a href="#" style="display: block; text-align: center; background: white; color: var(--tx-navy); padding: 1rem; border-radius: 4px; font-weight: 800; text-decoration: none;">Apply Now</a>
              </div>

              <!-- Local Paid Role -->
              <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 2.5rem; backdrop-filter: blur(10px);">
                  <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">STANDING NOFO</span>
                  <h3 style="color: white; font-size: 1.5rem; margin-top: 1.5rem; margin-bottom: 1rem;">Election Clerks</h3>
                  <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 2rem;">We are continuously recruiting paid election workers, alternate judges, and ballot board members directly to the Hidalgo County Elections Dept.</p>
                  <a href="election_workers.html" style="display: block; text-align: center; background: white; color: var(--tx-navy); padding: 1rem; border-radius: 4px; font-weight: 800; text-decoration: none;">See Details</a>
              </div>

          </div>

      </main>
  </div>
"""

with open('van_help.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{van_help_content}\n{footer}")

with open('press.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{press_content}\n{footer}")

with open('internships.html', 'w', encoding='utf-8') as f:
    f.write(f"{head}\n{nav}\n{internships_content}\n{footer}")

print("Successfully compiled van_help.html, press.html, and internships.html")

