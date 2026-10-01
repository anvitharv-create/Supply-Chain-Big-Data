from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("SupplyChainAnalytics")
    .master("local[*]")
    .getOrCreate()
)

print("===================================")
print("Supply Chain Big Data Project")
print("Spark Version:", spark.version)
print("Spark is running successfully!")
print("===================================")

