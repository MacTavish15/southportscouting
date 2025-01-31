import streamlit as st
#import openpyxl
import pandas as pd
from scipy.spatial import distance

#inputExcelFile ="Striker 2425 26th Jan 2025 400 mins min 2.xlsx"
#newWorkbook = openpyxl.load_workbook(inputExcelFile)
#sheetNames=newWorkbook.sheetnames

#xls = pd.ExcelFile(inputExcelFile)
#datas = []
#for name in sheetNames:
    #df = pd.read_excel(xls, name)
    #df['League'] = name
#    datas.append(df)

#data  = pd.concat(datas).reset_index()

#data.to_csv("results.csv",index=False)
data = pd.read_csv("results.csv",encoding="utf8")
st.sidebar.header("Southport F.C. Scouting")
add_selectbox_league = st.sidebar.selectbox(
    "League",
    data['League'].unique()
)

age = st.sidebar.number_input("Age Under value :")
select_attributs = st.sidebar.multiselect('Select Attributs',data.columns, [])

if st.sidebar.button("Show table", type="primary"):
    small_data = data[data.Age<age]
    small_data = small_data[small_data.League == add_selectbox_league][select_attributs]
    treated_data = small_data.copy()
    i = 0
    cols_cat=["index","Player","Team","Team within selected timeframe","Position",
                "Age", "TM Total Score","DLF Total Score","ST Total Score","All Round TOTAL","Market value","Contract expires","Matches played","Minutes played","Birth country","Passport country","Foot",
                "Height","Weight","On loan","League","Unnamed: 5","Unnamed: 6","Unnamed: 7","Unnamed: 8","Unnamed: 51"]
    for col in select_attributs:
        if col in cols_cat:
            pass
        else:
            treated_data[col] = treated_data[col] / treated_data[col].max()
            i = i + 1
    treated_data["Score"] = 0
    for col in select_attributs:
        if col in cols_cat:
            pass
        else:
            treated_data["Score"] = treated_data["Score"] + treated_data[col]
    treated_data["Score"] = treated_data["Score"] / i
    st.header("Table:")
    small_data["Score"] = treated_data["Score"] * 10
    small_data = small_data.sort_values("Score",ascending=False)
    st.table(small_data)

st.sidebar.header("Search based on Player")
add_selectbox_player = st.sidebar.selectbox(
    "Similair Players to ",
    data['Player'].unique()
)
if st.sidebar.button("Search", type="primary"):
    small_data = data[data.Age<age]
    small_data = small_data[small_data.League == add_selectbox_league][select_attributs]
    treated_data = small_data.copy()

    i = 0
    cols_cat=["index","Player","Team","Team within selected timeframe","Position",
                "Age", "TM Total Score","DLF Total Score","ST Total Score","All Round TOTAL","Market value","Contract expires","Matches played","Minutes played","Birth country","Passport country","Foot",
                "Height","Weight","On loan","League","Unnamed: 5","Unnamed: 6","Unnamed: 7","Unnamed: 8","Unnamed: 51"]
    cols_num=[]
    for col in select_attributs:
        if col in cols_cat:
            pass
        else:
            cols_num.append(col)
    for col in select_attributs:
        if col in cols_cat:
            pass
        else:
            treated_data[col] = treated_data[col] / treated_data[col].max()
            i = i + 1
    player_name = add_selectbox_player
    data_player = data[data.Player == player_name][cols_num]
    treated_data["Score"] = 0
    for col in select_attributs:
        if col in cols_cat:
            pass
        else:
            treated_data["Score"] = treated_data["Score"] + treated_data[col]
    treated_data["Score"] = treated_data["Score"] / i
    st.header("Table:")
    small_data["Score"] = treated_data["Score"] * 10
    small_data = small_data.sort_values("Score",ascending=False)
    small_data['Similarity']=0
    for i in range(len(small_data)):
        small_data.at[i,'Similarity'] = distance.euclidean(data_player.iloc[0], small_data.iloc[i][cols_num])
    small_data = small_data.sort_values("Similarity",ascending=True).dropna()
    st.table(small_data)
