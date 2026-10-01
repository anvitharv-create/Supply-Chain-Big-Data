from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date


# Create Spark session
spark = (
    SparkSession.builder
    .appName("SupplyChainDataIngestion")
    .master("local[*]")
    .getOrCreate()
)

# Keep Spark logs cleaner
spark.sparkContext.setLogLevel("WARN")


# Path to raw dataset
input_path = "data/raw/supply_chain_dataset1.csv"


# Read CSV using Spark
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)


print("\n========== RAW DATASET ==========")
print("Number of rows:", df.count())
print("Number of columns:", len(df.columns))

print("\n========== SCHEMA ==========")
df.printSchema()


# Convert Date from string to Spark DateType
df = df.withColumn(
    "Date",
    to_date(col("Date"), "yyyy-MM-dd")
)


print("\n========== UPDATED SCHEMA ==========")
df.printSchema()


print("\n========== SAMPLE RECORDS ==========")
df.show(5, truncate=False)


# Stop Spark
spark.stop()