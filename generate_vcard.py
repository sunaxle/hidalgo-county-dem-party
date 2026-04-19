import json

def generate_vcard():
    with open('data/master_candidates_2026.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)

    vcard_lines = []
    
    for c in candidates:
        fname = c.get('first_name', '').strip()
        lname = c.get('last_name', '').strip()
        
        if not fname and not lname:
            continue
            
        office = c.get('office', '').strip()
        email = c.get('email', '').strip()
        phone = c.get('phone', '').strip()
        
        # Build vCard
        vcard_lines.append("BEGIN:VCARD")
        vcard_lines.append("VERSION:3.0")
        vcard_lines.append(f"N:{lname};{fname};;;")
        
        fn = f"{fname} {lname}".strip()
        vcard_lines.append(f"FN:{fn}")
        
        # Adding to the specific list in iCloud / iOS
        vcard_lines.append("CATEGORIES:Elected Official phone numbers 2026")
        
        if office:
            vcard_lines.append(f"ORG:{office}")
            vcard_lines.append(f"TITLE:{office}")
            
        if email:
            # Handle multiple emails like "email1 / email2"
            emails = [e.strip() for e in email.replace('/', ',').split(',') if e.strip()]
            for e in emails:
                vcard_lines.append(f"EMAIL;type=INTERNET;type=WORK:{e}")
                
        if phone:
            vcard_lines.append(f"TEL;type=WORK;type=VOICE:{phone}")
            
        vcard_lines.append("END:VCARD")
        
    with open('data/hidalgo_dems_contacts.vcf', 'w', encoding='utf-8') as f:
        f.write('\n'.join(vcard_lines))
        
if __name__ == '__main__':
    generate_vcard()
    print("vCard generated successfully with the CATEGORIES field for the iCloud List.")
