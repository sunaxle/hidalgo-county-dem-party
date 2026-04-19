import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import getpass
import os

def send_test_blast():
    print("🚀 HIDALGO COUNTY DEMS - BLUEHOST TEST BLASTER")
    print("----------------------------------------------")
    
    # 1. Prompt for test credentials
    test_email = input("Enter your personal email address to receive the test: ").strip()
    if not test_email:
        print("Error: Email cannot be empty.")
        return

    first_name = input("Enter your first name (for the greeting): ").strip()
    if not first_name:
        first_name = "Supporter"

    sender_email = "info@hidalgocountydems.org"
    print(f"\n🔐 Please enter the password for {sender_email}")
    password = getpass.getpass()

    # 2. Load the HTML Template
    template_path = "momentum_template.html"
    try:
        with open(template_path, "r", encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print(f"Error: {template_path} not found. Are you running this from dev-tools/?")
        return

    # 3. Inject the dynamic variables into the HTML
    # We use replacing instead of .format() to avoid CSS bracket clashes
    personalized_html = html_template.replace("{first_name}", first_name)

    # 4. Connect and Send via Bluehost
    print("\n⏳ Connecting to Bluehost SMTP server on port 465...")
    try:
        # Bluehost uses simplewebmail / cpanel routing, standard SMTP_SSL on 465
        server = smtplib.SMTP_SSL('mail.hidalgocountydems.org', 465)
        server.login(sender_email, password)
        
        print("✅ Login successful. Transmitting payload...")
        
        # Support sending to multiple comma-separated test emails
        email_list = [e.strip() for e in test_email.split(',') if e.strip()]
        
        for email_addr in email_list:
            msg = EmailMessage()
            msg['Subject'] = "1,200 Strong: The New Hidalgo County Democratic Party"
            msg['From'] = formataddr(("Hidalgo County Democratic Party", sender_email))
            msg['To'] = email_addr
            msg.set_content("If you are seeing this, your email client does not support HTML. Please view in a modern client.")
            msg.add_alternative(personalized_html, subtype='html')
            
            server.send_message(msg)
            print(f"   -> Fired to {email_addr}")
        
        server.quit()
        print(f"\n🎉 SUCCESS! Test emails completely delivered.")
        print("Check your inbox (and your spam folder just in case). If it landed, the engine is fully operational!")
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ AUTHENTICATION FAILED: The password you entered was incorrect. Try again.")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    send_test_blast()
