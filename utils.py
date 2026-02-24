# utils.py

import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
# ========== Data Fetching Helpers ==========

def get_meter_data(api_url):
    """Fetch live data from smart meter via HTTP API endpoint."""
    try:
        r = requests.get(api_url, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Expecting dict/list; adapt parsing as per API's structure
        df = pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error fetching meter data: {e}")
        return pd.DataFrame()

# ========== Preprocessing Helpers ==========

def preprocess_meter_df(df, datetime_col="datetime", demand_col="demand"):
    """
    Make dataframe compatible with Prophet:
    - Rename columns to 'ds' (datetime) and 'y' (value)
    - Parse datetime and sort
    """
    df = df.rename(columns={datetime_col: 'ds', demand_col: 'y'}).copy()
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values("ds")
    return df

# ========== Alert Functions ==========

def demand_alert_message(latest_value, threshold):
    """
    Return alert message and status based on demand vs. threshold.
    """
    if latest_value > threshold:
        return (f"⚠️ Demand surge detected: {latest_value} MW", "warning")
    else:
        return (f"✅ Demand is within normal limits ({latest_value} MW).", "success")
# ========== Notification (External) ==========

def send_email_alert(demand_value, sender_email, password, recipient_email):
    """Send a basic email alert."""
    msg = MIMEText(f"Alert: Demand surged to {demand_value} MW.")
    msg['Subject'] = 'Smart Meter Alert'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

# ========== Visualization Helper (Optional) ==========

def highlight_peak(row):
    """
    Style function for use with Pandas dataframes in Streamlit to highlight peak demand row.
    """
    return ['background-color: #eb4d4b' if row['Peak'] else '' for _ in row]

