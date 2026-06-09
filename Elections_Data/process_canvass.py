import re

import pandas as pd

with open("raw_canvass.txt") as f:
    text = f.read()

# Extract Lt Gov Race Data (Democratic)
lt_gov_section = re.split(r"Lieutenant Governor - Democratic Party", text)
lt_gov_data = []

# Compile regex to match precinct rows which look like:
# 001\n3\n2\n5\n0\n0\n0\n2\n3\n5\n1,039\n0.48%
pattern = re.compile(
    r"^(\d{3})\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d,]+)\n([\d.]+)%$",
    re.MULTILINE,
)

for i in range(1, len(lt_gov_section)):
    # Break at the next race
    section = lt_gov_section[i].split("Attorney General - Democratic Party")[0]
    matches = pattern.finditer(section)
    for m in matches:
        lt_gov_data.append(
            {
                "Precinct": m.group(1),
                "Velez": int(m.group(2).replace(",", "")),
                "Goodwin": int(m.group(3).replace(",", "")),
                "Cast_Votes": int(m.group(4).replace(",", "")),
                "Undervotes": int(m.group(5).replace(",", "")),
                "Absentee": int(m.group(7).replace(",", "")),
                "Early_Voting": int(m.group(8).replace(",", "")),
                "Election_Day": int(m.group(9).replace(",", "")),
                "Total_Ballots": int(m.group(10).replace(",", "")),
                "Registered": int(m.group(11).replace(",", "")),
                "Turnout_Pct": float(m.group(12)),
            }
        )

df_lt_gov = pd.DataFrame(lt_gov_data).drop_duplicates("Precinct")

# Calculate insights
with open("canvass_insights.md", "w") as f:
    f.write("# Hidalgo County Primary Runoff Canvas Analysis\n\n")
    f.write("## 1. Voting Methods Breakdown (Democratic Primary)\n")
    total_absentee = df_lt_gov["Absentee"].sum()
    total_early = df_lt_gov["Early_Voting"].sum()
    total_ed = df_lt_gov["Election_Day"].sum()
    total_ballots = df_lt_gov["Total_Ballots"].sum()

    if total_ballots > 0:
        f.write(
            f"- **Absentee / Mail-in:** {total_absentee} ({total_absentee / total_ballots * 100:.1f}%)\n"
        )
        f.write(
            f"- **Early Voting:** {total_early} ({total_early / total_ballots * 100:.1f}%)\n"
        )
        f.write(
            f"- **Election Day:** {total_ed} ({total_ed / total_ballots * 100:.1f}%)\n\n"
        )
        f.write(
            "> **Insight:** Early Voting is the dominant method. Resource allocation for GOTV efforts should heavily front-load during the Early Voting period rather than Election Day.\n\n"
        )

    f.write("## 2. Lieutenant Governor Race Analysis\n")
    total_velez = df_lt_gov["Velez"].sum()
    total_goodwin = df_lt_gov["Goodwin"].sum()
    total_votes = df_lt_gov["Cast_Votes"].sum()
    total_undervotes = df_lt_gov["Undervotes"].sum()

    if total_votes > 0:
        f.write(
            f"- **Marcos Isaias Velez:** {total_velez} ({total_velez / total_votes * 100:.1f}%)\n"
        )
        f.write(
            f"- **Vikki Goodwin:** {total_goodwin} ({total_goodwin / total_votes * 100:.1f}%)\n"
        )
        f.write(
            f"- **Undervotes (Ballot Drop-off):** {total_undervotes} ({(total_undervotes / total_ballots * 100):.1f}% of total ballots)\n\n"
        )

        # Win margins
        df_lt_gov["Margin"] = (df_lt_gov["Velez"] - df_lt_gov["Goodwin"]).abs()
        df_lt_gov["Winner"] = df_lt_gov.apply(
            lambda row: (
                "Velez"
                if row["Velez"] > row["Goodwin"]
                else ("Goodwin" if row["Goodwin"] > row["Velez"] else "Tie")
            ),
            axis=1,
        )

        f.write("### Precinct Performance\n")
        f.write(
            f"- **Precincts won by Velez:** {len(df_lt_gov[df_lt_gov['Winner'] == 'Velez'])}\n"
        )
        f.write(
            f"- **Precincts won by Goodwin:** {len(df_lt_gov[df_lt_gov['Winner'] == 'Goodwin'])}\n"
        )
        f.write(
            f"- **Tied Precincts:** {len(df_lt_gov[df_lt_gov['Winner'] == 'Tie'])}\n\n"
        )

        f.write("### Strongest Precincts for Velez (by margin)\n")
        top_velez = (
            df_lt_gov[df_lt_gov["Winner"] == "Velez"]
            .sort_values("Margin", ascending=False)
            .head(5)
        )
        for _, row in top_velez.iterrows():
            f.write(
                f"- **Pct {row['Precinct']}:** Velez +{row['Margin']} ({row['Velez']} to {row['Goodwin']})\n"
            )

        f.write("\n### Strongest Precincts for Goodwin (by margin)\n")
        top_goodwin = (
            df_lt_gov[df_lt_gov["Winner"] == "Goodwin"]
            .sort_values("Margin", ascending=False)
            .head(5)
        )
        for _, row in top_goodwin.iterrows():
            f.write(
                f"- **Pct {row['Precinct']}:** Goodwin +{row['Margin']} ({row['Goodwin']} to {row['Velez']})\n"
            )
