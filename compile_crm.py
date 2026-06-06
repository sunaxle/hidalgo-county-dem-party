import csv
import json
import os
import re
from datetime import datetime

OUTPUT_FILE = 'compiled_crm_list.csv'
OUTPUT_HEADERS = ['FirstName', 'LastName', 'Email', 'Phone', 'Origin', 'Tags', 'DateAdded']

all_contacts = []
seen_emails = set()
seen_phones = set()

def normalize_phone(phone):
    if not phone:
        return ''
    # Remove all non-digits
    digits = re.sub(r'\D', '', str(phone))
    # If it has a leading 1 and is 11 digits, strip it
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]
    return digits

def normalize_email(email):
    if not email:
        return ''
    return str(email).strip().lower()

def add_contact(first, last, email, phone, origin, tags='', date_added=''):
    first = first.strip() if first else ''
    last = last.strip() if last else ''
    
    norm_email = normalize_email(email)
    norm_phone = normalize_phone(phone)
    
    # Check if empty contact
    if not first and not last and not norm_email and not norm_phone:
        return

    # Check for duplicates
    is_duplicate = False
    if norm_email and norm_email in seen_emails:
        is_duplicate = True
    if norm_phone and norm_phone in seen_phones:
        is_duplicate = True

    if is_duplicate:
        return # Skip duplicate

    if norm_email:
        seen_emails.add(norm_email)
    if norm_phone:
        seen_phones.add(norm_phone)

    all_contacts.append({
        'FirstName': first,
        'LastName': last,
        'Email': email.strip() if email else '',
        'Phone': str(phone).strip() if phone else '',
        'Origin': origin,
        'Tags': tags,
        'DateAdded': date_added
    })

# 1. McAllen Signups.csv
try:
    with open('data/McAllen Signups.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('First name', ''),
                last=row.get('Last name', ''),
                email=row.get('Email', ''),
                phone=row.get('Mobile number', ''),
                origin='McAllen Signups',
                date_added=row.get('Signup created time', '')
            )
except Exception as e:
    print(f"Error reading McAllen Signups: {e}")

# 2. curated_community_volunteers.csv
try:
    with open('data/curated_community_volunteers.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('FirstName', ''),
                last=row.get('LastName', ''),
                email=row.get('Email', ''),
                phone='',
                origin='Curated Community Volunteers',
                tags=row.get('Tags', '')
            )
except Exception as e:
    print(f"Error reading curated_community_volunteers: {e}")

# 3. curated_talarico_new_recruits.csv
try:
    with open('data/curated_talarico_new_recruits.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('FirstName', ''),
                last=row.get('LastName', ''),
                email=row.get('Email', ''),
                phone=row.get('Phone', ''),
                origin='Talarico New Recruits',
                tags=row.get('Tags', '')
            )
except Exception as e:
    print(f"Error reading curated_talarico_new_recruits: {e}")

# 4. curated_undisclosed_list.csv
try:
    with open('data/curated_undisclosed_list.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('FirstName', ''),
                last=row.get('LastName', ''),
                email=row.get('Email', ''),
                phone='',
                origin='Undisclosed List',
                tags=row.get('Tags', '')
            )
except Exception as e:
    print(f"Error reading curated_undisclosed_list: {e}")

# 5. old volunteer list 24-25.csv
try:
    with open('data/old volunteer list 24-25.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('first_name', ''),
                last=row.get('last_name', ''),
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                origin='Old Volunteer List 24-25',
                date_added=row.get('created_at', '')
            )
except Exception as e:
    print(f"Error reading old volunteer list 24-25: {e}")

# 6. top_tier_democrats.csv
try:
    with open('data/top_tier_democrats.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('First Name', ''),
                last=row.get('Last Name', ''),
                email=row.get('Email', ''),
                phone='',
                origin='Top Tier Democrats',
                tags=row.get('List Name', '')
            )
except Exception as e:
    print(f"Error reading top_tier_democrats: {e}")

# 7. young_dems.csv
try:
    with open('data/young_dems.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('First Name', ''),
                last=row.get('Last Name', ''),
                email=row.get('Email', ''),
                phone=row.get('Phone', ''),
                origin='Young Dems'
            )
except Exception as e:
    print(f"Error reading young_dems: {e}")

# 8. HCDP_Precinct_Contacts.csv
try:
    with open('HCDP_Precinct_Contacts.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(
                first=row.get('first', ''),
                last=row.get('last', ''),
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                origin='HCDP Precinct Contacts',
                tags=f"Precinct {row.get('precinct', '')}"
            )
except Exception as e:
    print(f"Error reading HCDP_Precinct_Contacts: {e}")

# 9. new_chairs.tsv
try:
    with open('new_chairs.tsv', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 6:
                if parts[0] == 'Accepted' or parts[0] == 'Won' or parts[0] == 'Status':
                    continue # skip header or non-data if needed
                add_contact(
                    first=parts[3],
                    last=parts[2],
                    email=parts[5],
                    phone=parts[4],
                    origin='New Chairs List',
                    tags=f"Status: {parts[0]}, Precinct: {parts[1]}"
                )
except Exception as e:
    print(f"Error reading new_chairs: {e}")

# 10. p192_non_voters.csv
try:
    with open('data/emaildatasettest/p192_non_voters.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # We must verify if there's actually contact info, but the file doesn't have email/phone!
            # However, for deduplication by name/address? We don't have address in master list yet.
            # We'll just add them if they aren't completely empty, but they won't dedupe against emails since they have none.
            # To prevent huge duplicate names, we could dedupe by name, but name collisions are real.
            # We'll let them pass through since they don't have contact info to dedupe.
            add_contact(
                first=row.get('FirstName', ''),
                last=row.get('LastName', ''),
                email='',
                phone='',
                origin='P192 Non Voters',
                tags=f"Age: {row.get('Age', '')}, SuperDem: {row.get('Lives_With_Super_Dem', '')}"
            )
except Exception as e:
    print(f"Error reading p192_non_voters: {e}")

# 11. JSON - master_candidates_2026.json
try:
    with open('data/master_candidates_2026.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            add_contact(
                first=item.get('first_name', ''),
                last=item.get('last_name', ''),
                email=item.get('email', ''),
                phone=item.get('phone', ''),
                origin='Master Candidates 2026',
                tags=f"Office: {item.get('office', '')}"
            )
except Exception as e:
    print(f"Error reading master_candidates_2026.json: {e}")

# 12. JSON - judicial_candidates_and_officials.json
try:
    with open('data/judicial_candidates_and_officials.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            add_contact(
                first=item.get('first_name', ''),
                last=item.get('last_name', ''),
                email=item.get('email', ''),
                phone=item.get('phone', ''),
                origin='Judicial Candidates and Officials',
                tags=f"Office: {item.get('office_full', '')}"
            )
except Exception as e:
    print(f"Error reading judicial_candidates_and_officials.json: {e}")

# Write to output
with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADERS)
    writer.writeheader()
    writer.writerows(all_contacts)

print(f"Successfully compiled {len(all_contacts)} UNIQUE contacts into {OUTPUT_FILE}")
