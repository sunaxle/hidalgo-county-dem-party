import re

# 1. Update js/precinct_hub.js for warning on cards
with open('js/precinct_hub.js', 'r', encoding='utf-8') as f:
    hub_js = f.read()

# We look for the <div ... Precinct ${chair.precinct}</div>
card_html_replace = """<div style="color: #94a3b8; font-size: 0.95rem; font-weight: 600; position: relative; z-index: 2;">Precinct ${chair.precinct}</div>
                    ${(cd15List.includes(parseInt(chair.precinct)) && cd28List.includes(parseInt(chair.precinct))) ? '<div style="color: #ea580c; font-size: 0.8rem; font-weight: 700; margin-top: 0.25rem;">⚠️ Split District</div>' : ''}"""

hub_js = hub_js.replace('<div style="color: #94a3b8; font-size: 0.95rem; font-weight: 600; position: relative; z-index: 2;">Precinct ${chair.precinct}</div>', card_html_replace)

with open('js/precinct_hub.js', 'w', encoding='utf-8') as f:
    f.write(hub_js)


# 2. Update hidalgo-election-map/map_chairs.js for popup
with open('hidalgo-election-map/map_chairs.js', 'r', encoding='utf-8') as f:
    map_js = f.read()

# Look for <h3 style="margin-top:0; color:#0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 5px;">Precinct ${cleanPct || 'Unknown'}</h3>
popup_replace = """<h3 style="margin-top:0; color:#0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 5px;">Precinct ${cleanPct || 'Unknown'}</h3>`;
        
        // Add split precinct warning if it falls into both districts
        if (window.cd15List && window.cd28List && cleanPct) {
            let pInt = parseInt(cleanPct, 10);
            if (window.cd15List.includes(pInt) && window.cd28List.includes(pInt)) {
                popupContent += `<div style="background: rgba(234, 88, 12, 0.1); border: 1px solid #ea580c; color: #ea580c; font-size: 0.8em; font-weight: bold; margin-bottom: 8px; padding: 4px; border-radius: 4px;">⚠️ Split District (TX-15 & TX-28)</div>`;
            }
        }"""

map_js = map_js.replace("<h3 style=\"margin-top:0; color:#0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 5px;\">Precinct ${cleanPct || 'Unknown'}</h3>`;", popup_replace)

with open('hidalgo-election-map/map_chairs.js', 'w', encoding='utf-8') as f:
    f.write(map_js)


# 3. Update precinct_chairs.html
with open('precinct_chairs.html', 'r', encoding='utf-8') as f:
    html = f.read()

row_replace = """              <td>
                  <span class="pct-badge">${person.precinct}</span>
                  ${(window.cd15List.includes(parseInt(person.precinct)) && window.cd28List.includes(parseInt(person.precinct))) ? '<br><span style="background:#ea580c; color:white; font-size:0.7rem; font-weight: bold; padding: 2px 6px; border-radius: 4px; display:inline-block; margin-top: 5px;">Split District</span>' : ''}
              </td>"""

html = html.replace('<td><span class="pct-badge">${person.precinct}</span></td>', row_replace)

with open('precinct_chairs.html', 'w', encoding='utf-8') as f:
    f.write(html)
