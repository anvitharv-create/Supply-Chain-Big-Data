from pyspark.sql import SparkSession
import sys

spark = (
    SparkSession.builder
    .appName("SupplyChainSQLAnalysis")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "data/processed/supply_chain_processed"

df = spark.read.parquet(input_path)

df.createOrReplaceTempView("supply_chain")

sql_file = sys.argv[1]

with open(sql_file, "r") as file:
    query = file.read()

result = spark.sql(query)

print("\n========== SPARK SQL ANALYSIS ==========")
print("SQL File:", sql_file)
result.show(20, truncate=False)

spark.stop()