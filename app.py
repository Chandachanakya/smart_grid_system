import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go
import requests
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from utils import (
    get_meter_data,
    preprocess_meter_df,
    demand_alert_message,
    send_email_alert,
    highlight_peak
)
# ------------------------------
# Theme and Page Config
# ------------------------------
st.set_page_config(page_title="Smart Grid Energy Forecast", layout="wide", page_icon="⚡")
st.markdown(
    """
    <style>
    /* Custom colors for headings and sections */
    .reportview-container .markdown-text-container {
        color: #222831;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Title and Description
# ------------------------------
st.title("⚡ Smart Grid Energy Demand Forecasting System")
st.markdown("""
### 🎯 Project Overview
This system uses deep learning–based time-series forecasting (Prophet/LSTM-ready) to predict short-term and long-term energy demand. 
It enables grid operators to optimize load balancing and prevent power surges.
""")

st.markdown("<hr style='border-color:#00adb5;'>", unsafe_allow_html=True)
st.subheader("🌈 Interactive Demo Dashboard")
st.write("Forecast electricity demand, visualize results and download your insights for grid planning.")

# ------------------------------
# Sidebar Controls
# ------------------------------
with st.sidebar:
    st.header("📥 Data & Settings")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    st.markdown("---")
    periods_input = st.number_input("Forecast Days Ahead", min_value=1, max_value=365, value=7)
    freq_input = st.selectbox("Forecast Frequency", options=["H", "D"], index=0)
    st.markdown("---")
    st.header("🎨 Visualization")
    actual_color = st.color_picker("Actual Demand Color", "#00adb5")
    pred_color = st.color_picker("Predicted Demand Color", "#fa7c30")
    interval_color = st.color_picker("Interval Fill Color", "#ffd369")
    st.markdown("---")

    st.header("⚡ Efficiency")
    show_peaks = st.checkbox("Highlight Peak Demand", value=True)
    show_stats = st.checkbox("Show Stats Cards", value=True)

# ------------------------------
# Data Handling
# ------------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("🔎 No file uploaded. Using sample data!")
    df = pd.read_csv("energy_demand.csv") 
print(df.columns)
print(df.head())
df.rename(columns={"datetime": "ds", "demand": "y"}, inplace=True)
df['ds'] = pd.to_datetime(df['ds'])

# ------------------------------
# Model & Forecast
# ------------------------------
if st.button("🧮 Run Forecast"):
    with st.spinner("Training Prophet model..."):
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=periods_input * (24 if freq_input == "H" else 1), freq=freq_input)
        forecast = model.predict(future)
#Evalutation
    merged = pd.merge(df, forecast[['ds', 'yhat']], on='ds', how='inner')
    mae = mean_absolute_error(merged['y'], merged['yhat'])
    rmse = np.sqrt(mean_squared_error(merged['y'], merged['yhat']))
    mape = np.mean(np.abs((merged['y'] - merged['yhat']) / merged['y'])) * 100

    st.markdown("### 📏 Forecast Accuracy")
    st.write(f"**MAE:** {mae:.2f}, **RMSE:** {rmse:.2f}, **MAPE:** {mape:.2f}%")
    
        # Phase 4: Demand Alert Section
        # ------------------------------
    st.subheader("⚠️ Demand Alert System")
    latest_value = df['y'].iloc[-1]
    threshold = df['y'].mean() * 1.2   # 20% above average as warning limit

    # Get alert message and display it
    alert_msg, status = demand_alert_message(latest_value, threshold)

    if status == "warning":
        st.error(alert_msg)
    else:
        st.success(alert_msg)
    
    # ------------------------------
    # Stats Card
    # ------------------------------
    if show_stats:
        peak_row = df.loc[df['y'].idxmax()]
        min_row = df.loc[df['y'].idxmin()]
        avg_value = df['y'].mean()
        col1, col2, col3 = st.columns(3)
        col1.metric(label="🚀 Peak Demand", value=f"{peak_row.y:.0f}", delta=f"{peak_row.ds.strftime('%d %b %Y %H:%M')}")
        col2.metric(label="🌱 Min Demand", value=f"{min_row.y:.0f}", delta=f"{min_row.ds.strftime('%d %b %Y %H:%M')}")
        col3.metric(label="📊 Avg Demand", value=f"{avg_value:.0f}")

    # ------------------------------
    # Enhanced Plotly Visualization
    # ------------------------------
    fig = go.Figure()

    # Actual
    fig.add_trace(go.Scatter(
        x=df['ds'], y=df['y'], mode='lines+markers', name='Actual',
        line=dict(color=actual_color, width=2), marker=dict(size=5)
    ))

    # Predicted
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast',
        line=dict(color=pred_color, width=3)
    ))

    # Confidence Interval
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', line=dict(width=0), showlegend=False)
    )
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', fill='tonexty', fillcolor=interval_color,
        line=dict(width=0), name='Confidence Interval', showlegend=True
    ))

    # Peak Demand Marker
    if show_peaks:
        peak_idx = forecast['yhat'].idxmax()
        fig.add_trace(go.Scatter(
            x=[forecast['ds'][peak_idx]], y=[forecast['yhat'][peak_idx]],
            mode='markers+text', marker=dict(size=12, color='red'),
            text=["Peak"], textposition="top center", name="Peak Predicted"
        ))

    fig.update_layout(
        title="🔮 Smart Grid Energy Demand Forecast",
        xaxis_title="Date & Time",
        yaxis_title="Demand (MW)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------
    # Data Table (Optional)
    # ------------------------------
    st.subheader("🔢 Forecasted Demand Table")
    forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast_display['Peak'] = forecast_display['yhat'] == forecast_display['yhat'].max()
    def highlight_peak(row):
        return ['background-color: #eb4d4b' if row.Peak else '' for _ in row]
    st.dataframe(forecast_display.style.apply(highlight_peak, axis=1))

    # ------------------------------
    # Download Button
    # ------------------------------
    st.success("👍 Forecast complete! Download results below.")
    csv = forecast_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Prediction",
        data=csv,
        file_name="energy_forecast.csv",
        mime="text/csv"
    )
else:
    st.info("⏳ Adjust sidebar settings and click 'Run Forecast' for predictions. Screenshots and charts will appear here.")

# Footer
st.markdown("---")
st.caption("Data Science Student Project")

