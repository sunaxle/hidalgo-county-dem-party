import csv
import re
import os

def parse_pasted_contacts(input_txt, existing_csv, output_csv):
    # 1. Load the existing curated emails so we can deduplicate against it
    existing_emails = set()
    try:
        with open(existing_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_emails.add(row['Email'].lower().strip())
    except FileNotFoundError:
        print(f"Warning: {existing_csv} not found. Proceeding without deduplicating against it.")

    # 2. Parse the raw text file
    new_contacts = []
    
    # Regex to capture "Name <email>" or just "email" or "<email>"
    # Example 1: Abe Sanchez <abe@gmail.com>,
    # Example 2: "Alma" <alma@yahoo.com>,
    # Example 3: "ltmcleaish@aol.com" <ltmcleaish@aol.com>,
    email_pattern = re.compile(r'([^<]*?)\s*<([^>]+)>')
    just_email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

    raw_total = 0
    with open(input_txt, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().rstrip(',')
            if not line:
                continue
            
            raw_total += 1
            match = email_pattern.search(line)
            
            first_name = ""
            last_name = ""
            email = ""
            
            if match:
                raw_name = match.group(1).replace('"', '').strip()
                email = match.group(2).strip().lower()
                
                # Split raw name into first/last if possible
                if raw_name:
                    parts = raw_name.split()
                    if len(parts) > 1:
                        first_name = parts[0]
                        last_name = " ".join(parts[1:])
                    else:
                        first_name = parts[0]
            else:
                # Try to just find an email
                em_match = just_email_pattern.search(line)
                if em_match:
                    email = em_match.group(1).strip().lower()
            
            # Avoid the weird "email" <email> format where name is just the email
            if "@" in first_name:
                first_name = ""
            
            if email:
                new_contacts.append({
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': email,
                    'Tags': 'Undisclosed_List'
                })

    # 3. Deduplicate
    unique_new_contacts = []
    seen_in_this_list = set()
    
    for contact in new_contacts:
        em = contact['Email']
        if em not in existing_emails and em not in seen_in_this_list:
            unique_new_contacts.append(contact)
            seen_in_this_list.add(em)
            
    # 4. Save the output
    with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['FirstName', 'LastName', 'Email', 'Tags'])
        writer.writeheader()
        writer.writerows(unique_new_contacts)

    # 5. Print out the stats for the user
    print(f"📊 Curation Results:")
    print(f"-------------------")
    print(f"Total raw lines pasted: {raw_total}")
    print(f"Total valid emails extracted: {len(new_contacts)}")
    print(f"Total existing Precinct Chair emails: {len(existing_emails)}")
    print(f"-------------------")
    print(f"✅ UNIQUE NEW CONTACTS ADDED: {len(unique_new_contacts)}")
    print(f"🔥 These {len(unique_new_contacts)} unique contacts have been saved to {output_csv}")

if __name__ == "__main__":
    parse_pasted_contacts(
        input_txt='../data/raw_pasted_contacts.txt',
        existing_csv='curated_precinct_chairs.csv',
        output_csv='../data/curated_undisclosed_list.csv'
    )
