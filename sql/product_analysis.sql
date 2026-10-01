SELECT
    SKU_ID,
    SUM(Units_Sold) AS Total_Units_Sold,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(AVG(Inventory_Level), 2) AS Average_Inventory,
    SUM(Stockout_Flag) AS Total_Stockouts
FROM supply_chain
GROUP BY SKU_ID
ORDER BY Total_Revenue DESC
LIMIT 10