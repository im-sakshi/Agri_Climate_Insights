import requests
import pandas as pd

def load_crop_data(api_url):
    r = requests.get(api_url)
    content = r.content.decode("utf-8")
    df = pd.read_csv(pd.io.common.StringIO(content))
    return df

def load_rainfall_data(path):
    df = pd.read_excel(path, engine="xlrd")
    return df
