import streamlit as st
import plotly.express as px
import pandas as pd

st.header('State unemployment rates (1980-2019)')
df = pd.read_csv('https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/annual_unemployment_state.csv')
df.drop(columns='State', inplace=True)

states = st.multiselect('Select states', df['ST'], ['CT', 'FL', 'MI', 'CA', 'IA'])

df = df.loc[df['ST'].isin(states), :]
df.dropna(inplace=True)

# Transforming the dataset to long format
df = df.reset_index()
dfm = pd.melt(df, id_vars='ST', value_vars=['ST']+[str(x) for x in range(1980, 2019)])
dfm.rename(columns={'variable':'year', 'value':'unemployment'}, inplace=True)

fig = px.bar(dfm,
            x="ST",
            y="unemployment",
            animation_frame="year",
            color="ST",
            range_y=[0,15])

event = st.plotly_chart(fig, key="mpg", on_select="rerun")

st.header('Data source')
st.dataframe(dfm)
