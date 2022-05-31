import streamlit as st
import pandas as pd

pd.options.display.max_columns = 999

st.title("UCSB 2021-2022 season stats")

players = [
    "4900668/cole-anderson",
    "4900669/ariel-bland",
    "4702594/gage-gomez",
    #'4900670/henry-hartwell',
    #'4592899/zach-harvey',
    "4397646/robinson-idehen",
    "4431850/jakov-kukic",
    "4900671/ajay-mitchell",
    "4397643/jay-nagle",
    "4397104/miles-norris",
    "4900672/david-pickles",
    "4431795/josh-pierre-louis",
    "4397676/ajare-sanni",
    "4900673/max-sheldon",
    "4397644/amadou-sow",
    "4397642/sekou-toure",
    "4397521/calvin-wishart",
]

def change_col_types(df):
    numcols_to_change = df.columns
    for col in numcols_to_change:
        try:
            df[col] = df[col].astype(float)
        except:
            continue
            
df_lst = []
for player in players:
    url = f"https://www.espn.com/mens-college-basketball/player/gamelog/_/id/{player}"
    df = pd.read_html(url)
    stats = pd.DataFrame(df[0])
    stats["Player"] = player[8:]
    stats = stats[:-1]  # drops last row which is an averages row
    df_lst.append(stats)

df = pd.concat(df_lst)
df = df[df["Date"].str.contains("Hercules") == False] #filter out rows that aren't game stats
df = df[df["Date"].str.contains("Skyline") == False]
change_col_types(df)

player_totals = df.groupby("Player").sum() #only season totals for each player

player_totals = player_totals.drop(columns=["FG%", "3P%", "FT%"])
player_totals["rebounds/min"] = player_totals["REB"] / player_totals["MIN"]
player_totals["assists/min"] = player_totals["AST"] / player_totals["MIN"]
player_totals["blocks/min"] = player_totals["BLK"] / player_totals["MIN"]
player_totals["steals/min"] = player_totals["STL"] / player_totals["MIN"]
player_totals["fouls/min"] = player_totals["PF"] / player_totals["MIN"]
player_totals["points/min"] = player_totals["PTS"] / player_totals["MIN"]
player_totals["turnovers/min"] = player_totals["TO"] / player_totals["MIN"]
player_totals["rebounds/min"] = player_totals["rebounds/min"].apply(
    lambda x: round(x, 2)
)
player_totals["assists/min"] = player_totals["assists/min"].apply(lambda x: round(x, 2))
player_totals["steals/min"] = player_totals["steals/min"].apply(lambda x: round(x, 2))
player_totals["fouls/min"] = player_totals["fouls/min"].apply(lambda x: round(x, 2))
player_totals["points/min"] = player_totals["points/min"].apply(lambda x: round(x, 2))
player_totals["turnovers/min"] = player_totals["turnovers/min"].apply(
    lambda x: round(x, 2)
)
player_totals = player_totals.reset_index(level=0)

player_totals = player_totals[
    [
        "Player",
        "PTS",
        "points/min",
        "REB",
        "rebounds/min",
        "AST",
        "assists/min",
        "TO",
        "turnovers/min",
        "PF",
        "fouls/min",
        "BLK",
        "blocks/min",
        "STL",
        "steals/min",       
    ]
]

player_totals.set_index("Player", inplace=True)

st.dataframe(player_totals.style.highlight_max(axis=0), height=1000)
