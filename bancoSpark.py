# Imports
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
        .appName('bancoSpark') \
        .getOrCreate()

# Read from SQL Table
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:sqlserver://localhost:3306;databaseName={cadastro}") \
  .option("driver","com.mysql.jdbc.Driver") \
  .option("dbtable", "cursos") \
  .option("user", "root") \
  .option("password", "") \
  .load()

df.show()