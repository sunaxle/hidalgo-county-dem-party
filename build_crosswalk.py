import pandas as pd
import glob
import os
import json

folder_path = '/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/Demographic data requests/'

# Define files
file_cc = os.path.join(folder_path, 'countycommissonersandprecincts.xls')
file_hd = os.path.join(folder_path, 'HDprecinctvshousedistricts.xls')
file_sd = os.path.join(folder_path, 'senatedistricts and precincts.xls')

# Function to parse VAN HTML-xls files safely
def extract_van_table(filepath):
    # read_html returns a list of dataframes found.
    # Usually in VAN exports, the actual data is the first or second table depending on headers.
    tables = pd.read_html(filepath, header=0) 
    
    # We look for the table that actually has our 'Precinct' column
    for df in tables:
        # Normalize column names by stripping whitespace and uppercase
        df.columns = df.columns.astype(str).str.strip().str.upper()
        if 'PRECINCT' in df.columns:
            return df
            
    # Fallback if header=0 grabbed the wrong row
    tables_no_head = pd.read_html(filepath)
    for df in tables_no_head:
        # Search the first few rows for the word "Precinct" to find the real header
        for idx in range(min(5, len(df))):
            row_values = [str(x).strip().upper() for x in df.iloc[idx].values]
            if 'PRECINCT' in row_values:
                # Set this row as header
                df.columns = row_values
                df = df.drop(range(idx + 1))
                return df

    return None

print("Processing County Commissioner Mapping...")
df_cc = extract_van_table(file_cc)
if df_cc is not None:
    # Rename columns to standard simple keys
    # Typically CC files have "County Comm" or similar
    df_cc = df_cc.rename(columns=lambda x: 'CC' if 'COUNTY COMM' in x else x)

print("Processing House District Mapping...")
df_hd = extract_van_table(file_hd)
if df_hd is not None:
    df_hd = df_hd.rename(columns=lambda x: 'HD' if 'STATE HOUSE' in x or 'HOUSE' in x else x)

print("Processing Senate District Mapping...")
df_sd = extract_van_table(file_sd)
if df_sd is not None:
    df_sd = df_sd.rename(columns=lambda x: 'SD' if 'STATE SENATE' in x or 'SENATE' in x else x)


# Now we perform a SQL-style OUTER JOIN on the PRECINCT column to merge all 3 sheets into one!
if df_cc is not None and df_hd is not None and df_sd is not None:
    # Filter only the columns we actually want to keep
    # CC should have PRECINCT and CC
    # HD should have PRECINCT and HD
    # SD should have PRECINCT and SD
    
    # Drop NAs in Precinct column
    df_cc = df_cc.dropna(subset=['PRECINCT']).copy()
    df_hd = df_hd.dropna(subset=['PRECINCT']).copy()
    df_sd = df_sd.dropna(subset=['PRECINCT']).copy()
    
    # Ensure precinct is string for clean merging
    df_cc['PRECINCT'] = df_cc['PRECINCT'].astype(str).str.replace(".0", "", regex=False)
    df_hd['PRECINCT'] = df_hd['PRECINCT'].astype(str).str.replace(".0", "", regex=False)
    df_sd['PRECINCT'] = df_sd['PRECINCT'].astype(str).str.replace(".0", "", regex=False)

    merged_df = pd.merge(df_cc[['PRECINCT', 'CC']], df_hd[['PRECINCT', 'HD']], on='PRECINCT', how='outer')
    master_df = pd.merge(merged_df, df_sd[['PRECINCT', 'SD']], on='PRECINCT', how='outer')
    
    # Convert to a clean list of dictionaries
    records = master_df.to_dict('records')
    
    # Write to a javascript file so the local HTML files can read it without a backend server
    js_output_path = '/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/js/precinct_mapping_data.js'
    
    with open(js_output_path, 'w') as f:
        f.write("const precinctDistricts = ")
        f.write(json.dumps(records, indent=4))
        f.write(";\n")
        
    print(f"\\nSUCCESS: Extracted and merged {len(records)} precincts.")
    print(f"Saved master Javascript crosswalk to: {js_output_path}")
    print("\nSample Output:")
    print(json.dumps(records[:3], indent=2))
else:
    print("FAILED to locate 'PRECINCT' column in one or more files.")
