# this program calculates the term_duration and appoinment_delay of each tenure.

import pandas as pd
from dateutil.parser import parse

df = pd.read_csv('governers_draft2.csv')
# storing null indexes
boolean1 = df['appointment_begin'].isnull()
boolean2 = df['appointment_end'].isnull()


for i in range(len(df)):
    # converting strings to date format
    if boolean1[i] == False:
        df['appointment_begin'][i] = df['appointment_begin'][i].strip()
        df['appointment_begin'][i] = pd.to_datetime(
            df['appointment_begin'][i], format='%d/%m/%y')

# correcting century
        if df['appointment_begin'][i].year >= 2021:
            df['appointment_begin'][i] -= pd.DateOffset(years=100)

# converting strings to date (ignoring cells containing -)
    if boolean2[i] == False:
        df['appointment_end'][i] = df['appointment_end'][i].strip()
        df['appointment_end'][i] = pd.to_datetime(
            df['appointment_end'][i], errors='ignore', format='%d/%m/%y')

# correcting century
        if isinstance(df['appointment_end'][i], str) == False and df['appointment_end'][i].year >= 2021:
            df['appointment_end'][i] -= pd.DateOffset(years=100)

# calculating term duration
    if boolean1[i] == False and boolean2[i] == False and isinstance(df['appointment_end'][i], str) == False:
        delta = df['appointment_end'][i]-df['appointment_begin'][i]
        df['term_duration'][i] = delta.days

# converting to date format
    if boolean1[i] == False:
        df['appointment_begin'][i] = df['appointment_begin'][i].strftime(
            '%d/%m/%Y')
    if boolean2[i] == False and isinstance(df['appointment_end'][i], str) == False:
        df['appointment_end'][i] = df['appointment_end'][i].strftime(
            '%d/%m/%Y')

# calculating appointment delay
for i in range(1, len(df)):
    result = (df['state/ut'][i].lower().replace('s/+',
                                                "") == df['state/ut'][i-1].lower().replace('s/+', ""))
    if result == True and boolean2[i-1] == False and boolean1[i] == False:
        a, b = pd.to_datetime(
            df['appointment_begin'][i], format='%d/%m/%Y'), pd.to_datetime(
            df['appointment_end'][i-1], errors='ignore', format='%d/%m/%Y')
        if a.year >= 2021:
            a -= pd.DateOffset(years=100)
        if b.year >= 2021:
            b -= pd.DateOffset(years=100)
        if df['appointment_end'][i-1] != "-":
            delta = a-b
            df['appointment_delay'][i] = delta.days

# change address accordingly
df.to_csv(r'C:\Users\Lenovo\Desktop\governers_draft.csv',
          index=False, header=True)
