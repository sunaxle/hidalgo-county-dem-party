import os

import pandas as pd

file_path = "2026_Election_Data/Precinct Performance Primary 26 HD 41/41pctbreak.xlsx"

try:
    df = pd.read_excel(file_path, header=None, nrows=5)
    print(df.to_string())
except Exception as e:
    print(f"Error reading file: {e}")
