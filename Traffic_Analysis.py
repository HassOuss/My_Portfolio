import streamlit as st 
import seaborn as sns 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('/Users/hass.ouss/Documents/Traffic_Crashes_-_Crashes.csv')
df.T

df.nunique()

df.info()

df.describe().T

# Print the shape of the DataFrame to show the number of rows and columns
print(df.shape)

# find missing values.
# The dataset has 919504 rows and we can see that some variable have more than 900000 missing values. 
# I will remove those variable   
df.isnull().sum()[df.isnull().sum()>0].sort_values(ascending=False)

# Display a random sample of 5 rows of the DataFrame, transposed for better visibility
df.sample(5).T

# Columns names
df.columns

df = df [['CRASH_RECORD_ID',
    #'CRASH_DATE_EST_I', 'CRASH_DATE',
       'POSTED_SPEED_LIMIT', 'TRAFFIC_CONTROL_DEVICE', 'DEVICE_CONDITION',
       'WEATHER_CONDITION', 'LIGHTING_CONDITION', 'FIRST_CRASH_TYPE',
       'TRAFFICWAY_TYPE', 
       #'LANE_CNT', 'INTERSECTION_RELATED_I',
       'ALIGNMENT', 'ROADWAY_SURFACE_COND',
       'ROAD_DEFECT', 'REPORT_TYPE', 'CRASH_TYPE', 
       'NOT_RIGHT_OF_WAY_I', 'HIT_AND_RUN_I', 'DAMAGE', 
       #'DATE_POLICE_NOTIFIED',
       'PRIM_CONTRIBUTORY_CAUSE', 'SEC_CONTRIBUTORY_CAUSE', 
       #'STREET_NO',
       'STREET_DIRECTION', 'STREET_NAME', 'BEAT_OF_OCCURRENCE',
       #'PHOTOS_TAKEN_I', 'STATEMENTS_TAKEN_I', 'DOORING_I', 'WORK_ZONE_I',
       #'WORK_ZONE_TYPE', 'WORKERS_PRESENT_I', 
       'NUM_UNITS',
       'MOST_SEVERE_INJURY', 'INJURIES_TOTAL', 'INJURIES_FATAL',
       'INJURIES_INCAPACITATING', 'INJURIES_NON_INCAPACITATING',
       'INJURIES_REPORTED_NOT_EVIDENT', 'INJURIES_NO_INDICATION',
       'INJURIES_UNKNOWN', 'CRASH_HOUR', 'CRASH_DAY_OF_WEEK', 'CRASH_MONTH',
       'LATITUDE', 'LONGITUDE', 'LOCATION'] ].copy()

df.head().T

# Data Visualization
#Traffic Control
df['TRAFFIC_CONTROL_DEVICE'].value_counts() \
               .sort_values(ascending=True) \
               .plot(kind    ='barh',
                     figsize =(14,7),
                     color   ='Maroon')

plt.xlabel('Control divice counts', fontsize=16, color='Black')
plt.ylabel('Divices ', fontsize=16, color='Black')
plt.xticks(fontsize=12, color='Black')
plt.yticks(fontsize=12, color='Black')
plt.title('Traffic control devices', fontsize=20)
plt.show()

#Device Condition
df['DEVICE_CONDITION'].value_counts() \
               .sort_values(ascending=True) \
               .plot(kind    ='barh',
                     figsize =(14,7),
                     color   ='Green')

plt.xlabel('Device condition counts', fontsize=16, color='Black')
plt.ylabel('Condition', fontsize=16, color='Black')
plt.xticks(fontsize=12, color='Black')
plt.yticks(fontsize=12, color='Black')
plt.title('Device condition', fontsize=20)
plt.show()

# Weather Condition
df['WEATHER_CONDITION'].value_counts() \
               .sort_values(ascending=True) \
               .plot(kind    ='barh',
                     figsize =(14,7),
                     color   ='Blue')

plt.xlabel('Weather condition counts', fontsize=16, color='Black')
plt.ylabel('Condition', fontsize=16, color='Black')
plt.xticks(fontsize=12, color='Black')
plt.yticks(fontsize=12, color='Black')
plt.title('Weather Condition', fontsize=20)
plt.show()

# Lighting Condition
df['LIGHTING_CONDITION'].value_counts() \
               .sort_values(ascending=True) \
               .plot(kind    ='barh',
                     figsize =(14,7),
                     color   ='Red')

plt.xlabel('Lighting condition counts', fontsize=16, color='Black')
plt.ylabel('Divices ', fontsize=16, color='Black')
plt.xticks(fontsize=12, color='Black')
plt.yticks(fontsize=12, color='Black')
plt.title('Lighting condition', fontsize=20)
plt.show()

#Lighting Condition
light_cond = df.groupby('LIGHTING_CONDITION')
light = light_cond.size().reset_index(name='light_cond')

plt.pie(light['light_cond'], labels=None,
        autopct='%1.1f%%')

plt.axis('equal')
plt.title('Lighting condition', fontsize=18)
plt.legend(light['LIGHTING_CONDITION'])
plt.show()

#First crash Type
df['FIRST_CRASH_TYPE'].value_counts() \
               .sort_values(ascending=True) \
               .plot(kind    ='barh',
                     figsize =(14,7),
                     color   ='Purple')

plt.xlabel('First crash counts', fontsize=16, color='Black')
plt.ylabel('Crash', fontsize=16, color='Black')
plt.xticks(fontsize=12, color='Black')
plt.yticks(fontsize=12, color='Black')
plt.title('Traffic control devices', fontsize=20)
plt.show()