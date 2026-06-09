import re

with open("press.html", encoding="utf-8") as f:
    html = f.read()

article_html = """
              <!-- Article New -->
              <div style="background: white; border-radius: 8px; padding: 2rem; border-left: 6px solid var(--tx-sky); box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                  <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                      <p style="color: #64748b; font-size: 0.9rem; font-weight: 600;">JUNE 5, 2026 • PRESS RELEASE</p>
                      <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 0.3rem 0.8rem; border-radius: 99px; font-size: 0.8rem; font-weight: 800; letter-spacing: 0.5px;">PRESS RELEASE</span>
                  </div>
                  <h3 style="color: var(--tx-navy); font-size: 1.5rem; margin-bottom: 1rem;">The Road to 500k: The Ultimate Voter Registration Drive</h3>
                  <p style="color: #475569; line-height: 1.6; margin-bottom: 1.5rem;">Hidalgo County is the beating heart of South Texas, and our political power lies in our numbers. Today, the Hidalgo County Democratic Party is officially launching the "Road to 500k" Voter Registration Drive with the bold goal of reaching half a million registered voters.</p>
                  <a href="road_to_500k_press_release.html" style="color: var(--tx-sky); font-weight: 800; text-decoration: none;">Read Full Statement ➔</a>
              </div>
"""

# Find where <!-- Article 0 --> starts
html = html.replace(
    "<!-- Article 0 -->", article_html + "\n              <!-- Article 0 -->"
)

with open("press.html", "w", encoding="utf-8") as f:
    f.write(html)
print("press.html updated.")
