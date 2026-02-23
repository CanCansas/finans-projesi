# 💸 Personal Finance Tracker & Econometric Forecasting Dashboard

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)

A full-stack financial data science application that not only tracks personal income and expenses but also utilizes time series analysis to forecast future expenditure trends. 

## 📌 Project Overview
This project is designed to demonstrate an end-to-end data pipeline: from relational database modeling and RESTful API development to interactive data visualization and econometric forecasting. It bridges the gap between software engineering and data science.



## 🚀 Key Features
* **Robust Backend API:** Built with **FastAPI** to handle CRUD operations for transactions and categories efficiently.
* **Relational Database Management:** Utilizes **SQLAlchemy** (ORM) with **SQLite** for structured, safe, and easily queryable data storage.
* **Econometric Time Series Forecasting:** Implements **Exponential Smoothing** ($\alpha = 0.5$) via **Pandas** to analyze past expenditure shocks and calculate weighted future spending trends.
* **Interactive Dashboard:** A modern, responsive web interface built with **Streamlit** and **Plotly** to visualize KPIs, expense distributions, and forecasting models.

## 🛠️ Technology Stack
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Database:** SQLite, SQLAlchemy
* **Data Processing & Analysis:** Pandas, Numpy
* **Frontend & Visualization:** Streamlit, Plotly Express

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/finance-tracker.git](https://github.com/yourusername/finance-tracker.git)
   cd finance-tracker