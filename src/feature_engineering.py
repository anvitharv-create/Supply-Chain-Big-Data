from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, when

spark = (
    SparkSession.builder
    .appName("SupplyChainFeatureEngineering")
    .master("local[*]")
    .config("spark.hadoop.fs.permissions.umask-mode", "000")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "data/raw/supply_chain_dataset1.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)

df = df.withColumn("Date", col("Date").cast("date"))

df = df.withColumn(
    "Revenue",
    round(col("Units_Sold") * col("Unit_Price"), 2)
)

df = df.withColumn(
    "Total_Cost",
    round(col("Units_Sold") * col("Unit_Cost"), 2)
)

df = df.withColumn(
    "Profit",
    round(col("Revenue") - col("Total_Cost"), 2)
)

df = df.withColumn(
    "Inventory_Value",
    round(col("Inventory_Level") * col("Unit_Cost"), 2)
)

df = df.withColumn(
    "Demand_Variance",
    round(col("Units_Sold") - col("Demand_Forecast"), 2)
)

df = df.withColumn(
    "Reorder_Status",
    when(
        col("Inventory_Level") <= col("Reorder_Point"),
        "REORDER_REQUIRED"
    ).otherwise("STOCK_SUFFICIENT")
)

df = df.withColumn(
    "Stock_Level_Category",
    when(
        col("Inventory_Level") <= col("Reorder_Point"),
        "LOW_STOCK"
    )
    .when(
        col("Inventory_Level") >= col("Reorder_Point") * 1.5,
        "HIGH_STOCK"
    )
    .otherwise("NORMAL_STOCK")
)

print("\nFEATURE ENGINEERING")
print("Total records:", df.count())
print("Total columns:", len(df.columns))

df.select(
    "Date",
    "SKU_ID",
    "Units_Sold",
    "Inventory_Level",
    "Unit_Price",
    "Revenue",
    "Total_Cost",
    "Profit",
    "Inventory_Value",
    "Demand_Forecast",
    "Demand_Variance",
    "Reorder_Status",
    "Stock_Level_Category"
).show(10, truncate=False)

output_path = "data/processed/supply_chain_processed"

df.write.mode("overwrite").parquet(output_path)

print("Processed data saved successfully.")
print("Output path:", output_path)

spark.stop()