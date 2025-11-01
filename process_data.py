import pandas as pd

def merge_data(crop_df, rain_df):
    c = crop_df.copy()
    r = rain_df.copy()

    c.columns = c.columns.str.lower()
    r.columns = r.columns.str.lower()

    c['district'] = c['district_name'].str.lower().str.strip()
    c['state'] = c['state_name'].str.lower().str.strip()

    r['district'] = r['district'].str.lower().str.strip()
    r['state'] = r['state/ut'].str.lower().str.strip()

    rain_cols = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

    rainfall_long = r.melt(
        id_vars=["state","district"],
        value_vars=rain_cols,
        var_name="month",
        value_name="rainfall"
    )

    rainfall_long["month"] = pd.Categorical(rainfall_long["month"], categories=order, ordered=True)

    merged = pd.merge(c, r, on=["state","district"], how="left")

    return merged