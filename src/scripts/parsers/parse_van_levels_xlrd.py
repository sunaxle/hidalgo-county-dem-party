import warnings

import pandas as pd

warnings.filterwarnings("ignore")

try:
    # Try reading as actual Excel file first (VAN sometimes outputs true Excel)
    df = pd.read_excel(
        "Elections_Data/VAN_Access_Exports/UserListExport-9534069555.xls"
    )
except Exception as e:
    print(f"Failed to read as Excel: {e}")
    try:
        # Fallback to reading it with a different engine or trying to decode it
        import chardet

        with open(
            "Elections_Data/VAN_Access_Exports/UserListExport-9534069555.xls", "rb"
        ) as f:
            raw_data = f.read(1000)
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

        # If it's a tab-separated fake XLS
        df = pd.read_csv(
            "Elections_Data/VAN_Access_Exports/UserListExport-9534069555.xls",
            sep="\t",
            encoding=encoding,
            on_bad_lines="skip",
        )
    except Exception as e2:
        print(f"Failed all reading methods: {e2}")
        exit(1)

# Check for Level 2 and Level 3 users
high_level_users = []

# Try to find columns that might represent User Profile, Role, or Level
cols = [c for c in df.columns if isinstance(c, str)]

for _index, row in df.iterrows():
    row_str = " ".join(str(val).lower() for val in row.values)

    # Try to find the name column (usually first or named 'Name')
    name = "Unknown"
    for col in cols:
        if "name" in col.lower():
            name = str(row[col])
            break
    if name == "Unknown" and len(row) > 0:
        name = str(row.iloc[0])

    # Looking for Level 2 or Level 3
    if (
        "level 2" in row_str
        or "level 3" in row_str
        or "level-2" in row_str
        or "level-3" in row_str
        or "admin" in row_str
    ):
        high_level_users.append(
            {
                "name": name,
                "details": [
                    f"{col}: {val}"
                    for col, val in zip(df.columns, row.values, strict=False)
                    if str(val) != "nan"
                ],
            }
        )

print(
    f"\nFound {len(high_level_users)} users with high-level access (Level 2, Level 3, Admin):"
)
print("=" * 70)
for u in high_level_users:
    print(f"👤 {u['name']}")
    for d in u["details"]:
        # Only print details that contain the interesting levels to keep output clean
        if "level 2" in d.lower() or "level 3" in d.lower() or "admin" in d.lower():
            print(f"   --> {d}")
    print("-" * 70)
