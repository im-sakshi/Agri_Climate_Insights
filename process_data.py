import pandas as pd

def merge_data(crop_df, rain_df):
    crop_df = crop_df.copy()
    rain_df = rain_df.copy()

    crop_df.columns = crop_df.columns.str.lower()
    rain_df.columns = rain_df.columns.str.lower()

    crop_df['district'] = crop_df['district_name'].str.lower().str.strip()
    crop_df['state'] = crop_df['state_name'].str.lower().str.strip()

    rain_df['district'] = rain_df['district'].str.lower().str.strip()
    rain_df['state'] = rain_df['state/ut'].str.lower().str.strip()

    merged = pd.merge(
        crop_df,
        rain_df,
        on=['state', 'district'],
        how='left'
    )

    return merged