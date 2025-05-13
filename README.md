# CSCI 5410 — Serverless Data Processing  
Dalhousie University · Summer 2024  
Author · Md Samshad Rahman (`@samshad`)

> A bite‑sized journey through **serverless architectures** from AWS Lambda image pipelines and Google Cloud Functions to a full‑stack feedback‑analytics platform orchestrated entirely with managed services.

---

## 🌐 What you’ll find here

| Folder | Theme | Key tech & skills |
|--------|-------|-------------------|
| **Lab/Lab1** | *Image‑processing on AWS Lambda* | Python 3.11 · Boto3 · S3 · DynamoDB<br>Upload, resize & audit images |
| **Lab/Lab2** | *GCP Cloud Functions & Pub/Sub* | Python · Google Cloud Functions · Pub/Sub triggers; serverless sentiment extraction using Google Cloud NLP API |
| **Lab/Lab3** | *Event‑driven data pipeline* | AWS Step Functions · SQS · SNS; orchestrates multi‑stage ETL (code in `Lab/Lab3/`) |
| **Project** | *Serverless feedback & room‑booking platform* | React front‑end + Python Lambda back‑end:<br>• **Backend** – 23 Lambda functions for auth, CRUD, sentiment analysis, chat‑bot helpers, and DynamoDB persistence volume <br>• **Frontend** – Create React App dashboard & forms for admins and users |

> ⭐ **Languages:** ≈ 51 % JavaScript, 31 % Python, 16 % CSS, 2 % HTML  
> 📁 **Repo activity:** 16 commits, labs + capstone milestones

---

## 🧠 Learning outcomes

* **Serverless primitives** – authoring & provisioning Lambda, Cloud Functions, and Step Functions without servers to patch.  
* **Event‑driven design** – S3/Object events, Pub/Sub and API Gateway triggers; fan‑in/out patterns with queues & topics.  
* **Poly‑cloud mindset** – mixed AWS + GCP toolchains; credential isolation and cross‑platform SDK use.  
* **Data processing pipelines** – on‑the‑fly image optimisation, feedback ingestion, sentiment scoring, and dashboard aggregation.  
* **Full‑stack delivery** – React SPA backed by RESTful Lambda APIs & DynamoDB—CI‑friendly and cost‑efficient.  

---

## 🛠 Toolchain

| Domain | Stack |
|--------|-------|
| **Back‑end** | AWS Lambda · API Gateway · DynamoDB · S3 · Step Functions · GCP Cloud Functions · Cloud NLP |
| **Front‑end** | React 18 · Vite/CRA · Tailwind CSS |
| **Infra‑as‑Code** | AWS SAM · CloudFormation & `gcloud` CLI scripts |
| **Auth** | Amazon Cognito |
| **DevOps** | GitHub Actions (lint + deploy), pre‑commit hooks |

---

## 📂 Repository layout

```
.
├── Lab/
│   ├── Lab1/                # Image optimise pipeline (AWS)
│   ├── Lab2/                # GCP Cloud Functions + Pub/Sub
│   └── Lab3/                # Serverless ETL with Step Functions
├── Project/
│   ├── backend/             # Python Lambda functions & utils
│   └── frontend/            # React SPA
└── .gitignore
```

Each sub‑folder ships a mini‑README or docstrings with deployment steps.

---

## 📄 Licence

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.  
© 2025 Md Samshad Rahman
