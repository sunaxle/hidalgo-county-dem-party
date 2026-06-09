import pandas as pd
import os

# Load data
df = pd.read_csv('data/registered_voters.csv')

# Sort by Year and Election Cycle
df = df.sort_values(by=['Year', 'Election Cycle'])

# Separate into Primary and General
primary_df = df[df['Election Cycle'] == 'Primary Election'].copy().sort_values('Year')
general_df = df[df['Election Cycle'] == 'General Election'].copy().sort_values('Year')

# Calculate growth trends
primary_df['Previous Year'] = primary_df['Year'].shift(1)
primary_df['Previous Voters'] = primary_df['Registered Voters'].shift(1)
primary_df['Growth (%)'] = ((primary_df['Registered Voters'] - primary_df['Previous Voters']) / primary_df['Previous Voters']) * 100

general_df['Previous Year'] = general_df['Year'].shift(1)
general_df['Previous Voters'] = general_df['Registered Voters'].shift(1)
general_df['Growth (%)'] = ((general_df['Registered Voters'] - general_df['Previous Voters']) / general_df['Previous Voters']) * 100

# Total growth from first to last record
prim_first = primary_df.iloc[0]
prim_last = primary_df.iloc[-1]
prim_total_growth = ((prim_last['Registered Voters'] - prim_first['Registered Voters']) / prim_first['Registered Voters']) * 100

gen_first = general_df.iloc[0]
gen_last = general_df.iloc[-1]
gen_total_growth = ((gen_last['Registered Voters'] - gen_first['Registered Voters']) / gen_first['Registered Voters']) * 100

# Primary vs General per year
merged_df = pd.merge(primary_df[['Year', 'Registered Voters']], general_df[['Year', 'Registered Voters']], on='Year', suffixes=('_Primary', '_General'))
merged_df['Gen vs Prim Bump'] = merged_df['Registered Voters_General'] - merged_df['Registered Voters_Primary']
merged_df['Gen vs Prim Bump (%)'] = (merged_df['Gen vs Prim Bump'] / merged_df['Registered Voters_Primary']) * 100

# Generate Markdown
md_lines = []
md_lines.append("# Voter Registration Data Insights")
md_lines.append("\n> [!NOTE]")
md_lines.append("> Analysis of Hidalgo County voter registration trends based on historical CSV files (2006-2024).")

md_lines.append("\n## Primary Elections Registration Trend")
md_lines.append("| Year | Registered Voters | Growth from Previous Cycle |")
md_lines.append("|---|---|---|")
for idx, row in primary_df.iterrows():
    growth_str = f"{row['Growth (%)']:.2f}%" if pd.notnull(row['Growth (%)']) else "N/A"
    md_lines.append(f"| {int(row['Year'])} | {int(row['Registered Voters']):,} | {growth_str} |")

md_lines.append(f"\n**Total Primary Registration Growth ({int(prim_first['Year'])} - {int(prim_last['Year'])}):** {prim_total_growth:.2f}%")

md_lines.append("\n## General Elections Registration Trend")
md_lines.append("| Year | Registered Voters | Growth from Previous Cycle |")
md_lines.append("|---|---|---|")
for idx, row in general_df.iterrows():
    growth_str = f"{row['Growth (%)']:.2f}%" if pd.notnull(row['Growth (%)']) else "N/A"
    md_lines.append(f"| {int(row['Year'])} | {int(row['Registered Voters']):,} | {growth_str} |")

md_lines.append(f"\n**Total General Registration Growth ({int(gen_first['Year'])} - {int(gen_last['Year'])}):** {gen_total_growth:.2f}%")

md_lines.append("\n## Election Year Bump (Primary to General)")
md_lines.append("This table illustrates the increase in registered voters between the primary election and the general election within the same year.")
md_lines.append("\n| Year | Primary Registration | General Registration | Net Increase | % Bump |")
md_lines.append("|---|---|---|---|---|")
for idx, row in merged_df.iterrows():
    md_lines.append(f"| {int(row['Year'])} | {int(row['Registered Voters_Primary']):,} | {int(row['Registered Voters_General']):,} | {int(row['Gen vs Prim Bump']):,} | {row['Gen vs Prim Bump (%)']:.2f}% |")

# Save to artifact dir
output_path = '/Users/dr3/.gemini/antigravity/brain/936700d8-f44b-4e98-b470-3f397bb61b20/voter_data_insights.md'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    f.write('\n'.join(md_lines))

print("Insights saved to", output_path)
