SELECT
    Warehouse_ID,
    SUM(Units_Sold) AS Total_Units_Sold,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(AVG(Inventory_Level), 2) AS Average_Inventory,
    ROUND(SUM(Inventory_Value), 2) AS Inventory_Value,
    SUM(Stockout_Flag) AS Total_Stockouts
FROM supply_chain
GROUP BY Warehouse_ID
ORDER BY Total_Revenue DESC