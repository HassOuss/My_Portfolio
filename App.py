import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to DuckDB
con = duckdb.connect(database=':memory:')

# 2. Loading CSVs into DuckDB tables
con.execute("CREATE TABLE energy_production AS SELECT * FROM read_csv_auto('Energy_Production.csv');")
con.execute("CREATE TABLE energy_consumption AS SELECT * FROM read_csv_auto('Energy_Consumption.csv');")
con.execute("CREATE TABLE energy_import AS SELECT * FROM read_csv_auto('Energy_Import.csv');")

query = """
SELECT
    p.month AS Month,
    p.Total_Primary_Energy_Production AS Total_Production,
    c.Total_Primary_Energy_Consumption AS Total_Consumption,
    p.Fossil_Fuels_Production AS Fossil_Production,
    c.Fossil_Fuels_Consumption AS Fossil_Consumption,
    p.Renewable_Energy_Production AS Renewable_Production,
    c.Renewable_Energy_Consumption AS Renewable_Consumption,
    p.Nuclear_Electric_Production AS Nuclear_Production,
    c.Nuclear_Electric_Consumption AS Nuclear_Consumption,
    i."Primary Energy Imports" AS Primary_Energy_Imports
FROM energy_production p
JOIN energy_consumption c ON p.month = c.month
JOIN energy_import i ON p.month = i.month
"""

df = con.execute(query).df()

# --- Convert 'month' to datetime ---
df["Month"] = pd.to_datetime(df["Month"], format="%Y %B")

df["Year"] = df["Month"].dt.year
df_yearly = df.groupby("Year").mean(numeric_only=True).reset_index()

# --- Title ---
st.title("Energy Production, Consumption, and Gaps Dashboard")

# --- 1. Line Chart: Total Production vs. Consumption ---
st.subheader("Total Primary Energy Production vs. Consumption")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_yearly["Year"], df_yearly["Total_Production"], label="Total Production", marker="o")
ax1.plot(df_yearly["Year"], df_yearly["Total_Consumption"], label="Total Consumption", marker="x")
ax1.set_title("Total Energy Production vs. Consumption")
ax1.set_xlabel("Year")
ax1.set_ylabel("Energy (units)")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# --- 2. Stacked Bar Chart: Energy Gaps ---
st.subheader("Energy Gaps by Source (Production - Consumption)")

df_yearly["Fossil_Gap"] = df_yearly["Fossil_Production"] - df_yearly["Fossil_Consumption"]
df_yearly["Renewable_Gap"] = df_yearly["Renewable_Production"] - df_yearly["Renewable_Consumption"]
df_yearly["Nuclear_Gap"] = df_yearly["Nuclear_Production"] - df_yearly["Nuclear_Consumption"]

df_gap = df_yearly[["Fossil_Gap", "Renewable_Gap", "Nuclear_Gap"]]

fig2, ax2 = plt.subplots(figsize=(12, 6))
df_gap.plot(kind="bar", stacked=True, ax=ax2)
ax2.set_title("Energy Gaps by Source")
ax2.set_ylabel("Gap (Production - Consumption)")
ax2.set_xlabel("Year")
st.pyplot(fig2)

# --- 3. Line Chart: Import Dependency ---
st.subheader("Energy Import Dependency Over Time")

df_yearly["Import_Dependency"] = (df_yearly["Primary_Energy_Imports"] / df_yearly["Total_Consumption"]) * 100

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(df_yearly["Year"], df_yearly["Import_Dependency"], marker="s", color="darkorange")
ax3.set_title("Energy Import Dependency (%)")
ax3.set_xlabel("Year")
ax3.set_ylabel("Import Dependency (%)")
ax3.grid(True)
st.pyplot(fig3)
