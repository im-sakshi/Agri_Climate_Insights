🌾 Agriculture & Climate Insights — Prototype

A simple, functional prototype that connects agricultural crop production data with climatic rainfall patterns for Indian states & districts using publicly available datasets from data.gov.in.

This project was created as part of the Bharat Digital Challenge — Project Samarth.

✅ Features

✔ State → District selection
✔ Crop production data viewer
✔ Rainfall pattern viewer
✔ Top N crops in a selected state
✔ Combined integrated dataset (crop + rainfall)
✔ Data sourced from live API + IMD rainfall dataset

✅ Dataset Sources
1. Crop Production Dataset (Live API, data.gov.in)

Resource ID: stored securely via .env

API Format: CSV

Fields used: State, District, Crop, Year, Area, Production

2. Rainfall Normals (IMD)

File: data/rainfall.xls

Columns include: JAN–DEC, ANNUAL, MAM, JJAS, OND

✅ Project Structure
project/
│
├── app.py
├── fetch_data.py
├── process_data.py
├── query_engine.py
├── requirements.txt
├── .env
├── .gitignore
└── data/
     └── rainfall.xls

✅ Installation & Setup
1. Create virtual environment
python -m venv .venv

2. Activate it

Windows:

.venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Add .env file

Create .env:

CROP_API_KEY=YOUR_API_KEY_HERE
CROP_RESOURCE_ID=YOUR_RESOURCE_ID_HERE

✅ Running the App
streamlit run app.py


Then open:
👉 http://localhost:8501/

✅ How It Works

Fetches crop data dynamically from data.gov.in using the API

Reads rainfall data from IMD XLS file

Cleans & normalizes state/district names

Merges climate + agriculture data

Lets user explore:

District rainfall data

Crop production trends

Top N state crops

✅ Limitations

IMD rainfall data is historical normals (1951–2000)

Crop dataset production values vary by availability on data.gov.in

Prototype focuses on merging datasets, not NLP Q&A