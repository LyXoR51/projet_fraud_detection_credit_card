import pandas as pd
import mlflow.sklearn
import mlflow
from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os 

app = FastAPI(title="Automatic Fraud Detection")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

class PredictionFeatures(BaseModel):
    category: str
    gender: str
    city: str
    dob: str
    city_pop: Union[int, float]
    job: str
    amt: Union[int, float]
    last: str
    first: str
    merchant: str
    zip: Union[int, float]

@app.post("/predict")
async def predict(predictionFeatures: PredictionFeatures):
    try:
        df = pd.DataFrame([predictionFeatures.dict()])
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model_name = "Automatic_Fraud_Detector_XGB"
        model_version = "latest"
        model = mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
        prediction = model.predict(df)
        return {"prediction": prediction.tolist()[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model_name = "Automatic_Fraud_Detector_XGB"
        model_version = "latest"
        model = mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
        predictions = model.predict(df)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
