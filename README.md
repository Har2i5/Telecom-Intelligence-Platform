# 📡 Telecom Reliability & Incident Intelligence Platform

An interactive data and machine learning platform designed to **analyze telecom equipment failures, assess operational risk, and predict incident severity in real time**.

---

## 🚨 Problem Statement

Telecommunication networks experience frequent equipment failures across multiple regions, providers, and device types.

However, organizations often struggle to:

* Identify **where failures are most concentrated**
* Understand **which failures cause the greatest customer impact**
* Prioritize **what to fix first under pressure**
* Predict **how severe a new failure will be at the moment it occurs**

This leads to:

* Slow response times
* Poor resource allocation
* Increased service downtime
* Customer dissatisfaction

---

## 💡 Solution

This platform transforms raw telecom failure logs into **actionable intelligence** by combining:

### 🔍 Data Analytics

* Failure distribution by **country, equipment, and type**
* Customer impact analysis
* Recovery performance insights

### ⚠️ Risk Ranking System

* Ranks **countries or equipment** based on:

  * Failure frequency
  * Customer impact
  * Recovery time
* Helps decision-makers **prioritize interventions**

### 🤖 Machine Learning Prediction

* Predicts **failure severity (Warning → Critical)**
* Works in:

  * Single prediction mode
  * Batch (CSV upload) mode
* Enables **real-time triaging**

---

## 🌍 Live Application

👉 **[Open the App](https://telecom-intelligence-platform-sod8ptpvdoefartnsu7lua.streamlit.app/)**

---

## 🧠 How It Works

### 1. Data Processing

* Feature engineering from:

  * timestamps
  * recovery actions
  * failure descriptions
* Extraction of:

  * root causes
  * operational signals
  * impact metrics

### 2. Machine Learning

* Model: **Random Forest Classifier**
* Pipeline includes:

  * Feature extraction
  * One-hot encoding
* Output:

  * Severity classification
  * Confidence insights

### 3. Visualization

* Built with **Plotly + Streamlit**
* Interactive dashboards:

  * Global failure map
  * Impact analysis
  * Risk ranking

---

## 📊 Key Features

* 🌍 Interactive global failure visualization
* 📊 Equipment & failure type analysis
* 📈 Customer impact distribution insights
* ⚠️ Intelligent risk ranking system
* 🤖 Real-time ML severity prediction
* 📂 Batch prediction via CSV upload

---

## 🛠️ Tech Stack

* **Frontend / App:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly
* **Machine Learning:** Scikit-learn
* **Model Persistence:** Joblib

---

## 📁 Dataset

This project uses the **Telecommunications Equipment Failure Logs** dataset.

### 📌 Description

The dataset contains detailed logs of telecom equipment failures including:

* failure events and timestamps
* equipment and provider identifiers
* failure types and severity
* recovery actions and durations
* customer impact metrics

It enables:

* reliability analysis
* predictive maintenance
* operational benchmarking

---

## 🙏 Data Source & Credit

Dataset provided by **Go Mask**

🔗 Source: *Telecommunications Equipment Failure Logs Dataset*

> This dataset is **not owned by me** and is used strictly for educational and analytical purposes.

---

## ⚠️ Disclaimer

* This project is a **simulation / analytical tool**, not a production telecom system
* Predictions are based on historical patterns and may not reflect real-world outcomes

---

## 🚀 Future Improvements

* Real-time streaming data integration
* Geo-level (lat/long) failure mapping
* Advanced anomaly detection
* Deployment as a full SaaS dashboard

---

## 👤 Author

**Bantar Harris**

---
