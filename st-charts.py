import streamlit as st
import pandas as pd
 
st.title('My app')
 
URL = ('https://raw.githubusercontent.com/iantonios/'
       'dsc205/refs/heads/main/kc_house_mini.csv')
df = pd.read_csv(URL)
 
st.dataframe(df, width=600, height=200)

cols = ['price', 'sqft_living', 'yr_built', 'lat', 'long']
df_short = df.loc[:100, cols]
df_short = df_short.rename(columns={'long': 'lon'})
 
st.subheader('King county (WA) dataset')
st.dataframe(df_short, width=800, height=200)

fig, ax = plt.subplots()

ax.scatter(df_short['sqft_living'], df_short['price']/1000, s=10)
ax.set_xlabel('Living Sq. Ft')
ax.set_ylabel('Price (in $1,000)')
 
st.subheader('Living space vs. price')
st.pyplot(fig=fig, clear_figure=True)
