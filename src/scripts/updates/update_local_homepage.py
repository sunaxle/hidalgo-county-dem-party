import os
import re

home = os.path.expanduser("~")
search_paths = [
    os.path.join(
        home,
        "Documents",
        "Antigravity Designs",
        "hidalgo-county-dem-party",
        "mobile_prototype",
        "index.html",
    ),
    os.path.join(
        home,
        "Documents",
        "Antigravity Designs",
        "hidalgo-county-dem-party",
        "index.html",
    ),
    os.path.join(home, "Documents", "hidalgo-county-dem-party", "index.html"),
]

banner_html = """    <!-- Live Voter Registration Countdown Banner -->
    <div id="voter-countdown-banner" style="background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%); color: white; text-align: center; padding: 12px 20px; font-weight: bold; font-family: \'Montserrat\', sans-serif; font-size: 14px; position: relative; z-index: 1001; box-shadow: 0 2px 5px rgba(0,0,0,0.15); display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <div style="font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px;">⚡ Help Us Register 20,000 More Voters! ⚡</div>
        <div>Texas Voter Registration Deadline: <span id="registration-deadline-date" style="color: #ffd700;">October 5, 2026</span> (<span id="days-remaining-count" style="color: #ffd700;">--</span> Days Remaining)</div>
        <a href="volunteer.html" style="color: white; text-decoration: underline; margin-top: 4px; font-size: 12px;">Become a Block Captain to Help Us Reach Our Goal &rarr;</a>
    </div>
    <script>
    (function() {
        const deadline = new Date(\'2026-10-05T23:59:59-05:00\');
        const now = new Date();
        const diffTime = deadline - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        const countEl = document.getElementById(\'days-remaining-count\');
        if (countEl) {
            countEl.textContent = diffDays > 0 ? diffDays : 0;
        }
    })();
    </script>
"""
updated_any = False
for p in search_paths:
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            content = f.read()

        # Remove any existing banner to avoid duplication
        content = re.sub(
            r"<!-- Live Voter Registration Countdown Banner -->.*?\(function\(\).*?\}\)\(\);.*?\s*</script>\s*",
            "",
            content,
            flags=re.DOTALL,
        )
        content = content.replace(
            'id="voter-countdown-banner"', 'id="old-banner-to-remove"'
        )  # safeguard

        # Comment out or remove old passed dates/announcements like June 3-4
        # For safety, let's look for known past campaign meeting blocks and comment them out
        content = re.sub(
            r'(<div class="event-card".*?June 3.*?</div>)',
            r"<!-- \1 -->",
            content,
            flags=re.DOTALL,
        )
        content = re.sub(
            r'(<div class="event-card".*?June 4.*?</div>)',
            r"<!-- \1 -->",
            content,
            flags=re.DOTALL,
        )

        # Inject new countdown banner right after <body>
        if "<body>" in content:
            content = content.replace("<body>", "<body>\n" + banner_html)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully updated index.html with live countdown banner at: {p}")
            updated_any = True

if not updated_any:
    print("Warning: No index.html files were found to update.")
