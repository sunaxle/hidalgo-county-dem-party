import json

with open('data/master_candidates_2026.json') as f:
    candidates = json.load(f)

# we need to build the statewide/federal list which is:
# James Talarico, Colin Allred, Bobby Pulido, Henry Cuellar, Gina Hinojosa, Vicki Goodwin, Joe Jaworski, Nathan Johnson,
# Clayton Tucker, Thomas Garcia, Oscar Longoria, Sergio Munoz Jr, Armando Martinez, Terry Canales, Eric Holguin, Seby Haddad, Julio Salinas

# Wait, let's just wipe out the `tab-federal` and `tab-state` and rebuild them perfectly based on the provided list!

congress_offices = ["U.S. Senator", "CD 15", "CD 28"]
state_offices = ["Governor", "Lieutenant Governor", "Attorney General", "Comptroller", "GLO Commissioner", "Ag Commissioner", "RR Commissioner", "SBOE District 2", "SBOE District 3", "State Senator District 27", "State Rep District 35", "State Rep District 36", "State Rep District 39", "State Rep District 40", "State Rep District 41"]
local_offices = ["206th JD", "275th JD", "370th JD", "Criminal District Attorney", "County Judge", "District Clerk", "County Clerk", "County Treasurer", "County Comm Pct 2", "County Comm Pct 4", "Constable Pct 5", "CCL 1", "CCL 2", "CCL 4", "CCL 5", "CCL 6", "CCL 8", "Probate Court 1", "Probate Court 2", "JP 1, Place 2", "JP 2, Place 1", "JP 2, Place 2", "JP 3, Place 2", "JP 4, Place 2", "JP 5/1"]

def get_icon(office_full):
    if "Senator" in office_full or "CD " in office_full:
        return "🇺🇸"
    elif "Governor" in office_full or "General" in office_full or "Commissioner" in office_full or "SBOE" in office_full:
        return "⭐"
    elif "State Rep" in office_full or "State Senator" in office_full:
        return "🤠"
    elif "JP" in office_full or "Constable" in office_full:
        return "🕊️"
    elif "Court" in office_full or "CCL" in office_full or "JD" in office_full or "Attorney" in office_full or "Judge" in office_full or "Clerk" in office_full:
        return "⚖️"
    elif "Treasurer" in office_full or "Comm" in office_full:
        return "🏛️"
    return "🏛️"

def build_cards(category_list):
    cards = []
    for cd in candidates:
        if any(cd['office'].startswith(prefix) for prefix in category_list):
            name = f"{cd['first_name']} {cd['last_name']}".strip()
            if not name:
                continue
            icon = get_icon(cd['office'])
            
            links_html = ""
            if cd['email']:
                links_html += f'<a href="mailto:{cd["email"]}">{cd["email"]}</a>'
            if cd['phone']:
                links_html += f'<a href="tel:{cd["phone"]}">{cd["phone"]}</a>'
                
            links_section = ""
            if links_html:
                links_section = f'<div class="official-links" style="margin-top: 0.5rem;">{links_html}</div>'

            card = f"""
        <div class="official-card">
          <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; border-radius: 50%; background: #334155; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">{icon}</div>
            <div>
              <span class="party-badge badge-dem">Democrat</span>
              <h3 class="official-name" style="font-size: 1.25rem;">{name}</h3>
            </div>
          </div>
          <p class="official-title">{cd['office']}</p>
          {links_section}
        </div>"""
            cards.append(card)
    return cards

fed_cards = build_cards(congress_offices)
state_cards = build_cards(state_offices)
local_cards = build_cards(local_offices)

new_fed = f"""    <!-- U.S. Congress Tab -->
    <div class="tab-content active" id="tab-federal">
      <div class="grid-3">
{''.join(fed_cards)}
      </div>
    </div>"""

new_state = f"""    <!-- Texas Legislature Tab -->
    <div class="tab-content" id="tab-state">
      <div class="grid-3">
{''.join(state_cards)}
      </div>
    </div>"""

new_local = f"""    <!-- Local & Judicial Tab -->
    <div class="tab-content" id="tab-local">
      <div class="grid-3">
{''.join(local_cards)}
      </div>
    </div>"""


import re

with open('elected_officials.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<!-- U\.S\. Congress Tab -->\s*<div class="tab-content(?:\s+active)?" id="tab-federal">.*?</div>\s*</div>', new_fed, html, flags=re.DOTALL)
html = re.sub(r'<!-- Texas Legislature Tab -->\s*<div class="tab-content" id="tab-state">.*?</div>\s*</div>', new_state, html, flags=re.DOTALL)
html = re.sub(r'<!-- Local & Judicial Tab -->\s*<div class="tab-content" id="tab-local">.*?</div>\s*</div>', new_local, html, flags=re.DOTALL)

with open('elected_officials.html', 'w', encoding='utf-8') as f:
    f.write(html)
