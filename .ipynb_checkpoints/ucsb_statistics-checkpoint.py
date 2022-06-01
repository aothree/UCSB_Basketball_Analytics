import streamlit as st
import pandas as pd
import numpy as np
import requests
pd.options.display.max_columns = 100

st.title("UCSB 2021-2022 season stats")

url = f"https://www.espn.com/mens-college-basketball/team/stats/_/id/2540"
info = pd.read_html(url)
names = pd.DataFrame(info[2])
stats = pd.DataFrame(info[3])
df = pd.concat([names, stats], axis = 1)

df["points/min"] = (df["PTS"] / df["MIN"]).apply(lambda x: round(x, 2))
df["rebounds/min"] = (df["REB"] / df["MIN"]).apply(lambda x: round(x, 2))
df["assists/min"] = (df["AST"] / df["MIN"]).apply(lambda x: round(x, 2))
df["blocks/min"] = (df["BLK"] / df["MIN"]).apply(lambda x: round(x, 2))
df["steals/min"] = (df["STL"] / df["MIN"]).apply(lambda x: round(x, 2))
df["turnovers/min"] = (df["TO"] / df["MIN"]).apply(lambda x: round(x,2))
df['offensive_reb/min'] = (df["OR"] / df["MIN"]).apply(lambda x: round(x, 2))
df['defensive_reb/min'] = (df["DR"] / df["MIN"]).apply(lambda x: round(x, 2))
df['FTA/min'] = (df["FTA"] / df["MIN"]).apply(lambda x: round(x, 2))
df['3PA/min'] = (df["3PA"] / df["MIN"]).apply(lambda x: round(x, 2))

df = df[:-1] # drops last row which is a totals row

st.dataframe(df.style.highlight_max(axis=0), height=1000)

st.table(df)