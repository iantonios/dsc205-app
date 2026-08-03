import streamlit as st
import pandas as pd
 
st.title('My app')
 
URL = ('https://raw.githubusercontent.com/iantonios/'
       'dsc205/refs/heads/main/tips.csv')
df = pd.read_csv(URL)
 
st.dataframe(df, width=600, height=200)
