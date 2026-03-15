import pandas as pd
import json
import os

folder_path = '/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/Demographic data requests/'

# Define files
file_cc = os.path.join(folder_path, 'countycommissonersandprecincts.xls')
file_hd = os.path.join(folder_path, 'HDprecinctvshousedistricts.xls')
file_sd = os.path.join(folder_path, 'senatedistricts and precincts.xls')

try:
    # Read the data, using html reader since these older VAN .xls files are often just HTML tables exported with an .xls extension
    try:
        df_cc = pd.read_excel(file_cc)
    except:
        df_cc = pd.read_html(file_cc)[0]
        
    try:
        df_hd = pd.read_excel(file_hd)
    except:
        df_hd = pd.read_html(file_hd)[0]
        
    try:
        df_sd = pd.read_excel(file_sd)
    except:
        df_sd = pd.read_html(file_sd)[0]
        

    # We need to print the columns to understand how VAN named them so we can merge them
    print("Columns in County Commissioner File:", df_cc.columns.tolist())
    print("Columns in House File:", df_hd.columns.tolist())
    print("Columns in Senate File:", df_sd.columns.tolist())
    
    # Let's also print the first few rows to see the data structure
    print("\nSample CC Data:")
    print(df_cc.head(3))
    
    print("\nSample HD Data:")
    print(df_hd.head(3))
    
except Exception as e:
    print(f"Error reading files: {e}")
    # Fallback to read them as raw text to inspect if they are weirdly formatted CSVs or HTML
    with open(file_cc, 'r', encoding='utf-8', errors='ignore') as f:
        print("\nRaw format preview:")
        print(f.read(500))
