
CREATE OR REPLACE TABLE energy_production AS
SELECT * FROM read_csv_auto('/Users/hass.ouss/Documents/Energy_Production.csv');


CREATE OR REPLACE TABLE energy_consumption AS
SELECT * FROM read_csv_auto('/Users/hass.ouss/Documents/Energy_Consumption.csv');

CREATE OR REPLACE TABLE energy_Import AS
SELECT * FROM read_csv_auto('/Users/hass.ouss/Documents/Energy_Import.csv');

PRAGMA table_info(energy_production);
PRAGMA table_info(energy_consumption);
PRAGMA table_info(energy_Import);

SHOW TABLES;
SELECT 
    p.month,
    p.Fossil_Fuels_Production AS Fossil_Production,
    c.Fossil_Fuels_Consumption AS Fossil_Consumption,
    p.Renewable_Energy_Production AS Renewable_production,
    c.Renewable_Energy_Consumption AS Renewable_Consumption,
    p.Nuclear_Electric_Production AS Nuclear_Production,
    c.Nuclear_Electric_Consumption AS Nuclear_Consumption,
    p.Total_Primary_Energy_Production AS Total_Energy_Production,
    c.Total_Primary_Energy_Consumption AS Total_Energy_Consumption
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month
    LIMIT 1000;

 
 --Generate gap for renewable energy
 --The zeros in the gap show that all renewable energy produced were allocated to the consumption.
SELECT 
    p.month,
    p.Renewable_Energy_Production AS renewable_production,
    c.Renewable_Energy_Consumption AS renewable_consumption,
    (p.Renewable_Energy_Production - c.Renewable_Energy_Consumption) AS renewable_gap
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month
    LIMIT 1000;


--Generate gap for nuclear energy   
--The zeros in the gap show that all nuclear energy produced were allocated to the consumption.
SELECT 
    p.month,
    p.Nuclear_Electric_Production AS nuclear_production,
    c.Nuclear_Electric_Consumption AS nuclear_consumption,
    (p.Nuclear_Electric_Production - c.Nuclear_Electric_Consumption) AS nuclear_gap
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month
    LIMIT 1000;


-- Generate gap for fossil energy 
--Throughout the period of 1973-2024, the fossil energy consumption was higher than the fossil energy production.
--The country imports fossil energy to cover the gap. 
SELECT 
    p.month,
    p.Fossil_Fuels_Production AS fossil_production,
    c.Fossil_Fuels_Consumption AS fossil_consumption,
    (p.Fossil_Fuels_Production - c.Fossil_Fuels_Consumption) AS fossil_gap
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month
    LIMIT 1000;

--Generate gap for total energy
SELECT 
    p.month,
    p.Total_Primary_Energy_Production AS total_energy_production,
    c.Total_Primary_Energy_Consumption AS total_energy_consumption,
    (p.Total_Primary_Energy_Production - c.Total_Primary_Energy_Consumption) AS total_gap
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month
    LIMIT 1000;

--Yearly Aggregates
SELECT 
    SUBSTR(p.month, 1, 4) AS year,
    SUM(p.Total_Primary_Energy_Production) AS yearly_production,
    SUM(c.Total_Primary_Energy_Consumption) AS yearly_consumption,
    SUM(p.Total_Primary_Energy_Production - c.Total_Primary_Energy_Consumption) AS yearly_gap
FROM energy_production p
JOIN energy_consumption c ON p.month = c.month
GROUP BY year
ORDER BY year;

--Share of Each Energy Source in Total Production
SELECT 
    p.month,
    (p.Fossil_Fuels_Production / p.Total_Primary_Energy_Production) * 100 AS fossil_share,
    (p.Nuclear_Electric_Production / p.Total_Primary_Energy_Production) * 100 AS nuclear_share,
    (p.Renewable_Energy_Production / p.Total_Primary_Energy_Production) * 100 AS renewable_share
FROM energy_production p
LIMIT 1000;

