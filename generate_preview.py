import os

TEMPLATE_FILE = "lupe_marcha_email_template.html"

# ACTUAL TRANSCRIPT AND MESSAGE CONTENT
YOUTUBE_TRANSCRIPT = "The recent ICE raids targeting the construction industry in the Valley are unacceptable. We are organizing a coalition of local leaders to demand that ICE get out of Hidalgo County."
PODCAST_TRANSCRIPT = "Rebuilding the 'South Texas Blue Wall' starts right here. We need to offer clear solutions and show people we are fighting for their pocketbook economic issues, not just talking."
CHAIRMAN_WORDS = """As I look to my final term as your County Chair, my priority is cementing the progress we've made. We must stand shoulder-to-shoulder with our community and protect our neighbors. That's why I'm asking you to join me and the Hidalgo County Democratic Party at the LUPE 'Marcha del Pueblo' in Edinburg on Saturday, May 2nd.<br><br>The Marcha del Pueblo is a new tradition bringing together organizations from across the Rio Grande Valley to uplift issues impacting our communities, such as labor rights, immigration, healthcare, education, and more. This family-friendly, peaceful march honors our shared history and affirms our collective power and vision for justice and belonging.<br><br>As a Precinct Chair, we hope you will walk alongside us and help make this gathering possible. Please reply to this email to let me know:<ul><li>If you will attend</li><li>How many people you anticipate bringing from your precinct (aim for at least five!)</li><li>If you’d like promotional materials to share with your neighbors</li></ul><br>Adelante,<br><strong>Richard Gonzales</strong><br><em>Hidalgo County Democratic Party Chair</em>"""
RSVP_LINK = "https://lupenet.org/marcha-del-pueblo-3/"

van_voter_count = "1,986"
recipient_name = "Cassandra"
precinct_num = "2"

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

html_content = html_content.replace("{{FIRST_NAME}}", recipient_name)
html_content = html_content.replace("{{PRECINCT_NUMBER}}", precinct_num)
html_content = html_content.replace("{{YOUTUBE_TRANSCRIPT}}", YOUTUBE_TRANSCRIPT)
html_content = html_content.replace("{{PODCAST_TRANSCRIPT}}", PODCAST_TRANSCRIPT)
html_content = html_content.replace("{{CHAIRMAN_WORDS}}", CHAIRMAN_WORDS)
html_content = html_content.replace("{{VAN_VOTER_COUNT}}", van_voter_count)
html_content = html_content.replace("{{FB_LINK}}", RSVP_LINK)

with open("lupe_marcha_preview.html", "w", encoding="utf-8") as f:
    f.write(html_content)
