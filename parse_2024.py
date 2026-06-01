import pandas as pd
import sys

file_path = "precinct_107_data_upload/detail.xls"

try:
    # Try reading as excel first
    try:
        xl = pd.ExcelFile(file_path, engine='xlrd')
        sheets = xl.sheet_names
        print("Excel format detected. Sheets:", sheets)
        for sheet in sheets:
            df = xl.parse(sheet)
            mask = df.apply(lambda row: row.astype(str).str.contains('107').any(), axis=1)
            if mask.any():
                print(f"--- Sheet: {sheet} ---")
                print(df[mask].to_string())
    except Exception as e:
        print("Not standard excel or missing xlrd, trying read_html:", e)
        # Try reading as HTML table (Clarity often exports HTML as .xls)
        dfs = pd.read_html(file_path)
        print(f"Found {len(dfs)} tables in HTML format.")
        for i, df in enumerate(dfs):
            mask = df.apply(lambda row: row.astype(str).str.contains('107').any(), axis=1)
            if mask.any():
                print(f"--- Table {i} ---")
                print(df[mask].to_string())

except Exception as e:
    print("Error parsing:", e)
