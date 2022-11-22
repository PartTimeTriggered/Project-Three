-- Create Two Tables
DROP TABLE IF EXISTS flu_data;
DROP TABLE IF EXISTS covid_data;
-----------------------------------------------------------------------------------------------------

-- Create  Table for CO2 Emission Per Capita
CREATE TABLE flu_data (
week TEXT,
'state' TEXT PRIMARY KEY,
age_group TEXT,
sex TEXT,
type_subtype TEXT,
count INTEGER
);


SELECT * FROM co2_emission;
--------------------------------------------------------------------------------------------------------------------

-- Create  Table for GDP Per Capita
CREATE TABLE covid_data (
week TEXT,
'state' TEXT,
stste_abbrev TEXT PRIMARY KEY,
confirmed TEXT,
deaths TEXT
);

SELECT * FROM gdp_per_capita;

----------------------------------------------------------------------------------------------------------------------------