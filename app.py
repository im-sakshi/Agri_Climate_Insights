import streamlit as st
import pandas as pd
from fetch_data import load_crop_data, load_rainfall_data
from process_data import merge_data

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CROP_API_KEY")
RESOURCE_ID = os.getenv("CROP_RESOURCE_ID")

crop_api = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=csv&limit=50000"

rain_path = "data/rainfall.xls"

crop_df = load_crop_data(crop_api)
rain_df = load_rainfall_data(rain_path)
data = merge_data(crop_df, rain_df)

st.title("Agriculture & Climate Insights")

st.write(
    "This simple tool lets you explore crop production and rainfall patterns "
    "for different states and districts using publicly available datasets."
)


st.subheader("Browse Data")

states = sorted(data['state'].dropna().unique())
selected_state = st.selectbox("State", states)

districts = sorted(
    data[data['state'] == selected_state]['district'].dropna().unique()
)
selected_district = st.selectbox("District", districts)


if st.button("View Details"):
    st.subheader(f"Details for {selected_district.title()}, {selected_state.title()}")

  
    crop_info = data[
        (data['state'] == selected_state) &
        (data['district'] == selected_district)
    ][['crop', 'area', 'production', 'crop_year']]

    if crop_info.empty:
        st.write("No crop data available for this location.")
    else:
        st.write("### Crop Information")
        st.dataframe(crop_info)

    
    rain_info = data[
        (data['state'] == selected_state) &
        (data['district'] == selected_district)
    ][['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','annual']]

    if rain_info.empty:
        st.write("No rainfall data found for this location.")
    else:
        st.write("### Rainfall Information")
        st.dataframe(rain_info)



st.subheader(f"Top Crops in {selected_state.title()}")

n_value = st.number_input("Number of crops", min_value=1, max_value=20, value=5)

if st.button("Show Top Crops"):
    state_crop = data[data['state'] == selected_state]

    if state_crop.empty:
        st.write("No crop data found.")
    else:
        top_crops = (
            state_crop.groupby('crop')['production']
            .sum()
            .sort_values(ascending=False)
            .head(n_value)
        )
        st.write(f"### Top {n_value} crops:")
        st.dataframe(top_crops)