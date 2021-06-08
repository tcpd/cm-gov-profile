# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import plotly.graph_objects as go
import plotly.express as px

pd.options.plotting.backend = "plotly"

source = "./Governors Data/governors_draft_4.csv"
new_source = "./Governors Data/governors_draft_4.csv"


df = pd.read_csv(source)
df = df.replace(np.nan, "", regex=True)


# print(df)


def correct_duration():
    global df
    for index, row in df.iterrows():
        s = row["appointment_begin"].split("/")

        if row["appointment_end"] == "Current":
            today = date.today()
            e = today.strftime("%d/%m/%Y")
            e = e.split("/")
        else:
            e = row["appointment_end"].split("/")

        s = [int(i) for i in s]
        e = [int(i) for i in e]
        start = datetime(s[2], s[1], s[0])
        end = datetime(e[2], e[1], e[0])

        duration = (end - start).days

        df.at[index, "term_duration"] = duration


# correct_duration()
# print(df)
# df.to_csv(new_source, index=False)


unique_ids = list(df["ID"])

unique_ids = list(np.unique(np.array(unique_ids)))


total_duration = []
names = []
state_comp = []

for i in unique_ids:
    total = 0
    name = ""
    of_state = []
    for index, row in df.iterrows():
        if row["ID"] == i:
            total += row["term_duration"]
            name = row["name"]
            of_state.append(row["state/ut"])
    total_duration.append(total)
    names.append(name)
    state_comp.append(list(np.unique(np.array(of_state))))

# id_and_dur = {unique_ids[i]: total_duration[i] for i in range(len(unique_ids))}
# print(id_and_dur)

for i in range(len(names)):
    names[i] += " ("
    for j in range(len(state_comp[i])):
        st = state_comp[i][j]
        if j != len(state_comp[i]) - 1:
            names[i] += st + ", "
        else:
            names[i] += st + ")"

# print(names)


fig = go.Figure(
    data=go.Scatter(
        x=unique_ids,
        y=total_duration,
        text=names,
        hovertemplate="<b>ID</b>: %{x}<br>"
        + "<b>Total Duration</b>: %{y} days<br>"
        + "<b>Name</b>: %{text}<extra></extra>",
    )
)


def total_duration_gov():
    return fig


# fig = go.Figure(data = go.Scatter(x = names, y = total_duration))
# fig.show()


bar_range_labels = [
    "<=100",
    "101-400",
    "401-800",
    "801-1200",
    "1201-1600",
    "1601-2000",
    "2001-4000",
    "4001-8000",
    ">8000",
]
range_labels = [100, 400, 800, 1200, 1600, 2000, 4000, 8000, 16000]

# bar_ranges = [i for i in range(range_labels)], bar_count = []

bar_count_gov = [0 * i for i in range_labels]

for val in range(len(range_labels)):
    for i in total_duration:
        if i <= range_labels[val]:
            bar_count_gov[val] += 1

for i in range(len(bar_count_gov) - 1, 0, -1):
    if i > 0:
        bar_count_gov[i] -= bar_count_gov[i - 1]

# add = 0
# for i in bar_count_gov:
#    add += i

# print(bar_count_gov)

# print(bar_range_labels, bar_count_gov)


fig = go.Figure(
    data=go.Bar(
        x=bar_range_labels,
        y=bar_count_gov,
        hovertemplate="<b>Range in days</b>: %{x}<br>"
        + "<b>Corresponding no. of Governors</b>: %{y} days<br><extra></extra>",
    )
)


def governors_days():
    return fig
