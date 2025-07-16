import streamlit as st 
import seaborn as sns 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster, HeatMap


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

# === Data Overview ===

st.subheader("Raw Data Preview")
st.dataframe(df.head())

df.nunique()
df.info()
st.subheader("Data Description")
df.describe().T
# Print the shape of the DataFrame to show the number of rows and columns
print(df.shape)

# find missing values.
# The dataset has 919504 rows and we can see that some variable have more than 900000 missing values. 
# I will remove those variable   
df.isnull().sum()[df.isnull().sum()>0].sort_values(ascending=False)

# === Data Preprocessing ===
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
elif bar_plot == "Weather Condition":
   st.subheader("Weather Condition")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['WEATHER_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='blue', ax=ax)
   ax.set_xlabel('Weather condition counts', fontsize=12)
   ax.set_ylabel('Condition', fontsize=12)
   st.pyplot(fig)

elif bar_plot == "Lighting Condition":
   st.subheader("Lighting Condition (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['LIGHTING_CONDITION'].value_counts().sort_values(ascending=True).plot(kind='barh', color='red', ax=ax)
   ax.set_xlabel('Lighting condition counts', fontsize=12)
   ax.set_ylabel('Condition', fontsize=12)
   st.pyplot(fig)

elif bar_plot == "Trafficway Type":
   st.subheader("Trafficway Type (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['TRAFFICWAY_TYPE'].value_counts().sort_values(ascending=True).plot(kind='barh', color ='Orange', ax=ax)
   ax.set_xlabel('Trafficway type counts', fontsize=12)
   ax.set_ylabel('Trafficway', fontsize=12)
   st.pyplot(fig)

elif bar_plot == "Alignment":
   st.subheader("Alignment Type (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['ALIGNMENT'].value_counts().sort_values(ascending=True).plot(kind='barh',color='Gray', ax=ax)
   ax.set_xlabel('Alignment type counts', fontsize=12)
   ax.set_ylabel('Alignment', fontsize=12)
   st.pyplot(fig)

elif bar_plot == "Roadway Surface Condition":
   st.subheader("Roadway Surface Condition (Bar Plot)")
   fig, ax = plt.subplots(figsize=(14, 7))
   df['ROADWAY_SURFACE_COND'].value_counts().sort_values(ascending=True).plot(kind='barh',color='Red', ax=ax)
   ax.set_xlabel('Roadway surface condition counts', fontsize=12)
   ax.set_ylabel('Roadway surface condition', fontsize=12)
   st.pyplot(fig)

elif bar_plot == "First Crash Type":
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
ax7.pie(Damage['Dam_Count'], labels=None,autopct='%1.1f%%')
ax7.axis('equal')
ax7.set_title('Damage')
ax7.legend(Damage['DAMAGE'], title="Damage", loc="center left", bbox_to_anchor=(1, 0.5))
st.pyplot(fig7)

st.subheader("Crash Trends Over Time")
# TOTAL CRASHES BY HOUR
st.subheader("Total Crashes by Hour")
st.markdown("-Among all hours of the day, 3 PM registers the peak in crash frequency.")

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
st.markdown("-Crashes are more frequent on Saturdays than on any other day of the week.")

time_day = df.groupby('CRASH_DAY_OF_WEEK').size().reset_index(name='Number of Crashes')
daily_crashes = time_day.groupby('CRASH_DAY_OF_WEEK')['Number of Crashes'].sum().reset_index(name='Total Crashes')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_crashes['CRASH_DAY_OF_WEEK'], daily_crashes['Total Crashes'], marker='o')
ax.grid(True)
ax.set_xlabel('Day of the Week (1=Monday)', fontsize=14)
ax.set_ylabel('Number of Crashes', fontsize=14)
ax.set_title('Total Crashes by Day of the Week', fontsize=16)
st.pyplot(fig)

# TOTAL CRASHES BY MONTH
st.subheader("Total Crashes by Month")
st.markdown("-**Observation:** Crashes are more frequent in September than in any other month of the year.")

time_month = df.groupby('CRASH_MONTH').size().reset_index(name='Number of Crashes')
monthly_crashes = time_month.groupby('CRASH_MONTH')['Number of Crashes'].sum().reset_index(name='Total Crashes')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_crashes['CRASH_MONTH'], monthly_crashes['Total Crashes'], marker='o')
ax.grid(True)
ax.set_xlabel('Month (1–12)', fontsize=14)
ax.set_ylabel('Number of Crashes', fontsize=14)
ax.set_title('Total Crashes by Month', fontsize=16)
st.pyplot(fig)

######### Test

# Clean column names
df.columns = df.columns.str.strip()

# Convert date to datetime
df['DATE_POLICE_NOTIFIED'] = pd.to_datetime(df['DATE_POLICE_NOTIFIED'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

# Sidebar filters
year_selected = st.sidebar.selectbox(
    "Select Year",
    sorted(df['DATE_POLICE_NOTIFIED'].dt.year.dropna().unique(), reverse=True)
)

view_option = st.sidebar.radio("Map Type", ("Cluster Markers", "Heatmap"))

# Filter data
df_filtered = df[df['DATE_POLICE_NOTIFIED'].dt.year == year_selected]
crash_counts = df_filtered.dropna(subset=["LATITUDE", "LONGITUDE"]) \
    .groupby(["LATITUDE", "LONGITUDE"]).size().reset_index(name='count')

# Create map
default_location = [crash_counts['LATITUDE'].mean(), crash_counts['LONGITUDE'].mean()]
m = folium.Map(location=default_location, zoom_start=11)

# Add selected map layer
if view_option == "Cluster Markers":
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in crash_counts.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=min(row['count'] / 100, 10),
            color='crimson',
            fill=True,
            fill_opacity=0.6,
            popup=f"Crashes: {row['count']}"
        ).add_to(marker_cluster)

elif view_option == "Heatmap":
    heat_data = crash_counts[['LATITUDE', 'LONGITUDE', 'count']].values.tolist()
    HeatMap(heat_data, radius=15).add_to(m)

# Show map
st.subheader("📍 Crash Locations in Chicago")
st_folium(m, width=900, height=500)
