from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum


# Create Spark session
spark = (
    SparkSession.builder
    .appName("SupplyChainDataValidation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# Load raw dataset
input_path = "data/raw/supply_chain_dataset1.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)


# Convert Date to proper date type
df = df.withColumn(
    "Date",
    col("Date").cast("date")
)


print("\n========== DATA VALIDATION ==========")
print("Total records:", df.count())


# --------------------------------------------------
# 1. Missing value check
# --------------------------------------------------

missing_values = df.select(
    [
        spark_sum(col(c).isNull().cast("int")).alias(c)
        for c in df.columns
    ]
)

print("\n--- Missing Values ---")
missing_values.show(truncate=False)


# --------------------------------------------------
# 2. Business-rule validation
# --------------------------------------------------

valid_records = df.filter(
    (col("Units_Sold") >= 0)
    & (col("Inventory_Level") >= 0)
    & (col("Supplier_Lead_Time_Days") > 0)
    & (col("Reorder_Point") >= 0)
    & (col("Order_Quantity") >= 0)
    & (col("Unit_Cost") > 0)
    & (col("Unit_Price") > 0)
    & (col("Promotion_Flag").isin(0, 1))
    & (col("Stockout_Flag").isin(0, 1))
    & (col("Demand_Forecast") >= 0)
)


valid_count = valid_records.count()
invalid_count = df.count() - valid_count


print("\n--- Business Rule Validation ---")
print("Valid records:", valid_count)
print("Invalid records:", invalid_count)


# --------------------------------------------------
# 3. Duplicate check
# --------------------------------------------------

duplicate_count = (
    df.count() - df.dropDuplicates().count()
)

print("\n--- Duplicate Check ---")
print("Duplicate records:", duplicate_count)


# --------------------------------------------------
# 4. Final validation status
# --------------------------------------------------

if invalid_count == 0 and duplicate_count == 0:
    print("\nValidation Status: PASSED")
else:
    print("\nValidation Status: REVIEW REQUIRED")


# Stop Spark
spark.stop()