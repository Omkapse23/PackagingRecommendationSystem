USE eco_packaging;

LOAD DATA LOCAL INFILE 'data.csv'
INTO TABLE materials
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Material_ID, Material_Type, Product_Category, Strength_MPa, Weight_Capacity_kg,
 Biodegradability_Score, CO2_Emission_kg, Recyclability_Percent,
 Source, Certification, Cost_INR, Notes);
