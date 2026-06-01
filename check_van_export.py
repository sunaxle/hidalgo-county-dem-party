import pandas as pd
import os

file_path = "2026_Election_Data/Precinct Performance Primary 26 HD 41/DemographicsNew.xls"

try:
    # Sometimes VAN exports XLS as HTML or messy CSV, but let's try reading as excel or csv.
    # We will use pandas read_excel, but if it fails we might need read_html.
    df = pd.read_excel(file_path, engine='xlrd')
    print("Columns:", list(df.columns))
    print("\nFirst 10 rows:")
    print(df.head(10).to_string())
except Exception as e:
    print(f"Error reading file with read_excel: {e}")
    try:
        df = pd.read_html(file_path)[0]
        print("Read as HTML. Columns:", list(df.columns))
        print("\nFirst 10 rows:")
        print(df.head(10).to_string())
    except Exception as e2:
        print(f"Error reading as HTML: {e2}")
