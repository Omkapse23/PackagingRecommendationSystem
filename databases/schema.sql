CREATE DATABASE IF NOT EXISTS eco_packaging;
USE eco_packaging;

DROP TABLE IF EXISTS materials;

CREATE TABLE materials (
    Material_ID VARCHAR(50),
    Material_Type VARCHAR(100),
    Product_Category VARCHAR(100),
    Strength_MPa DOUBLE,
    Weight_Capacity_kg DOUBLE,
    Biodegradability_Score DOUBLE,
    CO2_Emission_kg DOUBLE,
    Recyclability_Percent DOUBLE,
    Source VARCHAR(100),
    Certification VARCHAR(100),
    Cost_INR DOUBLE,
    Notes VARCHAR(255)
);
