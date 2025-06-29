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
    df = pd.read_csv("Traffic_Crashes.csv")
    st.warning("No file uploaded, using default sample data")


    # Preview Data
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
       'CRASH_DAY_OF_WEEK', 'CRASH_MONTH', 'LATITUDE', 'LONGITUDE',
       'LOCATION'
    ]
####
# Only keep columns that actually exist
existing_columns = [col for col in selected_columns if col in df.columns]
#df = df[selected_columns]

df = df[selected_columns].copy()
# Optional: show missing columns as a warning
missing_columns = [col for col in selected_columns if col not in df.columns]
  if missing_columns:
  st.warning(f"Missing columns in uploaded data: {missing_columns}")
    

    # === TRAFFIC CONTROL DEVICE PLOT ===
    st.subheader("Traffic Control Devices")
    fig1, ax1 = plt.subplots(figsize=(14, 7))
    df['TRAFFIC_CONTROL_DEVICE'].value_counts().sort_values(ascending=True).plot(kind='barh', color='maroon', ax=ax1)
    ax1.set_xlabel('Control device counts', fontsize=12)
    ax1.set_ylabel('Device', fontsize=12)
    st.pyplot(fig1)

    # === DEVICE CONDITION PLOT ===
    st.subheader("Device Condition")
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    df['DEVICE_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='green', ax=ax2)
    ax2.set_xlabel('Device condition counts', fontsize=12)
    ax2.set_ylabel('Condition', fontsize=12)
    st.pyplot(fig2)

    # === WEATHER CONDITION PLOT ===
    st.subheader("Weather Condition")
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    df['WEATHER_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='blue', ax=ax3)
    ax3.set_xlabel('Weather condition counts', fontsize=12)
    ax3.set_ylabel('Condition', fontsize=12)
    st.pyplot(fig3)

    # === LIGHTING CONDITION BAR PLOT ===
    st.subheader("Lighting Condition (Bar Plot)")
    fig4, ax4 = plt.subplots(figsize=(14, 7))
    df['LIGHTING_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='red', ax=ax4)
    ax4.set_xlabel('Lighting condition counts', fontsize=12)
    ax4.set_ylabel('Condition', fontsize=12)
    st.pyplot(fig4)

    # === LIGHTING CONDITION PIE CHART ===
    st.subheader("Lighting Condition (Pie Chart)")
    light = df.groupby('LIGHTING_CONDITION').size().reset_index(name='counts')
    fig5, ax5 = plt.subplots()
    ax5.pie(light['counts'], labels=None, autopct='%1.1f%%')
    ax5.axis('equal')
    ax5.set_title('Lighting Condition')
    ax5.legend(light['LIGHTING_CONDITION'], title="Lighting Types", loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig5)

    # === FIRST CRASH TYPE ===
    st.subheader("First Crash Type")
    fig6, ax6 = plt.subplots(figsize=(14, 7))
    df['FIRST_CRASH_TYPE'].value_counts().sort_values(ascending=True).plot(kind='barh', color='purple', ax=ax6)
    ax6.set_xlabel('First crash counts', fontsize=12)
    ax6.set_ylabel('Crash Type', fontsize=12)
    st.pyplot(fig6)

else:
    st.info("Please upload your Traffic Crashes CSV file to begin.")
