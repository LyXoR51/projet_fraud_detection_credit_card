# Fraud Detection API

Real-time fraud detection project with production-grade automated deployment via GitHub Actions.

## 🎯 Business Value

Detect fraudulent transactions in real-time through a robust **FastAPI** API and visualize results via an intuitive **Streamlit** dashboard.

**Context**: Credit card fraud costs EU financial institutions over €1 billion annually. This project delivers precise, scalable predictive detection.

## 🚀 Live Services

| Service | Description | URL |
|---------|-------------|-----|
| **Streamlit Dashboard** | Transactions visualization, EDA, architecture | [huggingface.co/spaces/lyx51/Fraud_detection](https://lyx51-fraud-detection-streamlit.hf.space) |
| **FastAPI API** | Real-time fraud predictions (XGBoost) | [lyx51-Fastapi-fraud-detector.hf.space/docs](https://lyx51-fraud-detection-fastapi.hf.space/docs#/) |
| **Demo Video** | Complete walkthrough | [Vidyard](https://share.vidyard.com/watch/2mLvhKeqyFrzDuSSDJt42s) |

## 🏗️ Production Architecture

```
Mono-repo GitHub (automated deployment)
├── FastAPI/           → Auto-sync HF FastAPI Space
├── streamlit/         → Auto-sync HF Streamlit Space
└── .github/workflows/ → Dedicated workflows per service

**Model Training & Storage**:
MLflow server → XGBoost model trained & stored
PostgreSQL NeonDB + AWS S3 artifacts
```

**Tech Stack**:
```
FastAPI + XGBoost + MLflow + PostgreSQL (NeonDB) + AWS S3
+ Hugging Face Spaces + GitHub Actions (automatic HF sync)
```


## 🔄 Automated MLOps Deployment

**Single GitHub repo** with service-specific workflows:

```yaml
# .github/workflows/fastapi-sync-hf.yml
name: FastAPI - Sync to Hugging Face
on:
  push:
    paths:
      - 'FastAPI/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Push to Hugging Face
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          mkdir tmp
          cp -r FastAPI/* tmp/
          cd tmp

          git init
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"

          git add .
          git commit -m "Deploy to Hugging Face"

          git branch -m master main

          git remote add hf "https://lyx51:${HF_TOKEN}@huggingface.co/spaces/lyx51/Fraud-detection-FastAPI"
          git fetch hf
          git push hf main:main --force
```

**Key Benefits**:
- ✅ Single source of truth
- ✅ Automatic HF sync on every push
- ✅ Zero-touch deployment
- ✅ Production-scalable

## 🚀 Local Quickstart

```bash
git clone https://github.com/LyXoR51/projet_fraud_detection_credit_card.git
cd FastAPI && docker build -t fraud-api .
cd ../streamlit && docker build -t fraud-dashboard .
```

## 📈 Production Metrics

- **Model**: XGBoost trained/stored on MLflow server
- **Database**: PostgreSQL NeonDB (detector + metadata schemas)
- **Storage**: AWS S3 model artifacts
- **Scalability**: Industrial-ready


## 📱 Future Roadmap

**Living project** - Ready for extension:
- Airflow orchestration
- Email notifications
- Model retraining pipelines
- Advanced monitoring

## 👤 Author

**Lyx51** - Data/ML Engineer → AI Project Manager  