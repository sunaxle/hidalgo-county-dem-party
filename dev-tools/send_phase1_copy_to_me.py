import smtplib
from email.message import EmailMessage
import sys
import getpass

TEMPLATE_FILE = "dev-tools/phase1_blast_preview.html"
MY_EMAIL = "romerodeab@gmail.com"

def load_template():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    sender_email = "info@hidalgocountydems.org"
    sender_password = getpass.getpass(f"🔑 Enter SMTP password for {sender_email}: ")

    try:
        html_content = load_template()
    except FileNotFoundError:
        print(f"❌ Could not find {TEMPLATE_FILE}")
        sys.exit(1)

    msg = EmailMessage()
    msg.add_alternative(html_content, subtype='html')
    msg['Subject'] = "🚀 Welcome to the New Digital Home of the Hidalgo County Democratic Party"
    msg['From'] = sender_email
    msg['To'] = MY_EMAIL

    print("Connecting to mail.hidalgocountydems.org via 465 (SSL)...")
    try:
        server = smtplib.SMTP_SSL("mail.hidalgocountydems.org", 465, timeout=20)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print(f"✅ Successfully fired a clean copy of the Phase 1 email directly to {MY_EMAIL}")
        server.quit()
    except Exception as e:
        print(f"❌ Failed to send directly: {e}")
