import csv

raw_input = "saul133@hotmail.com, alexfortexas02@gmail.com, lgala03@gmail.com, carlosrepettoayala@gmail.com, abram.mckee01@gmail.com, yanezjacqueline1210@gmail.com, paulmv55@yahoo.com, j.g.iii@hotmail.com, saragailb2gmail.com, benitezmarco2327@gmail.com, jason delattre01@gmail.com, nyssacruz@gmail.com"

# Clean the raw input string
emails = [e.strip() for e in raw_input.split(',')]

# Fix obvious typos: missing @ sign, stray spaces
cleaned_emails = []
for e in emails:
    e = e.replace(' ', '')
    if 'gmail.com' in e and '@' not in e:
        e = e.replace('gmail.com', '@gmail.com')
    cleaned_emails.append(e)

# Append to the CSV
with open('data/top_tier_democrats.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for email in cleaned_emails:
        writer.writerow(['', '', email, 'First round top tier democrats'])

print(f"Successfully appended {len(cleaned_emails)} new emails to data/top_tier_democrats.csv")
