import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
st.title('My app')
 
URL = ('https://raw.githubusercontent.com/iantonios/'
       'dsc205/refs/heads/main/tips.csv')
df = pd.read_csv(URL)
 
day = st.radio('Pick a day', ['Thur', 'Fri', 'Sat', 'Sun'])
 
subset = df[df['day'] == day]
st.write(f'{len(subset)} meals served on {day}')
 
fig, ax = plt.subplots()
sns.scatterplot(data=subset, x='total_bill', y='tip', ax=ax)
st.pyplot(fig, clear_figure=True)
 
if st.checkbox('Show the raw rows'):
    st.dataframe(subset)

