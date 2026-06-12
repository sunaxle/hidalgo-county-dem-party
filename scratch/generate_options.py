import pandas as pd

# Load the CSV
df = pd.read_csv('/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/HCDP_Precinct_Contacts.csv')

# Drop nulls if necessary and sort by precinct
df = df.sort_values(by='precinct')

html_options = '<option value="" disabled selected>Select your Precinct & Name...</option>\n'

for index, row in df.iterrows():
    precinct = row['precinct']
    first = str(row['first']).strip()
    last = str(row['last']).strip()
    name = f"{first} {last}"
    if pd.isna(row['first']) or first == 'nan':
        name = "Unknown"
    
    option_value = f"Precinct {precinct} - {name}"
    html_options += f'          <option value="{option_value}">{option_value}</option>\n'

# We'll save this to a file
with open('/Users/dr3/Documents/Antigravity Designs/Politics/hidalgo-county-dem-party/scratch/options.html', 'w') as f:
    f.write(html_options)
print("Options generated.")
