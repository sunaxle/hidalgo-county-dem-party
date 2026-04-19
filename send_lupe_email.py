import smtplib
from email.message import EmailMessage
import sys

def draft_email_content(recipient_name):
    """Generates the personalized email content."""
    return f"""Dear {recipient_name},

I hope this email finds you well. 

As we look to strengthen our community organizing and mobilization efforts, we are identifying opportunities to build stronger bridges between the Hidalgo County Democratic Party and allied organizations.

Could you please let me know if you are currently a member of LUPE or LUPE Votes? 

Understanding our shared memberships among Precinct Chairs will help us better coordinate our advocacy, leverage the strengths of both organizations, and maximize our overall impact across the county.

Thank you for your continued dedication to our community.

Best regards,

[Your Name]
[Your Title/Role]
Hidalgo County Democratic Party"""

def send_email(recipient_name, recipient_email, sender_email, sender_password):
    """Sends the email using SMTP."""
    subject = "Fostering Collaboration: Hidalgo County Dems & LUPE"
    body = draft_email_content(recipient_name)

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Bluehost SMTP configuration
    smtp_server = "mail.hidalgocountydemocraticparty.org" 
    smtp_port = 465 # Default SSL port for Bluehost
    
    try:
        print(f"Connecting to {smtp_server}...")
        # Using SMTP_SSL for Bluehost's standard secure connection
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email successfully sent to {recipient_name} ({recipient_email})!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Personalizing for Desi
    target_name = "Desi"
    target_email = "desi@example.com" # TODO: Update with Desi's real email address
    
    # Your Bluehost credentials
    my_email = "info@hidalgocountydemocraticparty.org"
    my_password = "your_email_password" # TODO: Update with the password for this email account
    # ---------------------
    
    print("Drafting email...")
    print("-" * 50)
    print(f"To: {target_name} <{target_email}>")
    print(f"Subject: Fostering Collaboration: Hidalgo County Dems & LUPE\n")
    print(draft_email_content(target_name))
    print("-" * 50)
    
    # If the user wants to test sending, they can run the script with a 'send' flag
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        if target_email == "desi@example.com" or my_password == "your_email_password":
            print("\n⚠️  Please update Desi's email address and your Bluehost password in the script before sending.")
            sys.exit(1)
        send_email(target_name, target_email, my_email, my_password)
    else:
        print("\nNote: This was just a dry-run print. To actually send the email, edit the script with your credentials, then run:")
        print("python3 send_lupe_email.py send")
