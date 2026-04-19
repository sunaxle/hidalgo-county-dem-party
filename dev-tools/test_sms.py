import smtplib
from email.message import EmailMessage
import getpass

def test_sms():
    print("🚀 SMS TERMINAL BLASTER - VERIZON GATEWAY")
    print("------------------------------------------")
    
    sender_email = "info@hidalgocountydems.org"
    password = getpass.getpass(f"🔐 Please enter password for {sender_email}: ")
    
    # Target via Verizon's free Email-to-SMS Gateway
    target_sms = "9566387581@vtext.com"
    
    msg = EmailMessage()
    # Leaving the subject blank so it looks more like a natural text message
    msg['From'] = sender_email
    msg['To'] = target_sms
    msg.set_content("Desi, \n\nThis is a text from a terminal.")
    
    print(f"\n⏳ Connecting to Bluehost SMTP to fire payload to {target_sms}...")
    try:
        server = smtplib.SMTP_SSL('mail.hidalgocountydems.org', 465)
        server.login(sender_email, password)
        
        server.send_message(msg)
        server.quit()
        print(f"\n🎉 SUCCESS! SMS Payload fired successfully.")
        print("Check your phone right now. It should arrive from an email address instead of a standard 10-digit number.")
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ AUTHENTICATION FAILED: Incorrect password.")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    test_sms()
