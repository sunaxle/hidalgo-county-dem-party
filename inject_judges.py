import json

def get_icon(office_full):
    if "Justice of the Peace" in office_full:
        return "🕊️"
    elif "Court" in office_full:
        return "⚖️"
    return "🏛️"

# Load JSON
with open('data/judicial_candidates_and_officials.json', 'r') as f:
    officials = json.load(f)

# Build HTML for new tab
cards_html = []
for off in officials:
    name = f"{off['first_name']} {off['last_name']}"
    title = off['office_full']
    icon = get_icon(title)
    
    card = f"""
        <div class="official-card">
          <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; border-radius: 50%; background: #334155; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">{icon}</div>
            <div>
              <span class="party-badge badge-dem">Democrat</span>
              <h3 class="official-name" style="font-size: 1.25rem;">{name}</h3>
            </div>
          </div>
          <p class="official-title">{title}</p>
        </div>"""
    cards_html.append(card)

new_tab_content = f"""
    <!-- Local & Judicial Tab -->
    <div class="tab-content" id="tab-local">
      <div class="grid-3">
{''.join(cards_html)}
      </div>
    </div>
"""

with open('elected_officials.html', 'r') as f:
    html = f.read()

# Add button
button_target = '<button class="tab-btn" data-target="tab-state">Texas Legislature</button>'
button_new = '<button class="tab-btn" data-target="tab-state">Texas Legislature</button>\n      <button class="tab-btn" data-target="tab-local">Judicial &amp; Local</button>'

if button_new not in html:
    html = html.replace(button_target, button_new)

# Add tab content right before the </section> after tab-state
end_section = "  </section>"
if 'id="tab-local"' not in html:
    html = html.replace(end_section, new_tab_content + "\n" + end_section)

with open('elected_officials.html', 'w') as f:
    f.write(html)

print("Injected judges into elected_officials.html")
