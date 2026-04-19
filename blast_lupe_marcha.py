import csv
import smtplib
from email.message import EmailMessage
import sys
import time
import json
import getpass

# To use this script, make sure `lupe_marcha_email_template.html` is in the same directory.
TEMPLATE_FILE = "lupe_marcha_email_template.html"
CHAIRS_CSV = "dev-tools/curated_precinct_chairs.csv"

# ACTUAL TRANSCRIPT AND MESSAGE CONTENT
YOUTUBE_TRANSCRIPT = "The recent ICE raids targeting the construction industry in the Valley are unacceptable. We are organizing a coalition of local leaders to demand that ICE get out of Hidalgo County."
PODCAST_TRANSCRIPT = "Rebuilding the 'South Texas Blue Wall' starts right here. We need to offer clear solutions and show people we are fighting for their pocketbook economic issues, not just talking."
CHAIRMAN_WORDS = """As I look to my final term as your County Chair, my priority is cementing the progress we've made. We must stand shoulder-to-shoulder with our community and protect our neighbors. That's why I'm asking you to join me and the Hidalgo County Democratic Party at the LUPE 'Marcha del Pueblo' in Edinburg on Saturday, May 2nd.<br><br>The Marcha del Pueblo is a new tradition bringing together organizations from across the Rio Grande Valley to uplift issues impacting our communities, such as labor rights, immigration, healthcare, education, and more. This family-friendly, peaceful march honors our shared history and affirms our collective power and vision for justice and belonging.<br><br>As a Precinct Chair, we hope you will walk alongside us and help make this gathering possible. Please reply to this email to let me know:<ul><li>If you will attend</li><li>How many people you anticipate bringing from your precinct (aim for at least five!)</li><li>If you’d like promotional materials to share with your neighbors</li></ul><br>Adelante,<br><strong>Richard Gonzales</strong><br><em>Hidalgo County Democratic Party Chair</em>"""
RSVP_LINK = "https://lupenet.org/marcha-del-pueblo-3/"

def load_template():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

# Load VAN Data once into memory
try:
    with open('dev-tools/van_turfs.json', 'r') as f:
        VAN_DATA = json.load(f)
except FileNotFoundError:
    VAN_DATA = {}

def get_van_voter_count(precinct_num):
    # Dynamically pull the exact voter count for their precinct, default to an unknown safe number if missing
    return VAN_DATA.get(str(precinct_num), "0")

def send_email(recipient_name, recipient_email, precinct_num, sender_email, server, template_html, is_dry_run=True):
    van_voter_count = get_van_voter_count(precinct_num)

    if precinct_num == "Unknown":
        subject = "Action Required: Join the LUPE May 2nd Marcha"
        html_content = template_html.replace("Precinct {{PRECINCT_NUMBER}}", "Your Area")
        html_content = html_content.replace("the designated Precinct Chair for Precinct {{PRECINCT_NUMBER}}", "a Democratic Leader in our community")
        # Side-step the specific voter count logic
        html_content = html_content.replace("<p>Your precinct currently has</p>", "<p>Our powerful community is filled with</p>")
        html_content = html_content.replace("{{VAN_VOTER_COUNT}} Registered Democrats", "Thousands of Active Democrats")
        html_content = html_content.replace("If you bring just 1% of them to the marcha, we will overwhelmingly exceed our goals.", "If you activate just a few people in your network for the marcha, we will overwhelmingly exceed our goals.")
    else:
        subject = f"Action Required: Join the LUPE May 2nd Marcha (Precinct {precinct_num})"
        html_content = template_html.replace("{{PRECINCT_NUMBER}}", precinct_num)

    # Replace placeholders in the HTML
    html_content = html_content.replace("{{FIRST_NAME}}", recipient_name)
    html_content = html_content.replace("{{YOUTUBE_TRANSCRIPT}}", YOUTUBE_TRANSCRIPT)
    html_content = html_content.replace("{{PODCAST_TRANSCRIPT}}", PODCAST_TRANSCRIPT)
    html_content = html_content.replace("{{CHAIRMAN_WORDS}}", CHAIRMAN_WORDS)
    html_content = html_content.replace("{{VAN_VOTER_COUNT}}", van_voter_count)
    html_content = html_content.replace("{{FB_LINK}}", RSVP_LINK)

    if is_dry_run:
        print(f"[DRY RUN] Would send to: {recipient_name} ({recipient_email}) for Precinct {precinct_num}")
        # Optionally print the first 200 chars of HTML
        return

    msg = EmailMessage()
    msg.add_alternative(html_content, subtype='html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        if server:
            server.send_message(msg)
            print(f"✅ Successfully sent to {recipient_name} ({recipient_email})")
            time.sleep(1) # Prevent rate-limiting
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

    print(f"Reading log from dev-tools/log_success.txt...")
    sent_emails = set()
    try:
        with open("dev-tools/log_success.txt", "r") as f:
            for line in f:
                sent_emails.add(line.strip().lower())
    except FileNotFoundError:
        pass

    print(f"Reading chairs from {CHAIRS_CSV}...")
    
    server = None
    if not is_dry_run:
        print("Connecting to mail.hidalgocountydems.org via 465 (SSL)...")
        smtp_server = "mail.hidalgocountydems.org" 
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20)
        server.login(my_email, my_password)

    emails_sent_in_batch = 0

    try:
        with open(CHAIRS_CSV, "r", encoding="utf-8") as f, open("dev-tools/log_success.txt", "a") as log_f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row['FirstName']
                email = row['Email']
                
                if not email or "@" not in email:
                    continue
                    
                if email.lower() in sent_emails:
                    print(f"⏭️  Skipping {email} (already sent)")
                    continue
                
                tags = row['Tags']
                precinct_part = [t.strip() for t in tags.split(",") if "Precinct_" in t]
                precinct_num = "Unknown"
                if precinct_part:
                    precinct_num = precinct_part[0].replace("Precinct_", "")

                if is_dry_run:
                    send_email(first_name, email, precinct_num, my_email, None, template, is_dry_run)
                else:
                    success = send_email(first_name, email, precinct_num, my_email, server, template, is_dry_run)
                    if success:
                        log_f.write(email.lower() + "\n")
                        log_f.flush()
                        emails_sent_in_batch += 1
                        
                        # Auto-cooldown to prevent Bluehost 421 Rate Limit
                        if emails_sent_in_batch >= 40:
                            print("\n⏸️  Reached 40 emails. Resting for 5 minutes to prevent mail server blocking...")
                            server.quit()
                            for i in range(300, 0, -1):
                                sys.stdout.write(f"\r⏳ Resting... {i} seconds remaining   ")
                                sys.stdout.flush()
                                time.sleep(1)
                            print("\n🔄 Reconnecting to mail server...")
                            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20)
                            server.login(my_email, my_password)
                            emails_sent_in_batch = 0
                    else:
                        print("Terminating blast to prevent spam lock. Wait a few moments before retrying.")
                        break

    except FileNotFoundError:
        print(f"❌ Could not find {CHAIRS_CSV}")
        sys.exit(1)
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass
        
    if is_dry_run:
        print("\nNote: This was a dry run. To actually send the blast, edit the script with your real password, transcripts, and run:")
        print("python3 blast_lupe_marcha.py send")
