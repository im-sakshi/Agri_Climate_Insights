import streamlit as st
import pandas as pd
import altair as alt
import os

from dotenv import load_dotenv
from fetch_data import load_crop_data, load_rainfall_data
from process_data import merge_data
from query_engine import find_top_crops, state_level_correlation

load_dotenv()

api_key = os.getenv("CROP_API_KEY")
resource_id = os.getenv("CROP_RESOURCE_ID")
crop_api = f"https://api.data.gov.in/resource/{resource_id}?api-key={api_key}&format=csv&limit=50000"

rain_path = "data/rainfall.xls"

crop_df = load_crop_data(crop_api)
rain_df = load_rainfall_data(rain_path)
data = merge_data(crop_df, rain_df)

st.title("Agriculture & Climate Insights")

st.write("Explore crop production and climate patterns across states and districts.")

st.subheader("Browse Data")

states = sorted(data["state"].dropna().unique())
selected_state = st.selectbox("State", states)

districts = sorted(data[data["state"] == selected_state]["district"].dropna().unique())
selected_district = st.selectbox("District", districts)

if st.button("View Details"):
    st.subheader(f"{selected_district.title()}, {selected_state.title()}")

    info_crop = data[
        (data["state"] == selected_state) &
        (data["district"] == selected_district)
    ][["crop","area","production","crop_year"]]

    if info_crop.empty:
        st.write("No crop data available.")
    else:
        st.write("### Crop Information")
        st.dataframe(info_crop)

    info_rain = data[
        (data["state"] == selected_state) &
        (data["district"] == selected_district)
    ][["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec","annual"]]

    if info_rain.empty:
        st.write("No rainfall data available.")
    else:
        st.write("### Rainfall Information")
        st.dataframe(info_rain)

        st.write("### Rainfall Trend")
        monthly_cols = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

        melted = info_rain[monthly_cols].melt(
            var_name="month",
            value_name="rainfall"
        )

        order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

        melted["month"] = pd.Categorical(melted["month"], categories=order, ordered=True)

        chart = alt.Chart(melted).mark_line(point=True).encode(
            x=alt.X("month:N", sort=order),
            y="rainfall:Q"
        ).properties(width=700, height=350)

        st.altair_chart(chart)


st.subheader(f"Top Crops in {selected_state.title()}")

count_n = st.number_input("Number of crops", min_value=1, max_value=20, value=5)

if st.button("Show Top Crops"):
    r = find_top_crops(data, selected_state, count_n)
    if r.empty:
        st.write("No crop data found.")
    else:
        st.write(f"### Top {count_n} Crops")
        st.dataframe(r)
        st.write("### Visualization")
        d = r.reset_index()
        c = alt.Chart(d).mark_bar().encode(
            x=alt.X("crop:N", sort="-y"),
            y="production:Q"
        ).properties(width=600, height=400)
        st.altair_chart(c)

st.subheader("Rainfall vs Crop Production (State Level)")

crops_available = sorted(data["crop"].dropna().unique())
selected_crop = st.selectbox("Select Crop", crops_available)

if st.button("Show Correlation Insight"):
    corr = state_level_correlation(data, selected_state, selected_crop)

    if corr is None:
        st.warning("Not enough data to compute correlation.")
    else:
        st.write(f"### Correlation for {selected_crop.title()} in {selected_state.title()}")
        st.write(f"Value: **{corr:.3f}**")

        if corr > 0.4:
            st.success("Production increases with higher rainfall.")
        elif corr < -0.4:
            st.error("Production decreases as rainfall increases.")
        else:
            st.info("Rainfall has weak or no visible impact on this crop.")