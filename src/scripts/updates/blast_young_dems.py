import csv
import getpass
import smtplib
import sys
import time
from email.message import EmailMessage

TEMPLATE_FILE = "young_dems_meeting_template.html"
TARGET_CSV = "data/young_dems.csv"


def load_template():
    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        return f.read()


def send_email(
    recipient_name,
    recipient_email,
    sender_email,
    server,
    template_html,
    is_dry_run=True,
):
    subject = "Action Required: Young Dems Convention Fundraiser Meeting"

    # Replace placeholders in the HTML
    html_content = template_html.replace("{{FIRST_NAME}}", recipient_name)

    if is_dry_run:
        print(f"[DRY RUN] Would send to: {recipient_name} ({recipient_email})")
        return

    msg = EmailMessage()
    msg.add_alternative(html_content, subtype="html")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        if server:
            server.send_message(msg)
            print(f"✅ Successfully sent to {recipient_name} ({recipient_email})")
            time.sleep(1)  # Prevent rate-limiting
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

    print(f"Reading contacts from {TARGET_CSV}...")

    server = None
    if not is_dry_run:
        print("Connecting to mail.hidalgocountydems.org via 465 (SSL)...")
        smtp_server = "mail.hidalgocountydems.org"
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20)
        server.login(my_email, my_password)

    emails_sent_in_batch = 0

    try:
        with open(TARGET_CSV, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row.get("First Name", "").strip()
                email_field = row.get("Email", "").strip()

                if not email_field:
                    continue

                # Some rows might have multiple emails separated by '/' or ' '
                # e.g., "alexoviedo64@yahoo.com / 7oviedoa7@gmail.com"
                if "/" in email_field:
                    emails = [e.strip() for e in email_field.split("/")]
                elif "," in email_field:
                    emails = [e.strip() for e in email_field.split(",")]
                else:
                    emails = [email_field]

                for email in emails:
                    if not email or "@" not in email:
                        continue

                    if is_dry_run:
                        send_email(
                            first_name, email, my_email, None, template, is_dry_run
                        )
                    else:
                        success = send_email(
                            first_name, email, my_email, server, template, is_dry_run
                        )
                        if success:
                            emails_sent_in_batch += 1

                            # Auto-cooldown to prevent Bluehost 421 Rate Limit
                            if emails_sent_in_batch >= 40:
                                print(
                                    "\n⏸️  Reached 40 emails. Resting for 5 minutes to prevent mail server blocking..."
                                )
                                server.quit()
                                for i in range(300, 0, -1):
                                    sys.stdout.write(
                                        f"\r⏳ Resting... {i} seconds remaining   "
                                    )
                                    sys.stdout.flush()
                                    time.sleep(1)
                                print("\n🔄 Reconnecting to mail server...")
                                server = smtplib.SMTP_SSL(
                                    smtp_server, smtp_port, timeout=20
                                )
                                server.login(my_email, my_password)
                                emails_sent_in_batch = 0
                        else:
                            print(
                                "Terminating blast to prevent spam lock. Wait a few moments before retrying."
                            )
                            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ Could not find {TARGET_CSV}")
        sys.exit(1)
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass

    if is_dry_run:
        print(
            "\nNote: This was a dry run. To actually send the blast, edit the script with your real password if needed, and run:"
        )
        print("python3 blast_young_dems.py send")
