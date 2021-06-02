import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import plotly.graph_objects as go
import plotly.express as px

pd.options.plotting.backend = "plotly"
source = "./Governors Data/governors_draft_4.csv"
df = pd.read_csv(source)
df = df.replace(np.nan, "", regex=True)
# print(df)
states_list = []
for index, row in df.iterrows():
    states_list.append(row["state/ut"])

states_list = list(np.unique(np.array(states_list)))

# print( states_list, len( states_list))


"""For each state find state based term-duration as % for each governor ever appointed to that state"""


def state_terms(state=""):
    try:
        unique_id = []
        for index, row in df.iterrows():
            if row["state/ut"] == state:
                unique_id.append(row["ID"])

        unique_id = list(np.unique(np.array(unique_id)))
        names = []
        total_dur = []

        for i in unique_id:
            name = ""
            total = 0
            for index, row in df.iterrows():
                if row["state/ut"] == state and row["ID"] == i:
                    total += row["term_duration"]
                    name = row["name"]
            names.append(name), total_dur.append(total)

        #print("Graph for State/UT:", state)
        fig = go.Figure(data=[go.Pie(labels=names, values=total_dur)])
        return fig
    except:
        return None


def test():
    return "hey"