--Moving Averages (e.g., 12-month average for smoothing)
SELECT 
    month,
    AVG(Total_Primary_Energy_Production) OVER (ORDER BY month ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS moving_avg_production
FROM energy_production;

--Energy Dependency Ratio
--How much of energy consumption is covered by imports:
SELECT 
    p.month,
    c.Total_Primary_Energy_Consumption,
    i."Primary Energy Imports",
    (i."Primary Energy Imports" / c.Total_Primary_Energy_Consumption) * 100 AS import_dependency_percent
FROM energy_production p
JOIN energy_consumption c ON p.month = c.month
JOIN energy_import i ON p.month = i.month;

--Extreme Value Detection
--Find months with highest/lowest renewable share:
SELECT *
FROM (
    SELECT 
        p.month,
        (p.Renewable_Energy_Production / p.Total_Primary_Energy_Production) * 100 AS renewable_share
    FROM energy_production p
) 
ORDER BY renewable_share DESC
LIMIT 5;

-- Looking at total production, total consumption and percentage 
SELECT 
    p.month,
    p.Total_Primary_Energy_Production,
    c.Total_Primary_Energy_Consumption,
    (p.Total_Primary_Energy_Production / c.Total_Primary_Energy_Consumption) * 100 AS Production_percentage
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month   --Energy production month = Energy consumption month 
    LIMIT 1000;

--Looking at percentage of renewable energy production in the total energy production
--Renewable energy production increased from 4% to 9% from 1973 to 2024. 
SELECT 
    p.month,
    p.Renewable_Energy_Production,
    p.Total_Primary_Energy_Production,
    (p.Renewable_Energy_Production / p.Total_Primary_Energy_Production) * 100 AS Renewable_Production_percentage
FROM energy_production p 
JOIN energy_consumption c 
    ON p.month = c.month   --Month Energy production = Month Energy consumption
    LIMIT 1000;


--Compare gap of total energy and import of energy
SELECT 
    p.month,
    (p.Total_Primary_Energy_Production - c.Total_Primary_Energy_Consumption) AS total_gap,
    i."Primary Energy Imports" AS total_energy_import,
    (total_gap + total_energy_import) AS sum_gap_import
FROM energy_production p
JOIN energy_consumption c
    ON p.month = c.month
JOIN energy_Import i
    ON p.month = i.month
LIMIT 1000;

#### Data visualization
# --- Convert 'month' to datetime ---
df["month"] = pd.to_datetime(df["month"], format="%Y-%m")

# --- Title ---
st.title("📊 Energy Production, Consumption, and Gaps Dashboard")

# --- 1. Line Chart: Total Production vs. Consumption ---
st.subheader("Total Primary Energy Production vs. Consumption")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df["month"], df["Total_Production"], label="Total Production", marker="o")
ax1.plot(df["month"], df["Total_Consumption"], label="Total Consumption", marker="x")
ax1.set_title("Total Energy Production vs. Consumption")
ax1.set_xlabel("Year")
ax1.set_ylabel("Energy (units)")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# --- 2. Stacked Bar Chart: Energy Gaps ---
st.subheader("Energy Gaps by Source (Production - Consumption)")

df["Fossil_Gap"] = df["Fossil_Production"] - df["Fossil_Consumption"]
df["Renewable_Gap"] = df["Renewable_Production"] - df["Renewable_Consumption"]
df["Nuclear_Gap"] = df["Nuclear_Production"] - df["Nuclear_Consumption"]

df_gap = df[["month", "Fossil_Gap", "Renewable_Gap", "Nuclear_Gap"]].set_index("month")

fig2, ax2 = plt.subplots(figsize=(12, 6))
df_gap.plot(kind="bar", stacked=True, ax=ax2)
ax2.set_title("Energy Gaps by Source")
ax2.set_ylabel("Gap (Production - Consumption)")
ax2.set_xlabel("Year")
st.pyplot(fig2)

# --- 3. Line Chart: Import Dependency ---
st.subheader("Energy Import Dependency Over Time")

df["Import_Dependency"] = (df["Primary_Energy_Imports"] / df["Total_Consumption"]) * 100

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(df["month"], df["Import_Dependency"], marker="s", color="darkorange")
ax3.set_title("Energy Import Dependency (%)")
ax3.set_xlabel("Year")
ax3.set_ylabel("Import Dependency (%)")
ax3.grid(True)
st.pyplot(fig3)
