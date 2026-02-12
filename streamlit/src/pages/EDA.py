#####   LIBRARY  #####
import streamlit as st
import pandas as pd
import plotly.express as px
import os


#####   DATA  #####
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # remonte à la racine du projet
DATA_ANALYSIS_URL = os.path.join(BASE_DIR, "datas", "get_around_delay_analysis.xlsx")
Fraud_repartition = pd.read_csv(os.path.join(BASE_DIR, "datas", "Fraud_repartition.csv"))
Amount_repartition = pd.read_csv(os.path.join(BASE_DIR, "datas", "Amount_repartition.csv"))
Fraud_amount = pd.read_csv(os.path.join(BASE_DIR, "datas", "Fraud_Amount.csv"))
Fraud_credit_card = pd.read_csv(os.path.join(BASE_DIR, "datas", "Fraud_credit_card.csv"))


#####   APP  #####
st.markdown(f"""

# EDA = Exploratory Data Analysis
            
In this page, we will explore the [training dataset from Kaggle](https://www.kaggle.com/datasets/kartik2112/fraud-detection/data) !
#
""")


container = st.container()
col1, col2 = container.columns(2)
with col1:

    st.subheader("Fraud repartition", divider=True)
    graph = px.pie(Fraud_repartition, values='count', names=["Legit","Fraud"])
    st.plotly_chart(graph, use_container_width=True)

with col2:
    st.subheader("Amount repartition", divider=True)
    graph = px.pie(Amount_repartition, values='amt', names=["Legit","Fraud"])
    st.plotly_chart(graph, use_container_width=True)
            
st.markdown(f"""
As we can see, "only" 0.4% of fraud. But the total amount of fraudulent transaction is near 3 % !
#
""")

st.subheader("Fraud amount distribution", divider=True)

graph = px.histogram(Fraud_amount,x='amt')
st.plotly_chart(graph, use_container_width=True)

st.markdown(f"""
#
""")


st.subheader("Fraudulent Credit card analysis", divider=True)

Fraud_credit_card_group = pd.DataFrame(Fraud_credit_card.groupby('cc_num')['cc_num'].value_counts())
graph = px.histogram(Fraud_credit_card_group)
st.plotly_chart(graph, use_container_width=True)
st.markdown(f"""
Fraudulent transaction are not a mistackes, the mean is 12 frauds by credit cards !
""")


st.subheader("Heat map of fraudulent transactions", divider=True)
df = pd.read_csv(os.path.join(BASE_DIR, "datas", "Fraud_city.csv"))
df = df.rename(columns={'merch_lat': 'lat', 'merch_long': 'lon'})
st.map(df)