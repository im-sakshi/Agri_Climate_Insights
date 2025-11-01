import pandas as pd

def find_top_crops(df, state_name, count_n):
    x = df[df["state"] == state_name]
    r = x.groupby("crop")["production"].sum().sort_values(ascending=False).head(count_n)
    return r

def state_level_correlation(df, state_name, crop_name):
    x = df[df["state"] == state_name]
    x = x[x["crop"] == crop_name]

    if x.empty:
        return None

    yearly_prod = x.groupby("crop_year")["production"].sum().reset_index()
    yearly_rain = x.groupby("crop_year")["annual"].mean().reset_index()

    merged = pd.merge(yearly_prod, yearly_rain, on="crop_year")

    if len(merged) < 3:
        return None

    corr = merged["production"].corr(merged["annual"])
    return float(corr)