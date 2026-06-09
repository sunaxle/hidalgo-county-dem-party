import sys

import pandas as pd

file_path = "precinct_107_data_upload/detail.xlsx"
xl = pd.ExcelFile(file_path)
print("Sheets:", xl.sheet_names)

# Let's peek into the first sheet
df = xl.parse(xl.sheet_names[0])
print(df.head(10))

# Also search for '107'
for sheet in xl.sheet_names:
    df = xl.parse(sheet)
    # Search for any cell containing '107'
    mask = df.apply(lambda row: row.astype(str).str.contains("107").any(), axis=1)
    if mask.any():
        print(f"\nFound 107 in sheet: {sheet}")
        print(df[mask].to_string())
