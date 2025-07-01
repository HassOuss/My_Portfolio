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
st.subheader("Bar Chart Selector")

bar_plot = st.selectbox(
    "Select a bar chart to view:",
    [
        "Traffic Control Devices",
        "Device Condition",
        "Weather Condition",
        "Lighting Condition",
        "Trafficway Type",
        "Alignment",
        "Roadway Surface Condition",
        "First Crash Type"
    ]
)

if bar_plot == "Traffic Control Devices":
    st.subheader("Traffic Control Devices")
    fig, ax = plt.subplots(figsize=(14, 7))
    df['TRAFFIC_CONTROL_DEVICE'].value_counts().sort_values(ascending=True).plot(kind='barh', color='maroon', ax=ax)
    ax.set_xlabel('Control device counts', fontsize=12)
    ax.set_ylabel('Device', fontsize=12)
    st.pyplot(fig)
elif bar_plot == "Device Condition":
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
   st.subheader("Lighting Condition (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['LIGHTING_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='red', ax=ax)
   ax.set_xlabel('Lighting condition counts', fontsize=12)
   ax.set_ylabel('Condition', fontsize=12)
   st.pyplot(fig)

elif plot_option == "Trafficway Type":
   st.subheader("Trafficway Type (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['TRAFFICWAY_TYPE'].value_counts().sort_values(ascending=True).plot(kind='barh', color ='Orange', ax=ax)
   ax.set_xlabel('Trafficway type counts', fontsize=12)
   ax.set_ylabel('Trafficway', fontsize=12)
   st.pyplot(fig)

elif plot_option == "Alignment":
   st.subheader("Alignment Type (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['ALIGNMENT'].value_counts().sort_values(ascending=True).plot(kind='barh',color='Gray', ax=ax)
   ax.set.xlabel('Alignment type counts', fontsize=12)
   ax.set.ylabel('Alignment', fontsize=12)
   st.pyplot(fig)

elif plot_option == "Roadway Surface Condition":
   st.subheader("Roadway Surface Condition (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['ROADWAY_SURFACE_COND'].value_counts().sort_values(ascending=True).plot(kind='barh',color='Red', ax=ax)
   ax.set.xlabel('Roadway surface condition counts', fontsize=12)
   ax.set.ylabel('Roadway surface condition', fontsize=12)
   st.pyplot(fig)

elif plot_option == "First Crash Type":
   st.subheader("First Crash Type")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['FIRST_CRASH_TYPE'].value_counts().sort_values(ascending=True).plot(kind='barh', color='purple', ax=ax)
   ax.set_xlabel('First crash counts', fontsize=12)
   ax.set_ylabel('Crash Type', fontsize=12)
   st.pyplot(fig)

######
# LIGHTING CONDITION PIE CHART
st.subheader("Lighting Condition (Pie Chart)")
light = df.groupby('LIGHTING_CONDITION').size().reset_index(name='counts')
fig5, ax5 = plt.subplots()
ax5.pie(light['counts'], labels=None, autopct='%1.1f%%')
ax5.axis('equal')
ax5.set_title('Lighting Condition')
ax5.legend(light['LIGHTING_CONDITION'], title="Lighting Types", loc="center left", bbox_to_anchor=(1, 0.5))
st.pyplot(fig5)

# CRASH TYPE
st.subheader("Crash Type (Pie Chart)")
crash = df.groupby('CRASH_TYPE').size().reset_index(name='Crash_Count')
fig6, ax6 = plt.subplots()
ax6.pie(crash['Crash_Count'], labels=None,autopct='%1.1f%%')
ax6.axis('equal')
ax6.set_title('Crash Type')
ax6.legend(crash['CRASH_TYPE'], title="Crash Types", loc="center left", bbox_to_anchor=(1, 0.5))
st.pyplot(fig6)

# DAMAGE
st.subheader("Damage (Pie Chart)")
Damage = df.groupby('DAMAGE').size().reset_index(name='Dam_Count')
fig7, ax7 = plt.subplots()
ax7.pie(Damage['Damage_Count'], labels=None,autopct='%1.1f%%')
ax7.axis('equal')
ax7.set_title('Damage')
ax7.legend(Damage['Damage'], title="Damage", loc="center left", bbox_to_anchor=(1, 0.5))
st.pyplot(fig7)

st.subheader("Crash Trends Over Time")
# TOTAL CRASHES BY HOUR
st.subheader("Total Crashes by Hour")

time_hour = df.groupby('CRASH_HOUR').size().reset_index(name='Number of Crashes')
hourly_crashes = time_hour.groupby('CRASH_HOUR')['Number of Crashes'].sum().reset_index(name='Total Crashes')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_crashes['CRASH_HOUR'], hourly_crashes['Total Crashes'], marker='o')
ax.grid(True)
ax.set_xlabel('Hour of Day', fontsize=14)
ax.set_ylabel('Number of Crashes', fontsize=14)
ax.set_title('Total Crashes by Hour', fontsize=16)
st.pyplot(fig)

# TOTAL CRASHES BY DAY OF THE WEEK
st.subheader("Total Crashes by Day of the Week")

time_day = df.groupby('CRASH_DAY_OF_WEEK').size().reset_index(name='Number of Crashes')
daily_crashes = time_day.groupby('CRASH_DAY_OF_WEEK')['Number of Crashes'].sum().reset_index(name='Total Crashes')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_crashes['CRASH_DAY_OF_WEEK'], daily_crashes['Total Crashes'], marker='o')
ax.grid(True)
ax.set_xlabel('Day of the Week (0=Monday)', fontsize=14)
ax.set_ylabel('Number of Crashes', fontsize=14)
ax.set_title('Total Crashes by Day of the Week', fontsize=16)
st.pyplot(fig)

# TOTAL CRASHES BY MONTH
st.subheader("Total Crashes by Month")

time_month = df.groupby('CRASH_MONTH').size().reset_index(name='Number of Crashes')
monthly_crashes = time_month.groupby('CRASH_MONTH')['Number of Crashes'].sum().reset_index(name='Total Crashes')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_crashes['CRASH_MONTH'], monthly_crashes['Total Crashes'], marker='o')
ax.grid(True)
ax.set_xlabel('Month (1–12)', fontsize=14)
ax.set_ylabel('Number of Crashes', fontsize=14)
ax.set_title('Total Crashes by Month', fontsize=16)
st.pyplot(fig)
