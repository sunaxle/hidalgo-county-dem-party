import pandas as pd
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('Elections_Data/VAN_Access_Exports/UserListExport-9534069555.xls', sep='\t', encoding='utf-16')

level3_users = []
cols = [c for c in df.columns if isinstance(c, str)]

for index, row in df.iterrows():
    row_str = " ".join(str(val).lower() for val in row.values)
    
    name = "Unknown"
    for col in cols:
        if 'name' in col.lower():
            name = str(row[col])
            break
    if name == "Unknown" and len(row) > 0:
        name = str(row.iloc[0])
    
    # In Texas VAN, Level 3 is usually denoted as "Texas (3) Campaign Manager" or similar
    if '(3)' in row_str or 'level 3' in row_str or 'level-3' in row_str:
        level3_users.append({
            'name': name,
            'details': [f"{col}: {val}" for col, val in zip(df.columns, row.values) if str(val) != 'nan']
        })

if len(level3_users) > 0:
    print(f"Found {len(level3_users)} users with Level 3 access:")
    print("=" * 50)
    for u in level3_users:
        print(f"👤 {u['name']}")
        for d in u['details']:
            if '(3)' in d.lower() or 'level 3' in d.lower():
                print(f"   --> {d}")
        print("-" * 50)
else:
    print("Zero users found with Level 3 access.")
