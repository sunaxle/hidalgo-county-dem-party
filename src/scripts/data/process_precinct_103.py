import glob
import os

import pandas as pd

# Find all Excel files
files = glob.glob("precinct_103_data/*.xlsx")
all_names = []

for file in files:
    df = pd.read_excel(file)
    # Check if 'Precinct' column exists
    if "Precinct" in df.columns:
        # Filter for Precinct 103 (handle both numeric and string types)
        df_103 = df[df["Precinct"].astype(str).str.strip() == "103"]

        # Check column format
        if "VoterName" in df_103.columns:
            # Format: 'VoterName', 'VUID', 'Precinct'
            for _idx, row in df_103.iterrows():
                all_names.append(
                    {
                        "Name": row["VoterName"],
                        "VUID": row["VUID"],
                        "Source": os.path.basename(file),
                    }
                )
        elif "Last Name" in df_103.columns and "First Name" in df_103.columns:
            # Format: 'VUID', 'Last Name', 'First Name', 'Middle Name', 'Name Suffix', 'Precinct'
            for _idx, row in df_103.iterrows():
                # Construct name
                last = str(row["Last Name"]) if pd.notna(row["Last Name"]) else ""
                first = str(row["First Name"]) if pd.notna(row["First Name"]) else ""
                middle = str(row["Middle Name"]) if pd.notna(row["Middle Name"]) else ""
                suffix = str(row["Name Suffix"]) if pd.notna(row["Name Suffix"]) else ""

                parts = [last + ","]
                if first:
                    parts.append(first)
                if middle:
                    parts.append(middle)
                if suffix:
                    parts.append(suffix)

                full_name = " ".join(parts).strip()

                all_names.append(
                    {
                        "Name": full_name,
                        "VUID": row["VUID"],
                        "Source": os.path.basename(file),
                    }
                )

# Create final dataframe and save to CSV
result_df = pd.DataFrame(all_names)
if not result_df.empty:
    # Remove duplicates based on VUID if they exist across files
    result_df = result_df.drop_duplicates(subset=["VUID"])

    # Sort alphabetically
    result_df = result_df.sort_values(by="Name")

    # Save to CSV
    result_df.to_csv("precinct_103_voters.csv", index=False)
    print(f"Successfully extracted {len(result_df)} unique voters from Precinct 103.")
    print("Saved to precinct_103_voters.csv")
else:
    print("No voters found in Precinct 103.")
