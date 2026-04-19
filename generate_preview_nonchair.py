import sys

TEMPLATE_FILE = "lupe_marcha_email_template.html"

YOUTUBE_TRANSCRIPT = "The recent ICE raids targeting the construction industry in the Valley are unacceptable. We are organizing a coalition of local leaders to demand that ICE get out of Hidalgo County."
PODCAST_TRANSCRIPT = "Rebuilding the 'South Texas Blue Wall' starts right here. We need to offer clear solutions and show people we are fighting for their pocketbook economic issues, not just talking."
CHAIRMAN_WORDS = """As I look to my final term as your County Chair, my priority is cementing the progress we've made. We must stand shoulder-to-shoulder with our community and protect our neighbors. That's why I'm asking you to join me and the Hidalgo County Democratic Party at the LUPE 'Marcha del Pueblo' in Edinburg on Saturday, May 2nd.<br><br>The Marcha del Pueblo is a new tradition bringing together organizations from across the Rio Grande Valley to uplift issues impacting our communities, such as labor rights, immigration, healthcare, education, and more. This family-friendly, peaceful march honors our shared history and affirms our collective power and vision for justice and belonging.<br><br>As a Precinct Chair, we hope you will walk alongside us and help make this gathering possible. Please reply to this email to let me know:<ul><li>If you will attend</li><li>How many people you anticipate bringing from your precinct (aim for at least five!)</li><li>If you’d like promotional materials to share with your neighbors</li></ul><br>Adelante,<br><strong>Richard Gonzales</strong><br><em>Hidalgo County Democratic Party Chair</em>"""
RSVP_LINK = "https://lupenet.org/marcha-del-pueblo-3/"

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

# NON-CHAIR LOGIC EXACTLY LIKE PRODUCTION SCRIPT
html_content = html_content.replace("Precinct {{PRECINCT_NUMBER}}", "Your Area")
html_content = html_content.replace("the designated Precinct Chair for Precinct {{PRECINCT_NUMBER}}", "a Democratic Leader in our community")

html_content = html_content.replace("<p>Your precinct currently has</p>", "<p>Our powerful community is filled with</p>")
html_content = html_content.replace("{{VAN_VOTER_COUNT}} Registered Democrats", "Thousands of Active Democrats")
html_content = html_content.replace("If you bring just 1% of them to the marcha, we will overwhelmingly exceed our goals.", "If you activate just a few people in your network for the marcha, we will overwhelmingly exceed our goals.")


# General Variables
html_content = html_content.replace("{{FIRST_NAME}}", "Abad")
html_content = html_content.replace("{{YOUTUBE_TRANSCRIPT}}", YOUTUBE_TRANSCRIPT)
html_content = html_content.replace("{{PODCAST_TRANSCRIPT}}", PODCAST_TRANSCRIPT)
html_content = html_content.replace("{{CHAIRMAN_WORDS}}", CHAIRMAN_WORDS)
html_content = html_content.replace("{{FB_LINK}}", RSVP_LINK)

with open("lupe_marcha_preview_nonchair.html", "w", encoding="utf-8") as f:
    f.write(html_content)

