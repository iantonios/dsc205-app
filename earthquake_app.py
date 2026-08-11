"""
USGS Earthquake Explorer
------------------------
A simple Streamlit app that visualizes earthquakes (M2.5+, past 30 days)
from the US Geological Survey real-time CSV feed.

Run with:  streamlit run earthquake_app.py
"""

import folium
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_folium import st_folium

DATA_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv"

st.set_page_config(page_title="USGS Earthquake Explorer", layout="wide")


# ----------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------
@st.cache_data(ttl=3600)  # refresh hourly; the feed is live
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    # 'time' looks like 2026-08-11T14:23:45.120Z -> split date from time
    df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=True)
    df["date"] = df["time"].dt.date
    return df.dropna(subset=["latitude", "longitude", "mag"])


st.title("🌍 USGS Earthquake Explorer")
st.caption("Magnitude 2.5+ earthquakes worldwide, past 30 days — source: USGS")

with st.spinner("Fetching data from USGS..."):
    df = load_data(DATA_URL)

st.write(f"**{len(df):,}** earthquakes loaded, "
         f"from {df['date'].min()} to {df['date'].max()}.")


# ----------------------------------------------------------------------
# 1. Checkbox: show date / magnitude / location table
# ----------------------------------------------------------------------
if st.checkbox("Show earthquake data (date, magnitude, location)"):
    table = (df[["date", "mag", "place"]]
             .rename(columns={"mag": "magnitude", "place": "location"})
             .sort_values("date", ascending=False)
             .reset_index(drop=True))
    st.dataframe(table, use_container_width=True, height=350)


# ----------------------------------------------------------------------
# 2. Seaborn distribution of magnitudes (entire dataset)
# ----------------------------------------------------------------------
st.subheader("Distribution of earthquake magnitudes")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(data=df, x="mag", bins=30, kde=True, color="#c0392b", ax=ax)
ax.set_xlabel("Magnitude")
ax.set_ylabel("Number of earthquakes")
ax.set_title("Magnitude distribution — all recorded events")
st.pyplot(fig)

col1, col2, col3 = st.columns(3)
col1.metric("Mean magnitude", f"{df['mag'].mean():.2f}")
col2.metric("Median magnitude", f"{df['mag'].median():.2f}")
col3.metric("Max magnitude", f"{df['mag'].max():.2f}")


# ----------------------------------------------------------------------
# 3. Form + folium map
# ----------------------------------------------------------------------
st.subheader("Map earthquakes by magnitude")

mag_min, mag_max = float(df["mag"].min()), float(df["mag"].max())

with st.form("magnitude_form"):
    selected_mag = st.slider(
        "Select minimum magnitude of interest",
        min_value=round(mag_min, 1),
        max_value=round(mag_max, 1),
        value=round(mag_min + (mag_max - mag_min) / 2, 1),
        step=0.1,
    )
    submitted = st.form_submit_button("Show map")

# Persist the choice so the map survives st_folium's reruns
if submitted:
    st.session_state["mag_threshold"] = selected_mag

if "mag_threshold" in st.session_state:
    threshold = st.session_state["mag_threshold"]
    subset = df[df["mag"] >= threshold]

    st.write(f"Showing **{len(subset):,}** earthquakes with magnitude ≥ {threshold}")

    if subset.empty:
        st.warning("No earthquakes match that magnitude. Try a lower value.")
    else:
        quake_map = folium.Map(
            location=[subset["latitude"].mean(), subset["longitude"].mean()],
            zoom_start=2,
            tiles="CartoDB positron",
        )

        for _, row in subset.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=max(3, row["mag"] * 1.5),
                color="crimson",
                fill=True,
                fill_opacity=0.5,
                popup=folium.Popup(
                    f"<b>M {row['mag']}</b><br>{row['place']}<br>{row['date']}",
                    max_width=250,
                ),
                tooltip=f"M {row['mag']}",
            ).add_to(quake_map)

        st_folium(quake_map, width=1000, height=550, returned_objects=[])
else:
    st.info("Pick a magnitude above and click **Show map**.")
