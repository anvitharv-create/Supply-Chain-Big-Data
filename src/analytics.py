from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, round, desc

spark = (
    SparkSession.builder
    .appName("SupplyChainAnalytics")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "data/processed/supply_chain_processed"

df = spark.read.parquet(input_path)

print("\n========== DATASET OVERVIEW ==========")
print("Total records:", df.count())
print("Total columns:", len(df.columns))

print("\n========== PRODUCT ANALYSIS ==========")

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

product_analysis.show(10, truncate=False)

print("\n========== WAREHOUSE ANALYSIS ==========")

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

warehouse_analysis.show(10, truncate=False)

print("\n========== SUPPLIER ANALYSIS ==========")

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

supplier_analysis.show(10, truncate=False)

print("\n========== REGIONAL ANALYSIS ==========")

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

regional_analysis.show(truncate=False)

print("\n========== REORDER ANALYSIS ==========")

reorder_analysis = (
    df.groupBy("Reorder_Status")
    .agg(
        count("*").alias("Record_Count"),
        round(avg("Inventory_Level"), 2).alias("Average_Inventory"),
        round(avg("Demand_Forecast"), 2).alias("Average_Demand_Forecast")
    )
    .orderBy(desc("Record_Count"))
)

reorder_analysis.show(truncate=False)

print("\n========== TOP PRODUCTS BY PROFIT ==========")

top_products = (
    product_analysis
    .orderBy(desc("Total_Profit"))
    .limit(10)
)

top_products.show(10, truncate=False)

print("\n========== STOCKOUT ANALYSIS ==========")

stockout_analysis = (
    df.groupBy("SKU_ID")
    .agg(
        sum("Stockout_Flag").alias("Stockout_Count"),
        sum("Units_Sold").alias("Total_Units_Sold"),
        round(avg("Inventory_Level"), 2).alias("Average_Inventory"),
        round(avg("Demand_Forecast"), 2).alias("Average_Demand_Forecast")
    )
    .filter(col("Stockout_Count") > 0)
    .orderBy(desc("Stockout_Count"))
)

stockout_analysis.show(10, truncate=False)

spark.stop()