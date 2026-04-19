import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import getpass
import os

def send_desi_analysis():
    print("🚀 HIDALGO COUNTY DEMS - DESI PRECINCT 192 SENDER")
    print("--------------------------------------------------")
    
    # 1. Credentials
    desi_email = input("Enter Desi's email address: ").strip()
    if not desi_email:
        print("Error: Desi's email cannot be empty.")
        return

    sender_email = "info@hidalgocountydems.org"
    print(f"\n🔐 Please enter the password for {sender_email}")
    password = getpass.getpass()

    # 2. Load the HTML Template
    template_path = "precinct_192_analysis.html"
    try:
        with open(template_path, "r", encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print(f"Error: {template_path} not found. Make sure you are in dev-tools.")
        return

    # 3. Construct the Multipart Email
    msg = EmailMessage()
    msg['Subject'] = "CONFIDENTIAL: Precinct 192 Strategic Deep Dive & Target Data"
    msg['From'] = formataddr(("Hidalgo County Democratic Party", sender_email))
    msg['To'] = desi_email
    
    # Attach HTML payload
    msg.set_content("Please enable HTML to view this report.")
    msg.add_alternative(html_template, subtype='html')

    # 4. Attachments
    print("\n📦 Packing attachments...")
    
    # File 1: The Raw Data File (Full DB)
    full_db_path = "../data/emaildatasettest/p192demodataemail20260412-6063013339.xls"
    try:
        with open(full_db_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='vnd.ms-excel', filename='Full_Precinct_192_Database.xls')
            print("   -> Attached: Full Database")
    except Exception as e:
        print(f"   [!] Failed to attach full DB: {e}")

    # File 2: Targeted Non-Voters CSV
    non_voters_path = "../data/emaildatasettest/p192_non_voters.csv"
    try:
        with open(non_voters_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='text', subtype='csv', filename='Targeted_Non_Voters.csv')
            print("   -> Attached: Targeted Non-Voters")
    except Exception as e:
        print(f"   [!] Failed to attach non-voters list: {e}")

    # 5. Connect and Send via Bluehost
    print("\n⏳ Connecting to Bluehost SMTP server on port 465...")
    try:
        server = smtplib.SMTP_SSL('mail.hidalgocountydems.org', 465)
        server.login(sender_email, password)
        
        print("✅ Login successful. Transmitting highly-classified payload...")
        server.send_message(msg)
        server.quit()
        
        print(f"\n🎉 SUCCESS! Strategic packet delivered to {desi_email}.")
        print("The ground game has officially commenced.")
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ AUTHENTICATION FAILED: The password you entered was incorrect.")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    send_desi_analysis()
