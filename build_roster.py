import os

try:
    with open('precinct_profiles.html', 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace("Precinct Profiles | Hidalgo Dems", "Volunteer Roster | Hidalgo Dems")
    text = text.replace('<h1 style="color: var(--accent); font-size: 3rem; margin-bottom: 1rem;">Precinct Profiles</h1>', '<h1 style="color: var(--accent); font-size: 3rem; margin-bottom: 1rem;">Volunteer Roster</h1>')
    text = text.replace("Meet the grassroots leaders of your neighborhood. Select your precinct below to view the dedicated Chair's profile, contact info, and localized announcements.", "Access our live volunteer database. Search for your own generated profile by typing your first and last name below to connect with your designated Precinct Chair.")
    text = text.replace("Find Your Precinct", "Find Your Profile")

    search_block = """            <!-- Name Search -->
            <div>
                <label style="display:block; text-align:left; color:#cbd5e1; margin-bottom:0.5rem; font-weight:600; font-size:0.9rem;">Search by Volunteer Name</label>
                <div style="display: flex; gap: 1rem;">
                  <input type="text" id="name-search-input" placeholder="e.g. Jane Doe" style="flex: 1; padding: 1rem 1.5rem; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #fff; font-size: 1.1rem; outline: none;">
                  <button id="name-search-btn" class="btn btn-primary" style="border: none; cursor: pointer; padding: 1rem 2rem; font-size: 1.1rem; font-weight: bold; background: transparent; border: 2px solid var(--accent); color: var(--accent);">Search</button>
                </div>
                <div id="name-search-error" style="color: #ef4444; margin-top: 0.5rem; display: none; font-weight: 600; text-align:left;"></div>
            </div>"""

    target_insertion = 'id="precinct-search-error" style="color: #ef4444; margin-top: 0.5rem; display: none; font-weight: 600; text-align:left;"></div>\n            </div>'
    text = text.replace(target_insertion, target_insertion + '\n\n' + search_block)

    text = text.replace("Recent Leadership Elected", "Grassroots Volunteer Activity")
    text = text.replace('js/chair_data.js?v=2', 'js/volunteer_sync.js?v=3')
    text = text.replace('js/precinct_hub.js?v=4', 'js/volunteer_hub.js?v=1')

    with open('volunteer_roster.html', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("Successfully built Volunteer Roster HTML!")
except Exception as e:
    print(f"Error compiling HTML: {e}")
