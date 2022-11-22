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


SELECT * FROM flu_data;
--------------------------------------------------------------------------------------------------------------------

-- Create  Table for GDP Per Capita
CREATE TABLE covid_data (
week TEXT,
'state' TEXT PRIMARY KEY,
confirmed INT,
recovered INT,
deaths INT,
confirmed_cum INT,
recovered_cum INT,
deaths_cum INT
);

SELECT * FROM covid_data;

----------------------------------------------------------------------------------------------------------------------------