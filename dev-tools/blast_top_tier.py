import csv
import smtplib
from email.message import EmailMessage
import sys
import time
import getpass

TEMPLATE_FILE = "dev-tools/top_tier_blast_preview.html"
CSV_FILE = "data/top_tier_democrats.csv"
CC_EMAIL = "romerodeab@gmail.com"

def load_template():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def send_email(first_name, recipient_email, sender_email, server, template_html, is_dry_run=True):
    subject = "🚀 Major Launch: Massive Updates to the Hidalgo Dems Digital Infrastructure"
    
    html_content = template_html.replace("{FIRST_NAME}", first_name)

    if is_dry_run:
        print(f"[DRY RUN] Would send to: {recipient_email} (CC: {CC_EMAIL})")
        return

    msg = EmailMessage()
    msg.add_alternative(html_content, subtype='html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Cc'] = CC_EMAIL

    try:
        if server:
            server.send_message(msg)
            print(f"✅ Successfully sent to {recipient_email}")
            time.sleep(5) # Slowed down to 5 seconds to bypass host outgoing spam locks
            return True
    except Exception as e:
        print(f"❌ Failed to send to {recipient_email}: {e}")
        return False

if __name__ == "__main__":
    my_email = "info@hidalgocountydems.org"
    my_password = None
    
    is_dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        is_dry_run = False
        my_password = getpass.getpass(f"🔑 Enter SMTP password for {my_email}: ")

    print("Loading email template...")
    try:
        template = load_template()
    except FileNotFoundError:
        print(f"❌ Could not find {TEMPLATE_FILE}")
        sys.exit(1)

    print(f"Reading VIP list from {CSV_FILE}...")
    
    server = None
    if not is_dry_run:
        print("Connecting to mail.hidalgocountydems.org via 465 (SSL)...")
        smtp_server = "mail.hidalgocountydems.org" 
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20)
        server.login(my_email, my_password)

    total_sent = 0

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row.get('First Name', 'Leader').strip()
                if not first_name:
                    first_name = "Leader"
                email = row.get('Email', '').strip()
                
                if not email or "@" not in email:
                    continue
                    
                if is_dry_run:
                    send_email(first_name, email, my_email, None, template, is_dry_run)
                else:
                    success = send_email(first_name, email, my_email, server, template, is_dry_run)
                    if success:
                        total_sent += 1
                        
                        # Added extremely safe rate limit cooldowns like the previous script
                        if total_sent >= 40:
                            print("\n⏸️  Resting for 5 minutes to prevent mail server blocking...")
                            server.quit()
                            for i in range(300, 0, -1):
                                sys.stdout.write(f"\r⏳ Resting... {i} seconds remaining   ")
                                sys.stdout.flush()
                                time.sleep(1)
                            print("\n🔄 Reconnecting to mail server...")
                            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20)
                            server.login(my_email, my_password)
                            total_sent = 0

    except FileNotFoundError:
        print(f"❌ Could not find {CSV_FILE}")
        sys.exit(1)
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass
        
    if is_dry_run:
        print("\nNote: This was a dry run. To actually send the blast and CC yourself, run:")
        print("python3 dev-tools/blast_top_tier.py send")
