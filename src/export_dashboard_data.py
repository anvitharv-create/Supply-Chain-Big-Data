from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, round, desc

spark = (
    SparkSession.builder
    .appName("SupplyChainDashboardExport")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "data/processed/supply_chain_processed"
output_path = "data/dashboard"

df = spark.read.parquet(input_path)

product_analysis = (
    df.groupBy("SKU_ID")
    .agg(
        sum("Units_Sold").alias("Total_Units_Sold"),
        round(sum("Revenue"), 2).alias("Total_Revenue"),
        round(sum("Profit"), 2).alias("Total_Profit"),
        round(avg("Inventory_Level"), 2).alias("Average_Inventory"),
        sum("Stockout_Flag").alias("Total_Stockouts")
    )
    .orderBy(desc("Total_Revenue"))
)

warehouse_analysis = (
    df.groupBy("Warehouse_ID")
    .agg(
        sum("Units_Sold").alias("Total_Units_Sold"),
        round(sum("Revenue"), 2).alias("Total_Revenue"),
        round(avg("Inventory_Level"), 2).alias("Average_Inventory"),
        round(sum("Inventory_Value"), 2).alias("Inventory_Value"),
        sum("Stockout_Flag").alias("Total_Stockouts")
    )
    .orderBy(desc("Total_Revenue"))
)

supplier_analysis = (
    df.groupBy("Supplier_ID")
    .agg(
        round(avg("Supplier_Lead_Time_Days"), 2).alias("Average_Lead_Time"),
        sum("Order_Quantity").alias("Total_Order_Quantity"),
        round(sum("Total_Cost"), 2).alias("Total_Cost"),
        round(sum("Profit"), 2).alias("Total_Profit")
    )
    .orderBy(desc("Total_Order_Quantity"))
)

regional_analysis = (
    df.groupBy("Region")
    .agg(
        sum("Units_Sold").alias("Total_Units_Sold"),
        round(sum("Revenue"), 2).alias("Total_Revenue"),
        round(sum("Profit"), 2).alias("Total_Profit"),
        round(avg("Inventory_Level"), 2).alias("Average_Inventory"),
        sum("Stockout_Flag").alias("Total_Stockouts")
    )
    .orderBy(desc("Total_Revenue"))
)

reorder_analysis = (
    df.groupBy("Reorder_Status")
    .agg(
        count("*").alias("Record_Count"),
        round(avg("Inventory_Level"), 2).alias("Average_Inventory"),
        round(avg("Demand_Forecast"), 2).alias("Average_Demand_Forecast")
    )
    .orderBy(desc("Record_Count"))
)

product_analysis.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{output_path}/product_analysis"
)

warehouse_analysis.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{output_path}/warehouse_analysis"
)

supplier_analysis.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{output_path}/supplier_analysis"
)

regional_analysis.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{output_path}/regional_analysis"
)

reorder_analysis.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{output_path}/reorder_analysis"
)

print("\n========== DASHBOARD DATA EXPORT ==========")
print("Product analysis exported")
print("Warehouse analysis exported")
print("Supplier analysis exported")
print("Regional analysis exported")
print("Reorder analysis exported")
print("Dashboard data saved to:", output_path)

spark.stop()