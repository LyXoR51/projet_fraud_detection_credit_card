import streamlit as st
st.set_page_config(layout="wide")

#from utils.common import load_data_analysis

# Load data
#data = load_data_analysis()

pages = [
    st.Page("pages/home.py", title="Home", icon="ℹ️"),
    st.Page("pages/EDA.py", title="EDA", icon="📈"),
    st.Page("pages/architecture.py", title="Architecture", icon="🏗️"),
    st.Page("pages/database.py", title="Detector", icon="💻"),
]

pg = st.navigation(pages)
pg.run()