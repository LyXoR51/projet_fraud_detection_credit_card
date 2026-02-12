#####   LIBRARY  #####
from sqlalchemy import create_engine, text
import plotly.express as px
import streamlit as st
from datetime import datetime
import pandas as pd
import requests
import random
import json
import os



#####   DATA & VARIABLE #####
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
ENGINE = create_engine(POSTGRES_DATABASE, echo=True)
TABLE_NAME = 'fraud_detector'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # remonte à la racine du projet
FRAUD_DATASET = pd.read_csv(os.path.join(BASE_DIR, "datas", "full_fraud_dataset_detected_by_model.csv"), index_col=0)
LEGIT_DATASET = pd.read_csv(os.path.join(BASE_DIR, "datas", "fraudTest_sample.csv"), index_col=0)
FASTAPI_URL = os.getenv("FASTAPI_URL")

#####   APP  #####
def display_data(df):
    df['current_time'] = pd.to_datetime(df['current_time'], unit='ms')
    df_fraud = df[df['is_fraud']==1]

    if len(df_fraud != 0):
        st.subheader(f" ⚠️ Alert - Fraudulent transaction detected :  {len(df_fraud)} ->  {round(df_fraud['amt'].sum(),2)}$ ")
        st.dataframe(df[df['is_fraud']==1])
    else:
        st.subheader("✅ No fraudulent transaction detected !")

    st.subheader(f"✅ Legitimate transaction: {len(df[df['is_fraud']==0])} ")
    st.dataframe(df[df['is_fraud']==0])


def generate_transaction(data):
    # current datetime
    now = datetime.now()
    ts = int(datetime.timestamp(now) * 1000)

    # collect trans_num in DB
    with ENGINE.connect() as conn:
        stmt = text(f"""
            SELECT trans_num FROM {TABLE_NAME} 
        """)
        result = conn.execute(stmt)

    trans_num_in_db = pd.DataFrame(result.fetchall(), columns=result.keys())

    # preprocess
    existing_trans_nums = trans_num_in_db['trans_num'].tolist()
    df = data[~data['trans_num'].isin(existing_trans_nums)]
    df = df.sample(1)

    df.drop(columns=['is_fraud','trans_date_trans_time','unix_time'], inplace=True)

    json_payload = df.to_dict(orient="records")[0]

    response = requests.post(FASTAPI_URL, json = json_payload)

    data = response.json()
    df['is_fraud'] = data['prediction']
    df['current_time'] = ts

    # push data to neon
    df.to_sql(TABLE_NAME, con=ENGINE, if_exists='append', index=False)


st.markdown("**Tip:** The realtime API isn’t available yet — use this button to generate a new transaction. It may be legit or fraudulent, depending on the model. The first run might take longer as the model warms up..")
with st.spinner("Processing..."):
    if st.button("Generate a new transaction"):
        if random.randint(1, 3) ==1:
            data = FRAUD_DATASET
        else:
            data = LEGIT_DATASET
        generate_transaction(data)





tab1, tab2, tab3 = st.tabs([" 📅 Today", " 🗓️ Yesterday", " 🗄️ Global"])
with tab1:
    with ENGINE.connect() as conn:
        stmt = text(f"""
            SELECT * 
            FROM {TABLE_NAME} 
            WHERE to_timestamp(("current_time")::bigint / 1000)::date = CURRENT_DATE;
        """)
        result = conn.execute(stmt)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    display_data(df)

with tab2:
    with ENGINE.connect() as conn:
        stmt = text(f"""
            SELECT * 
            FROM {TABLE_NAME} 
            WHERE to_timestamp(("current_time")::bigint / 1000)::date = CURRENT_DATE -1 ;
        """)
        result = conn.execute(stmt)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    display_data(df)


with tab3:
    with ENGINE.connect() as conn:
        stmt = text(f"""
            SELECT * 
            FROM {TABLE_NAME};
        """)
        result = conn.execute(stmt)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    display_data(df)
