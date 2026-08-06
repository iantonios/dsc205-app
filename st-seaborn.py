import seaborn as sns
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
 
URL = ('https://raw.githubusercontent.com/iantonios/'
       'dsc205/refs/heads/main/tips.csv')
df = pd.read_csv(URL)
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='total_bill', y='tip',hue='time', ax=ax)
ax.set_title('Tips by bill size')
st.pyplot(fig, clear_figure=True)
