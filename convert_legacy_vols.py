import csv
import random

input_file = "data/old volunteer list 24-25.csv"
output_file = "data/mock_volunteers.csv"

# Roles to distribute
roles = ["Precinct Chair", "Block Captain", "General Volunteer"]

out_rows = []
out_headers = ["Timestamp", "First Name", "Last Name", "Email", "Phone", "Role", "Precinct Number", "Photo Link", "Short Bio"]

# We'll put 60 people into the system so the hub looks populated
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 60:
                break
                
            first = row.get("first_name", "").strip().title()
            last = row.get("last_name", "").strip().title()
            email = row.get("email", "").strip()
            phone = row.get("phone", "").strip()
            
            if not first or not last:
                continue
                
            # Randomly assign a precinct between 1 and 280
            pct = random.randint(1, 280)
            
            # Weighted random role: 40% Chair, 30% Captain, 30% General Volunteer
            role = random.choices(roles, weights=[40, 30, 30])[0]
            
            bio = f"Hi, I'm {first}. I've been a proud Democrat in Hidalgo County for years and am ready to help organize our community for the upcoming elections!"
            
            photo = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png"
            
            out_rows.append({
                "Timestamp": "3/19/2026 12:00:00",
                "First Name": first,
                "Last Name": last,
                "Email": email,
                "Phone": phone,
                "Role": role,
                "Precinct Number": pct,
                "Photo Link": photo,
                "Short Bio": bio
            })
            count += 1

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=out_headers)
        writer.writeheader()
        for r in out_rows:
            writer.writerow(r)

    print(f"Successfully converted {len(out_rows)} volunteers into profile cards!")

except Exception as e:
    print(f"Error: {e}")
