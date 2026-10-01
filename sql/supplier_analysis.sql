SELECT
    Supplier_ID,
    ROUND(AVG(Supplier_Lead_Time_Days), 2) AS Average_Lead_Time,
    SUM(Order_Quantity) AS Total_Order_Quantity,
    ROUND(SUM(Total_Cost), 2) AS Total_Cost,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM supply_chain
GROUP BY Supplier_ID
ORDER BY Total_Order_Quantity DESC