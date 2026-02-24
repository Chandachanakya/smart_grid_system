# ⚡ Smart Grid Energy Predictor

A time-series forecasting application that predicts energy consumption in a smart grid using **Facebook Prophet** and provides interactive visualization through a **Streamlit dashboard**.

The objective of this project is to improve energy demand forecasting accuracy for better grid stability, peak load management, and operational efficiency.



## 📌 Problem Statement

Energy demand in smart grids fluctuates due to:

- Daily consumption patterns  
- Seasonal variations  
- Long-term trends  
- External influencing factors  

Poor forecasting leads to:

- Energy overproduction or shortages  
- Increased operational costs  
- Reduced grid reliability  
- Inefficient renewable energy integration  

This project builds a forecasting pipeline using Prophet to model trend and seasonality and generate reliable future predictions.


## 🧠 Forecasting Model

### Prophet (by Meta)

Prophet is a time-series forecasting model designed for datasets with strong seasonal patterns and trend components.

### Key Features

- Automatic trend detection  
- Built-in yearly and weekly seasonality  
- Handles missing data  
- Generates uncertainty intervals  
- Robust against outliers  

The model is trained on historical energy consumption data and predicts future demand for a configurable time horizon.



## 🏗️ Tech Stack

**Language**
- Python 3.9+

**Libraries**
- pandas  
- numpy  
- matplotlib  
- seaborn  
- scikit-learn  
- prophet  
- streamlit  



## 📊 Data Format

The dataset must contain the following columns:

| Column | Description |
|--------|------------|
| ds     | Date column (datetime format) |
| y      | Energy consumption value |

Example:

```csv
ds,y
2023-01-01,320.5
2023-01-02,345.8
```



## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Chandachanakya/smart_grid_system.git
cd smart-grid-energy-predictor
```

### 2. Create a Virtual Environment (Recommended)

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```



## ▶️ Running the Project

### Train the Prophet Model

```bash
python src/train_prophet.py
```

This will:
- Load historical data  
- Fit the Prophet model  
- Generate forecast results  



### Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

Open your browser and navigate to:

```
http://localhost:8501
```



## 📈 Dashboard Features

- Upload custom energy dataset  
- Select forecast horizon (30, 60, 90 days, etc.)  
- Visualize:
  - Historical consumption  
  - Forecasted demand  
  - Trend component  
  - Seasonality components  
- View confidence intervals  
- Download forecast results as CSV  



## 📉 Model Evaluation

Performance is measured using:

- Mean Absolute Error (MAE)  
- Root Mean Squared Error (RMSE)  
- R² Score  

These metrics evaluate prediction accuracy on unseen data.



## 🚀 Deployment

To deploy using Streamlit Cloud:

1. Push the repository to GitHub  
2. Connect the repository to Streamlit Cloud  
3. Set `app.py` as the entry point  
4. Deploy  


## 🔮 Future Improvements

- Add weather data as external regressors  
- Compare Prophet with LSTM/GRU models  
- Implement anomaly detection  
- Integrate real-time smart meter APIs  
- Containerize using Docker  



## 📜 License

This project is intended for educational and research purposes.
