import pandas as pd
import numpy as np
from datetime import datetime

source = "../Governors Data/governors_draft_3.csv"
new_source = "../Governors Data/new.csv"

df = pd.read_csv(source)
df = df.replace(np.nan, '', regex=True)


male_titles = ['SHRI', 'SIR', 'SH.']
female_titles = ['SMT', 'SHRIMATI']

state_keywords = {"Rajasthan":"rajas", "Karnataka":"kar.nic.in", "Tamil Nadu":"tn", 
    "Uttar Pradesh":"upgovernor", "West Bengal":"kolkata", "Madhya Pradesh":"mp.gov", 
    "Bihar":"bih", "Uttarakhand":"governoruk", "Meghalaya":"meggovernor", 
    "Andhra Pradesh":"ap.gov", "Arunachal Pradesh":"arunachal", "Puducherry":"py",
    "Jammu & Kashmir":"jkraj","Andaman & Nicobar Islands":"nicobars", "Daman & Diu":"daman", 
    "Dadra & Nagar Haveli":"daman", "Himachal Pradesh":"himachal",
    "Dadra & Nagar Haveli & Daman & Diu":"daman"}

def unique_values(data, column_name):   
    x = list(data[column_name])
    print(np.unique(np.array(x)))

def find_gender_anomalies():
    global df
    df["Gender Flag"] = ""

    for index, row in df.iterrows():
        
        if row["Gender"] == '':
            df.at[index, 'Gender Flag'] = "Flagged: no gender"
            print("No gender found for atleast one case")
            continue
        
        title_gender = ""
        for title in female_titles:
            if title in row["title_begin"]:
                title_gender = "F"
        if title_gender == "":
            for title in male_titles:
                if title in row["title_begin"]:
                    title_gender = "M"

        if (title_gender == "M" and row["Gender"] == "F") or (title_gender == "F" and row["Gender"] == "M"):
            df.at[index,'Gender Flag'] = "Flagged"
            

def find_term_anomalies():
    global df
    df["Term Flag"] = ""
    for index, row in df.iterrows():
        if row["appointment_begin"] == "" or row["appointment_begin"] == "-":
            df.at[index, 'Term Flag'] = "Flagged: no appointment_begin"
            continue
        if row["appointment_end"] == "" or row["appointment_end"] == "-":
            df.at[index, 'Term Flag'] = "Flagged: no appointment_end"
            continue
        if row["term_duration"] == "":
            df.at[index, 'Term Flag'] = "Flagged: no term_duration"
            continue

        s = row["appointment_begin"].split("/")
        e = row["appointment_end"].split("/")
        s=[int(i) for i in s]
        e=[int(i) for i in e]
        start = datetime(s[2], s[1], s[0])
        end = datetime(e[2], e[1], e[0])
        duration = (end - start).days
        if duration != int(row["term_duration"]):
            df.at[index, 'Term Flag'] = "Flagged: incorrect term_duration"
        if duration < 0:
            df.at[index, 'Term Flag'] = "Incorrect dates"

def find_state_anomalies():
    global df
    df["State Flag"] = ""
    for index, row in df.iterrows():
        website = ""
        if row["state/ut"] in state_keywords.keys():
            website = state_keywords[row["state/ut"]]
        else:
            website = row["state/ut"].lower()
        
        if not (website in row["source"]):
            df.at[index, 'State Flag'] = "Flagged: incorrect website"

def fix_date_format():
    global df
    for index, row in df.iterrows():
        try:
            (b_d,b_m,b_y) = tuple(row["appointment_begin"].split('/'))
            if len(b_d) != 2:
                b_d = '0' + b_d
            if len(b_m) != 2:
                b_m = '0' + b_m
            if len(b_y) != 4:
                if int(b_y) <= 20:
                    b_y = '20' + b_y
                else:
                    b_y = '19' + b_y
            df.at[index, 'appointment_begin'] = f"{b_d}/{b_m}/{b_y}"
        except:
            pass
        
        try:
            (e_d,e_m,e_y) = tuple(row["appointment_end"].split('/'))
            if len(e_d) != 2:
                e_d = '0' + e_d
            if len(e_m) != 2:
                e_m = '0' + e_m
            if len(e_y) != 4:
                if int(e_y) <= 20:
                    e_y = '20' + e_y
                else:
                    e_y = '19' + e_y
            df.at[index, 'appointment_end'] = f"{e_d}/{e_m}/{e_y}"
        except:
            pass


# find_gender_anomalies()
# find_term_anomalies()
# find_state_anomalies()
fix_date_format()
print(df)
# df.to_csv(new_source, index=False)