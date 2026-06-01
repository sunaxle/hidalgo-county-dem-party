import smtplib
from email.message import EmailMessage
import sys
import getpass

def run_diagnostic():
    sender_email = "info@hidalgocountydems.org"
    print("\n--- INITIATING SMTP DIAGNOSTIC ---")
    sender_password = getpass.getpass(f"🔑 Enter SMTP password for {sender_email}: ")

    msg = EmailMessage()
    msg.set_content("This is a system diagnostic message to verify SMTP routing and Google inbound reception protocols.")
    msg['Subject'] = "System Diagnostic - SMTP Routing Test"
    msg['From'] = sender_email
    msg['To'] = "romerodeab@gmail.com"

    try:
        print("\n[Connecting to mail.hidalgocountydems.org...]")
        server = smtplib.SMTP_SSL("mail.hidalgocountydems.org", 465, timeout=20)
        
        # This will print the raw network exchange between the server and Google
        server.set_debuglevel(1) 
        
        server.login(sender_email, sender_password)
        print("\n[Firing payload...]")
        server.send_message(msg)
        server.quit()
        
        print("\n✅ VERIFICATION COMPLETE")
        print("If the massive text block above ended with a '250 OK Message accepted' code, it means the server successfully wired it exactly where it was supposed to go. If it still didn't arrive, Google is actively throttling it as spam.")
    except Exception as e:
        print(f"\n❌ ROUTING FAILURE. Error: {e}")

if __name__ == "__main__":
    run_diagnostic()
