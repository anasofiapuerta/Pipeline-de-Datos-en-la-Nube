# Databricks notebook source
from pyspark.sql.functions import col, lit, regexp_replace, expr


#CONFIGURACIÓN DE ACCESOS Y RUTAS
#credencial en Databricks Secrets por peticion de seguridad, no se expone en el código
ACCOUNT_KEY = dbutils.secrets.get(scope="dataco", key="storage-key")
BASE_PATH = "abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/"

gold_enriched_path = BASE_PATH + "3-gold/deliveries_enriched"      

storage_options = {
    "fs.azure.account.key.adlsinpipecentralcanada1.dfs.core.windows.net": ACCOUNT_KEY.strip()
}


#Parametros de conexión a Azure SQL Database
DB_HOST = "sql-insightpipeline-centralcanada-001.database.windows.net"  
DB_PORT = "1433"
DB_NAME = "db-insightpipeline"
DB_USER = "sqladmin"
DB_PASSWORD = "Happy#Cat2026"

#Lee y extiende datos en spark
print("Leyendo datos enriquecidos desde la zona Gold (Parquet)...")
df_gold_raw = spark.read.options(**storage_options).parquet(gold_enriched_path)

df_gold = df_gold_raw \
    .withColumn("delivery_id", expr("try_cast(regexp_replace(id_factura, '[a-zA-Z\\\\s]', '') as bigint)")) \
    .withColumn("sale_fk", expr("try_cast(regexp_replace(id_factura, '[a-zA-Z\\\\s]', '') as bigint)")) \
    .withColumn("product_fk", expr("try_cast(regexp_replace(producto, '[a-zA-Z\\\\s]', '') as int)")) \
    .withColumn("customer_fk", expr("try_cast(regexp_replace(cliente, '[a-zA-Z\\\\s]', '') as int)")) \
    .withColumn("delivery_status", lit("Entregado").cast("string")) \
    .withColumnRenamed("fecha", "delivery_date") \
    .withColumnRenamed("latitud", "letitude") \
    .withColumnRenamed("longitud", "longitude") \
    .select("delivery_id", "sale_fk", "product_fk", "customer_fk", "delivery_date", "delivery_status", "letitude", "longitude")

total_registros = df_gold.count()
print(f"Registros listos para transferir: {total_registros}")




tabla_destino = "dw.fact_deliveries"
print(f"Iniciando carga mediante formato nativo 'sqlserver' en '{tabla_destino}'...")

try:
    (df_gold.write
     .format("sqlserver")
     .option("host", DB_HOST)
     .option("port", DB_PORT)
     .option("database", DB_NAME)
     .option("user", DB_USER)
     .option("password", DB_PASSWORD)
     .option("dbtable", tabla_destino)
     .mode("overwrite")
     .save())

    print("¡Carga masiva completada con éxito a Azure SQL relacional!")
    print(f"\nVERIFICACIÓN FINAL: Se han enviado exitosamente {total_registros} registros hacia Azure SQL.")

except Exception as e:
    print(f"Error crítico durante la escritura nativa: {str(e)}")

print("Pipeline de Datos Completado de Extremo a Extremo")