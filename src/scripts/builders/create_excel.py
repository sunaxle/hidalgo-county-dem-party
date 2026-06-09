import pandas as pd

# Read the CSV
df = pd.read_csv("precinct_103_voters.csv")

# Texas VAN (VoteBuilder) matching works best with just the VUID.
# We'll put VUID first, followed by Name.
df = df[["VUID", "Name"]]

# Save to Excel
df.to_excel("precinct_103_van_upload.xlsx", index=False)
print("Created precinct_103_van_upload.xlsx")
