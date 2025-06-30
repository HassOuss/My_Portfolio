import streamlit as st 
import seaborn as sns 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

st.title("Chicago Traffic Crashes Dashboard")
st.markdown("Analyze patterns in crashes by control devices, lighting, weather, and more.")

# === File Uploader ===
uploaded_file = st.file_uploader("Upload your own Traffic CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Using uploaded file")
else:
    try:
        df = pd.read_csv("Traffic_Crashes.csv")
        st.warning("No file uploaded, using default sample data.")
    except FileNotFoundError:
        st.error("No file uploaded and default sample data not found.")
        st.stop()

# === Shared Analysis Below ===

st.subheader("Raw Data Preview")
st.dataframe(df.head())

# Data Preprocessing
selected_columns = [
    'POSTED_SPEED_LIMIT', 'TRAFFIC_CONTROL_DEVICE', 'DEVICE_CONDITION',
    'WEATHER_CONDITION', 'LIGHTING_CONDITION', 'FIRST_CRASH_TYPE',
    'TRAFFICWAY_TYPE', 'ALIGNMENT', 'ROADWAY_SURFACE_COND', 'ROAD_DEFECT',
    'REPORT_TYPE', 'CRASH_TYPE', 'INTERSECTION_RELATED_I', 'HIT_AND_RUN_I',
    'DAMAGE', 'DATE_POLICE_NOTIFIED', 'PRIM_CONTRIBUTORY_CAUSE',
    'SEC_CONTRIBUTORY_CAUSE', 'STREET_NO', 'STREET_DIRECTION',
    'STREET_NAME', 'BEAT_OF_OCCURRENCE', 'NUM_UNITS', 'MOST_SEVERE_INJURY',
    'INJURIES_TOTAL', 'INJURIES_FATAL', 'INJURIES_INCAPACITATING',
    'INJURIES_NON_INCAPACITATING', 'INJURIES_REPORTED_NOT_EVIDENT',
    'INJURIES_NO_INDICATION', 'INJURIES_UNKNOWN', 'CRASH_HOUR',
    'CRASH_DAY_OF_WEEK', 'CRASH_MONTH', 'LATITUDE', 'LONGITUDE', 'LOCATION']

# Filter to only existing columns
existing_columns = [col for col in selected_columns if col in df.columns]
df = df[existing_columns]

# Optional: show missing columns
missing_columns = [col for col in selected_columns if col not in df.columns]
if missing_columns:
    st.warning(f"Missing columns in uploaded data: {missing_columns}")

# === VISUALIZATIONS ===

st.subheader("Select a Plot to Display")

plot_option = st.selectbox(
    "Choose one:",
    [
        "Traffic Control Devices",
        "Device Condition",
        "Weather Condition",
        "Lighting Condition"
    ]
)

if plot_option == "Traffic Control Devices":
    st.subheader("Traffic Control Devices")
    fig, ax = plt.subplots(figsize=(14, 7))
    df['TRAFFIC_CONTROL_DEVICE'].value_counts().sort_values(ascending=True).plot(kind='barh', color='maroon', ax=ax)
    ax.set_xlabel('Control device counts', fontsize=12)
    ax.set_ylabel('Device', fontsize=12)
    st.pyplot(fig)

elif plot_option == "Device Condition":
    st.subheader("Device Condition")
    fig, ax = plt.subplots(figsize=(14, 7))
    df['DEVICE_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='green', ax=ax)
    ax.set_xlabel('Device condition counts', fontsize=12)
    ax.set_ylabel('Condition', fontsize=12)
    st.pyplot(fig)

elif plot_option == "Weather Condition":
    st.subheader("Weather Condition")
    fig, ax = plt.subplots(figsize=(14, 7))
    df['WEATHER_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='blue', ax=ax)
    ax.set_xlabel('Weather condition counts', fontsize=12)
    ax.set_ylabel('Condition', fontsize=12)
    st.pyplot(fig)

elif plot_option == "Lighting Condition":
    st.subheader("Lighting Condition")
    fig, ax = plt.subplots(figsize=(14, 7))
    df['LIGHTING_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='red', ax=ax)
    ax.set_xlabel('Lighting condition counts', fontsize=12)
    ax.set_ylabel('Condition', fontsize=12)
    st.pyplot(fig)


# LIGHTING CONDITION PIE CHART
st.subheader("Lighting Condition (Pie Chart)")
light = df.groupby('LIGHTING_CONDITION').size().reset_index(name='counts')
fig5, ax5 = plt.subplots()
ax5.pie(light['counts'], labels=None, autopct='%1.1f%%')
ax5.axis('equal')
ax5.set_title('Lighting Condition')
ax5.legend(light['LIGHTING_CONDITION'], title="Lighting Types", loc="center left", bbox_to_anchor=(1, 0.5))
st.pyplot(fig5)

# FIRST CRASH TYPE
st.subheader("First Crash Type")
fig6, ax6 = plt.subplots(figsize=(14, 7))
df['FIRST_CRASH_TYPE'].value_counts().sort_values(ascending=True).plot(kind='barh', color='purple', ax=ax6)
ax6.set_xlabel('First crash counts', fontsize=12)
ax6.set_ylabel('Crash Type', fontsize=12)
st.pyplot(fig6)
