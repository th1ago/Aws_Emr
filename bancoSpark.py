# Imports
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
        .appName('bancoSpark') \
        .getOrCreate()

# Read from SQL Table
df = spark.read \
  .format("com.microsoft.sqlserver.jdbc.spark") \
  .option("url", "jdbc:sqlserver://{SERVER_ADDR};databaseName=emp;") \
  .option("dbtable", "employee") \
  .option("user", "root") \
  .option("password", "") \
  .load()

df.show()