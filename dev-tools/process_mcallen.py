import csv
import re
import os

def process_mcallen(input_csv, existing_csvs, output_csv):
    # 1. Load all existing emails from other lists to avoid duplicates
    existing_emails = set()
    total_existing = 0
    
    for existing_csv in existing_csvs:
        try:
            with open(existing_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('Email', '').lower().strip()
                    if email and email not in existing_emails:
                        existing_emails.add(email)
                        total_existing += 1
        except FileNotFoundError:
            print(f"Warning: {existing_csv} not found. Skipping duplicate check against it.")

    # 2. Parse the McAllen list
    new_contacts = []
    seen_in_this_list = set()
    raw_total = 0

    with open(input_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_total += 1
            email = row.get('Email', '').lower().strip()
            first_name = row.get('First name', '').strip()
            last_name = row.get('Last name', '').strip()
            phone = row.get('Mobile number', '').strip()
            
            if not email:
                continue
                
            # Filter out dummies if any sneaked in
            if email in ['a@a.com', 'yolo@gmail.com']:
                continue
                
            # Check for uniqueness
            if email not in existing_emails and email not in seen_in_this_list:
                new_contacts.append({
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': email,
                    'Phone': phone,
                    'Tags': 'Talarico_Recruit'
                })
                seen_in_this_list.add(email)

    # 3. Save the output
    with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['FirstName', 'LastName', 'Email', 'Phone', 'Tags'])
        writer.writeheader()
        writer.writerows(new_contacts)

    # 4. Print out the stats for the user
    new_grand_total = total_existing + len(new_contacts)
    
    print(f"📊 McAllen Signups Results:")
    print(f"-------------------")
    print(f"Total raw signups in CSV: {raw_total}")
    print(f"Total existing unique emails on file: {total_existing}")
    print(f"-------------------")
    print(f"✅ UNIQUE NEW TALARICO RECRUITS ADDED: {len(new_contacts)}")
    print(f"🌎 NEW GRAND TOTAL ARMY SIZE: {new_grand_total}")
    print(f"🔥 These new contacts have been saved to {output_csv}")

if __name__ == "__main__":
    process_mcallen(
        input_csv='../data/McAllen Signups.csv',
        existing_csvs=[
            'curated_precinct_chairs.csv', 
            '../data/curated_undisclosed_list.csv',
            '../data/curated_community_volunteers.csv'
        ],
        output_csv='../data/curated_talarico_new_recruits.csv'
    )
