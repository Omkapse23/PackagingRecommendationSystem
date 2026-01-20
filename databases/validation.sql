USE eco_packaging;

SELECT * FROM materials LIMIT 10;

SELECT * FROM materials;

SELECT Material_Type, Product_Category, Biodegradability_Score, Recyclability_Percent, Cost_INR
FROM materials
ORDER BY Biodegradability_Score DESC, Recyclability_Percent DESC
LIMIT 10;

SELECT Material_Type, Biodegradability_Score, Recyclability_Percent, Cost_INR
FROM materials
WHERE Product_Category = 'Textiles'
ORDER BY Biodegradability_Score DESC;

SELECT Material_Type, Biodegradability_Score, Recyclability_Percent, Cost_INR
FROM materials
ORDER BY Cost_INR ASC
LIMIT 10;
