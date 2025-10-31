import pandas as pd

def compare_states_crop(df, crop_name, state_a, state_b, years):
    f = df[(df['crop']==crop_name) & (df['year'].isin(years))]
    a = f[f['state']==state_a]
    b = f[f['state']==state_b]
    a_prod = a['production'].mean()
    b_prod = b['production'].mean()
    a_rain = a['annual_rain'].mean()
    b_rain = b['annual_rain'].mean()
    return a_prod, b_prod, a_rain, b_rain

def top_crops(df, state, n):
    f = df[df['state']==state]
    r = f.groupby('crop')['production'].sum().sort_values(ascending=False).head(n)
    return r