import smtplib
from email.message import EmailMessage
import sys
import getpass

def run_diagnostic():
    sender_email = "info@hidalgocountydems.org"
    print("\n--- INITIATING PURE PLAIN-TEXT DIAGNOSTIC ---")
    sender_password = getpass.getpass(f"🔑 Enter SMTP password for {sender_email}: ")

    # No HTML. No links. Just plain text. 
    msg = EmailMessage()
    msg.set_content("If you receive this, it proves that Google was blocking the HTML hyperlinks, not your domain.")
    msg['Subject'] = "Diagnostic: Plain Text Test"
    msg['From'] = sender_email
    msg['To'] = "romerodeab@gmail.com"

    try:
        print("\n[Connecting...]")
        server = smtplib.SMTP_SSL("mail.hidalgocountydems.org", 465, timeout=20)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("\n✅ Sent plain text message.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    run_diagnostic()
