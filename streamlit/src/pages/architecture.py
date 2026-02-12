#####   LIBRARY  #####
import streamlit as st
import os


#####   DATA  #####
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # remonte à la racine du projet
APP_architecture = os.path.join(BASE_DIR, "datas", "app_architecture.png")
DAG_schema = os.path.join(BASE_DIR, "datas", "DAG_schema.png")


#####   APP  #####
st.markdown("""

# Architecture
            
This app is primarily built using Airflow, MLflow, and PostgreSQL:

- **Airflow** orchestrates the application workflows.
- **MLflow** is used to store and manage models, as well as to serve them for predictions.
- **PostgreSQL** serves as the main database.

Additional tools:

- **FastAPI** exposes the model through an API endpoint.
- **Streamlit** provides a user-friendly interface for visualizing the database content.

""")

st.image(APP_architecture)

st.markdown("""
**Note**: Free services are prioritized for deployment:

- **Hugging Face**: Hosting MLflow, FastAPI, and Streamlit  
- **NeonDB**: PostgreSQL database with two schemas:  
    - The detector database  
    - MLflow model storage  
- **Docker**: Used for running a local Airflow server  
- **AWS S3 bucket**: Stores model artifacts (used by MLflow)  
- **GitHub**: Code versioning platform  
#
""")

st.markdown("""

# DAGs = Directed Acyclic Graphs 

There are two main DAGs used to run this app:

- **Collect Real Payments from API**:  
  An hourly task triggered by Airflow to fetch a new batch of data from the Jedha API.  
  A data validation step is included to ensure data quality.  

- **Fraud Detection**:  
  Also triggered hourly, this DAG performs batch predictions on the newly collected data stored in the PostgreSQL database.  
  The model (XGBoost) predicts whether a transaction is **fraudulent or not**.  
  Results are saved to the database, and if a fraud is detected, an email notification is sent.  

**Note**: The model was initially trained using a "one-shot training" approach.  
There is no DAG in this app for retraining the model.
""")
      
st.image(DAG_schema)
