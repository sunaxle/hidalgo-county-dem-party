import re

import pandas as pd

with open("detail.txt") as f:
    lines = f.readlines()

data = []
parsing_turnout = False

for line in lines:
    if line.startswith("Precinct") and "Voter Turnout" in line:
        if not parsing_turnout:
            parsing_turnout = True
        else:
            break
        continue
    if line.startswith("Total:"):
        parsing_turnout = False
        continue
    if parsing_turnout:
        if line.strip() == "":
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 4:
            pct = parts[0]
            reg = int(parts[1])
            cast = int(parts[2])
            turnout = float(parts[3].replace("%", ""))
            data.append(
                {
                    "Precinct": pct,
                    "Registered_Voters": reg,
                    "Ballots_Cast": cast,
                    "Turnout_Pct": turnout,
                }
            )

df = pd.DataFrame(data)


def df_to_markdown(df):
    header = "| " + " | ".join(df.columns) + " |\n"
    header += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"
    rows = ""
    for _, row in df.iterrows():
        rows += "| " + " | ".join([str(val) for val in row.values]) + " |\n"
    return header + rows


with open("runoff_analysis.md", "w") as out:
    out.write("# Hidalgo County Primary Runoff Analysis\n\n")
    out.write(
        "This report analyzes the official precinct-by-precinct voting data for the most recent primary runoff.\n\n"
    )

    out.write(f"**Total Registered Voters:** {df['Registered_Voters'].sum()}\n")
    out.write(f"**Total Ballots Cast:** {df['Ballots_Cast'].sum()}\n")
    overall_turnout = (
        df["Ballots_Cast"].sum() / df["Registered_Voters"].sum() * 100
        if df["Registered_Voters"].sum() > 0
        else 0
    )
    out.write(f"**Overall Turnout:** {overall_turnout:.2f}%\n\n")

    out.write("## Top 10 Precincts by Turnout Percentage\n")
    out.write(
        df_to_markdown(df.sort_values("Turnout_Pct", ascending=False).head(10)) + "\n\n"
    )

    out.write("## Top 10 Precincts by Total Ballots Cast\n")
    out.write(
        df_to_markdown(df.sort_values("Ballots_Cast", ascending=False).head(10))
        + "\n\n"
    )

    out.write("## Bottom 10 Precincts by Turnout Percentage\n")
    out.write(
        df_to_markdown(df.sort_values("Turnout_Pct", ascending=True).head(10)) + "\n\n"
    )
