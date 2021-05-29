# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import json
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

df = pd.read_csv("./Governors Data/governors_draft_4.csv")


keys = df.groupby(
    ["state/ut"])["Gender"].value_counts(normalize=True).keys().tolist()
values = df.groupby(
    ["state/ut"])["Gender"].value_counts(normalize=True).tolist()
ratio = {"State": [], "Ratio": []}
for ptr in range(len(keys)):
    if keys[ptr][1] == "M":
        ratio["State"].append(keys[ptr][0])
        ratio["Ratio"].append(1 - values[ptr])


states = json.load(open("./Governors Data/states_india.geojson", "r"))
states["features"][1]["properties"]
state = {}
anomalies = {
    "Arunanchal Pradesh": "Arunachal Pradesh",
    "Andaman & Nicobar Island": "Andaman & Nicobar Islands",
    "Dadara & Nagar Havelli": "Dadra & Nagar Haveli",
    "NCT of Delhi": "Delhi",
}
list_states = []
for f in states["features"]:
    f["id"] = f["properties"]["state_code"]
    s = f["properties"]["st_nm"]
    if s in anomalies:
        s = anomalies[s]
    list_states.append(s)
    state[s] = f["id"]
ratio = pd.DataFrame(ratio)
ratio.drop(index=ratio[ratio["State"] == "Ladakh"].index, inplace=True)
ratio.drop(
    index=ratio[ratio["State"] == "Dadra & Nagar Haveli & Daman & Diu"].index,
    inplace=True,
)
# state['Dadra & Nagar Haveli & Daman & Diu']=state['Dadra & Nagar Haveli']
# state['Ladakh']=state['Jammu & Kashmir']
# print(state['Lad'])
ratio["id"] = ratio["State"].apply(lambda x: state[x])
flag = False
# print(ratio.iloc[0]['State'])
# This is to check if all the states match or not
for i in range(len(ratio.index)):
    if ratio.iloc[i]["State"] in list_states:
        continue
    else:
        flag = True
# print(flag)


fig = px.choropleth(ratio, locations="id", geojson="states", color="Ratio")


def gender_data():
    return fig
