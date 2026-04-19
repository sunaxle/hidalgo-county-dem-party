import smtplib
import csv
import ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import os

# --- Configuration ---
SMTP_SERVER = "smtp.bluehost.com"  # default Bluehost SMTP. Could also be mail.hidalgocountydems.org
SMTP_PORT = 465 # SSL port
SENDER_EMAIL = "info@hidalgocountydems.org"
# ---------------------

def send_email_blast(csv_file_path, subject, html_content_file):
    # Ask for password so it's not saved in plain text
    password = getpass.getpass(prompt='Enter Bluehost Email Password: ')
    
    # Read the HTML template
    with open(html_content_file, 'r', encoding='utf-8') as f:
        html_template = f.read()

    # Read the contact list
    contacts = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contacts.append(row)
            
    print(f"Loaded {len(contacts)} contacts. Preparing to send...")

    # Create secure SSL context
    context = ssl.create_default_context()

    sent_count = 0
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, password)
        
        for person in contacts:
            email = person.get("Email")
            first_name = person.get("FirstName", "Supporter")
            
            if not email:
                continue

            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = SENDER_EMAIL
            message["To"] = email

            # Personalize the HTML content (if we put a {FirstName} tag in the HTML)
            personalized_html = html_template.replace("{FirstName}", first_name)
            
            # Attach HTML
            message.attach(MIMEText(personalized_html, "html"))

            try:
                server.sendmail(SENDER_EMAIL, email, message.as_string())
                print(f"✅ Sent to {first_name} ({email})")
                sent_count += 1
                time.sleep(1) # Throttle to avoid Bluehost spam limits
            except Exception as e:
                print(f"❌ Failed to send to {email}. Error: {e}")

    print(f"\n🎉 Blast complete! Successfully sent {sent_count} emails.")

if __name__ == "__main__":
    print("Welcome to the Ad-Hoc Email Blaster")
    # Usage example (we will run this from the terminal later):
    # send_email_blast('data/curated_list.csv', 'Urgent Democratic Update', 'communications/email_template.html')
