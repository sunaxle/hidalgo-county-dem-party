import smtplib
from email.message import EmailMessage
import sys
import getpass

TEMPLATE_FILE = "lupe_marcha_email_template.html"

# Test Data
YOUTUBE_TRANSCRIPT = "The recent ICE raids targeting the construction industry in the Valley are unacceptable. We are organizing a coalition of local leaders to demand that ICE get out of Hidalgo County."
PODCAST_TRANSCRIPT = "Rebuilding the 'South Texas Blue Wall' starts right here. We need to offer clear solutions and show people we are fighting for their pocketbook economic issues, not just talking."
CHAIRMAN_WORDS = """As I look to my final term as your County Chair, my priority is cementing the progress we've made. We must stand shoulder-to-shoulder with our community and protect our neighbors. That's why I'm asking you to join me and the Hidalgo County Democratic Party at the LUPE 'Marcha del Pueblo' in Edinburg on Saturday, May 2nd.<br><br>The Marcha del Pueblo is a new tradition bringing together organizations from across the Rio Grande Valley to uplift issues impacting our communities, such as labor rights, immigration, healthcare, education, and more. This family-friendly, peaceful march honors our shared history and affirms our collective power and vision for justice and belonging.<br><br>As a Precinct Chair, we hope you will walk alongside us and help make this gathering possible. Please reply to this email to let me know:<ul><li>If you will attend</li><li>How many people you anticipate bringing from your precinct (aim for at least five!)</li><li>If you’d like promotional materials to share with your neighbors</li></ul><br>Adelante,<br><strong>Richard Gonzales</strong><br><em>Hidalgo County Democratic Party Chair</em>"""
RSVP_LINK = "https://lupenet.org/marcha-del-pueblo-3/"

def send_test_email(target_email, sender_email, sender_password):
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ Could not find {TEMPLATE_FILE}")
        return

    # Replace with test data
    html_content = html_content.replace("{{FIRST_NAME}}", "Test User")
    html_content = html_content.replace("{{PRECINCT_NUMBER}}", "99")
    html_content = html_content.replace("{{YOUTUBE_TRANSCRIPT}}", YOUTUBE_TRANSCRIPT)
    html_content = html_content.replace("{{PODCAST_TRANSCRIPT}}", PODCAST_TRANSCRIPT)
    html_content = html_content.replace("{{CHAIRMAN_WORDS}}", CHAIRMAN_WORDS)
    html_content = html_content.replace("{{VAN_VOTER_COUNT}}", "1,250")
    html_content = html_content.replace("{{FB_LINK}}", RSVP_LINK)

    msg = EmailMessage()
    msg.add_alternative(html_content, subtype='html')
    msg['Subject'] = "[TEST] Action Required: Join the LUPE May 2nd Marcha"
    msg['From'] = sender_email
    msg['To'] = target_email

    smtp_server = "mail.hidalgocountydems.org" 
    smtp_port = 465
    
    print(f"Sending test email to {target_email} via {smtp_server}...")
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Successfully sent test email to {target_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    print("-" * 50)
    print("Test Email Blast Sender")
    print("-" * 50)
    
    sender = "info@hidalgocountydems.org" # Current correct email domain
    target = input("Enter the email address you want to send the test TO: ")
    password = getpass.getpass(f"Enter the password for {sender}: ")
    
    if target and password:
        send_test_email(target, sender, password)
    else:
        print("Required fields missing. Exiting.")
