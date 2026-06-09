import os
import re

# Determine the absolute path to the project root based on the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHAIR_DATA_PATH = os.path.join(BASE_DIR, "js", "chair_data.js")
VAN_EXPORT_PATH = os.path.join(
    BASE_DIR, "Elections_Data", "VAN_Access_Exports", "UserListExport-9534069555.xls"
)
REPORT_PATH = os.path.join(
    BASE_DIR, "Elections_Data", "VAN_Access_Exports", "van_cross_reference_report.md"
)

# Read js/chair_data.js to extract official chairs
official_emails = set()
official_names = set()

try:
    with open(CHAIR_DATA_PATH, encoding="utf-8") as f:
        js_content = f.read()

    lines = js_content.split("\n")
    for line in lines:
        email_match = re.search(
            r'[\'"]([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)[\'"]', line
        )
        if email_match:
            official_emails.add(email_match.group(1).lower())

        name_match = re.search(
            r'(?:name|Name|chair|Chair)\s*:\s*[\'"]([^\'"]+)[\'"]', line
        )
        if name_match:
            official_names.add(name_match.group(1).lower().strip())
except FileNotFoundError:
    print(f"Warning: {CHAIR_DATA_PATH} not found.")

# Read the XLS file (tab-separated UTF-16)
van_users = []
try:
    with open(VAN_EXPORT_PATH, "rb") as f:
        content = f.read().decode("utf-16")
        rows = content.split("\n")
        if len(rows) > 0:
            header = rows[0].split("\t")
            for row in rows[1:]:
                if not row.strip():
                    continue
                cols = row.split("\t")
                if len(cols) >= 13:
                    last_name = cols[0].strip()
                    first_name = cols[1].strip()
                    email = cols[12].strip().lower()
                    role = cols[17].strip() if len(cols) > 17 else "Unknown"

                    van_users.append(
                        {
                            "Name": f"{first_name} {last_name}".strip(),
                            "Email": email,
                            "Role": role,
                            "FirstName": first_name.lower(),
                            "LastName": last_name.lower(),
                        }
                    )
except FileNotFoundError:
    print(f"Warning: {VAN_EXPORT_PATH} not found.")
except Exception as e:
    print(f"Error reading VAN export: {e}")

chairs_with_access = []
non_chairs_with_access = []

for user in van_users:
    is_chair = False
    if user["Email"] in official_emails and user["Email"] != "":
        is_chair = True
    else:
        for official_name in official_names:
            if user["FirstName"] in official_name and user["LastName"] in official_name:
                is_chair = True
                break

    if is_chair:
        chairs_with_access.append(user)
    else:
        non_chairs_with_access.append(user)

# Generate report
try:
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as out:
        out.write("# VAN Access Cross-Reference Report\n\n")
        out.write(f"**Total VAN Users Found:** {len(van_users)}\n")
        out.write(f"**Official Chairs with VAN Access:** {len(chairs_with_access)}\n")
        out.write(
            f"**Non-Chairs/Staff/Volunteers with VAN Access:** {len(non_chairs_with_access)}\n\n"
        )

        out.write("## 1. Official Precinct Chairs WITH VAN Access\n")
        out.write("| Name | Email | VAN Profile |\n")
        out.write("| --- | --- | --- |\n")
        for u in chairs_with_access:
            out.write(f"| {u['Name']} | {u['Email']} | {u['Role']} |\n")

        out.write("\n## 2. Non-Chairs / Staff / Volunteers WITH VAN Access\n")
        out.write("| Name | Email | VAN Profile |\n")
        out.write("| --- | --- | --- |\n")
        for u in non_chairs_with_access:
            out.write(f"| {u['Name']} | {u['Email']} | {u['Role']} |\n")

    print(f"Total Users: {len(van_users)}")
    print(f"Chairs: {len(chairs_with_access)}")
    print(f"Non-Chairs: {len(non_chairs_with_access)}")
    print(f"Report generated successfully at {REPORT_PATH}")
except Exception as e:
    print(f"Error writing report: {e}")
