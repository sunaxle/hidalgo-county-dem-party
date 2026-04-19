import csv
import re
import os

def process_portal(input_txt, existing_csvs, output_csv):
    # 1. Load all existing emails from other lists to avoid duplicates
    existing_emails = set()
    for existing_csv in existing_csvs:
        try:
            with open(existing_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_emails.add(row['Email'].lower().strip())
        except FileNotFoundError:
            print(f"Warning: {existing_csv} not found. Skipping duplicate check against it.")

    # 2. Parse the raw portal list
    new_contacts = []
    seen_in_this_list = set()
    
    # Regex to capture just the email if it's alone, or within < >
    just_email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
    # Let's also handle the typo "yahoo.vom"
    typofix_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.vom)')

    raw_total = 0
    with open(input_txt, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().rstrip(',')
            if not line:
                continue
            
            raw_total += 1
            email = ""
            
            em_match = just_email_pattern.search(line)
            if em_match:
                email = em_match.group(1).strip().lower()
            else:
                # Handle the .vom typo explicitly
                typo_match = typofix_pattern.search(line)
                if typo_match:
                    email = typo_match.group(1).strip().lower().replace(".vom", ".com")
            
            if email:
                # Filter out the dummy test emails
                if email in ['a@a.com', 'yolo@gmail.com']:
                    continue
                
                # Check for uniqueness
                if email not in existing_emails and email not in seen_in_this_list:
                    new_contacts.append({
                        'FirstName': 'Supporter',  # Default since the form dump didn't have names attached
                        'LastName': '',
                        'Email': email,
                        'Tags': 'Community_Volunteer'
                    })
                    seen_in_this_list.add(email)

    # 4. Save the output
    with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['FirstName', 'LastName', 'Email', 'Tags'])
        writer.writeheader()
        writer.writerows(new_contacts)

    # 5. Print out the stats for the user
    print(f"📊 Portal List Results:")
    print(f"-------------------")
    print(f"Total raw lines pasted: {raw_total}")
    print(f"Total existing emails on file: {len(existing_emails)}")
    print(f"-------------------")
    print(f"✅ UNIQUE NEW PORTAL VOLUNTEERS ADDED: {len(new_contacts)}")
    print(f"🔥 These new contacts have been saved to {output_csv}")

if __name__ == "__main__":
    process_portal(
        input_txt='../data/raw_portal_contacts.txt',
        existing_csvs=['curated_precinct_chairs.csv', '../data/curated_undisclosed_list.csv'],
        output_csv='../data/curated_community_volunteers.csv'
    )
