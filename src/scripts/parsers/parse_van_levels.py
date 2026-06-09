import csv
import json
import re
import warnings

# Read the HTML export using pandas since it's an XLS file that contains an HTML table (common VAN export format)
import pandas as pd

warnings.filterwarnings("ignore")

try:
    # VAN "XLS" exports are almost always HTML tables
    dfs = pd.read_html(
        "Elections_Data/VAN_Access_Exports/UserListExport-9534069555.xls"
    )
    df = dfs[0]
except Exception as e:
    print(f"Failed to read XLS as HTML: {e}")
    exit(1)

# Check for Level 2 and Level 3 users
high_level_users = []
for _index, row in df.iterrows():
    # Convert row to string to check for levels
    row_str = " ".join(str(val).lower() for val in row.values)
    name = row.iloc[0] if len(row) > 0 else "Unknown"

    # Simple check - if the row contains level 2 or level 3 in the profile/security role
    if (
        "level 2" in row_str
        or "level 3" in row_str
        or "admin" in row_str
        or "director" in row_str
    ):
        # Extract just the relevant info to avoid printing the whole ugly row
        high_level_users.append(
            {
                "name": name,
                "details": [str(val) for val in row.values if str(val) != "nan"],
            }
        )

print(
    f"Found {len(high_level_users)} users with high-level access (Level 2, Level 3, Admin, etc):"
)
print("-" * 50)
for u in high_level_users:
    print(f"- {u['name']}")
    for d in u["details"][1:]:
        print(f"  > {d}")
    print()
