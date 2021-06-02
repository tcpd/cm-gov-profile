import streamlit as st
import numpy as np
import pandas as pd
from dashboard.state_based_terms import state_terms, states_list
from dashboard.total_terms import governors_days, total_duration_gov
from dashboard.gender_data import gender_data
from dashboard.timeline_visualization import timeline_name, timeline_state

# from fuzzywuzzy import fuzz, process

# Str_A = "FuzzyWuzzy is a lifesaver!"
# Str_B = "fuzzy wuzzy is a LIFE SAVER."
# ratio = fuzz.ratio(Str_A.lower(), Str_B.lower())
# st.title(ratio)

st.title("CM Governor Dataset Visualizations")
"Average Days"
st.plotly_chart(governors_days())
"Duration of Governors"
st.plotly_chart(total_duration_gov())
"Gender Data"
st.plotly_chart(gender_data())
"Timeline Visualized by Name"
st.plotly_chart(timeline_name())
"Timeline Visualized by State"
st.plotly_chart(timeline_state())
option = st.selectbox("States", states_list)
"State Based Terms"
st.plotly_chart(state_terms(option))
