
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



    SELECT * FROM read_csv_auto('/Users/hass.ouss/Documents/Energy_Import.csv');
