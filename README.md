# cm-gov-profile
git repository for profiling cms and governors

# UI (Governors' Dataset)

- [X] Correct anomalies esp those related to gender
- [X] Correct anomalies with respect to Term Duration and related dates (confusion)
- [X] Enter values that are not present esp. wrt. term appointment
- [X] Enter values related to term expiry or end date that are not present

- [X] Make necessary Data Cleaning

- [X] Visualization of governor vs duration of term
- [X] Visualizations for governors across multiple states
- [X] Play around creating more visualizations

- [ ] Cartogram
- [ ] Dash UI
- [ ] Add necessary references and notes

## Phase 2: Making a dashboard

Steps:

pip install -r requirements.txt
streamlit run dashboard/app.py

- [ ] Timeline Visualisations
- [ ] Cartogram
- [ ] Test CM dataset

# Data cleaning

- [X] Merges and splits based on assembly terms in CM dataset
- [ ] Fill in missing dates for CM dataset
- [ ] Merges rows in Gov dataset