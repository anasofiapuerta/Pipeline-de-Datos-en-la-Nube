# Databricks notebook source
dbutils.widgets.text("carpeta_origen", "Carga_Default")
nombre_carpeta = dbutils.widgets.get("carpeta_origen")

#Lee la carpeta dinámica que manda Data Factory
BRONZE_PATH_LEER = f"abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/1-bronze/{nombre_carpeta}/ventas_initial.csv"

#Lo guarda en la misma estructura modular
BRONZE_PATH_ESCRIBIR = f"abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/1-bronze/{nombre_carpeta}/ventas.parquet"

#CONFIGURACIÓN DE CREDENCIALES Y RUTAS
#credencial en Databricks Secrets por peticion de seguridad, no se expone en el código
ACCOUNT_KEY = dbutils.secrets.get(scope="dataco", key="storage-key")
BASE_PATH = "abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/"

storage_options = {
    "fs.azure.account.key.adlsinpipecentralcanada1.dfs.core.windows.net": ACCOUNT_KEY.strip()
}

#Orígenes locales en Databricks
origen_ventas = "dbfs:/Volumes/db_insightpipeline_centralcanada_001/default/bronze/ventas_initial.csv"
origen_deliveries = "dbfs:/Volumes/db_insightpipeline_centralcanada_001/default/bronze/deliveries_gps.csv"

#Destinos finales en la zona Bronze de Azure
destino_ventas = BASE_PATH + "1-bronze/ventas_initial.csv"
destino_deliveries = BASE_PATH + "1-bronze/deliveries_gps.csv"


#LEE LOCAL Y ESCRIBIR EN AZURE (BYPASS DE SPARK CONNECT)
try:
    # Ventas
    print("Transfiriendo y leyendo 'ventas_initial.csv'...")
    # Leemos del almacenamiento local de Databricks
    df_ventas_local = spark.read.option("header", "true").option("inferSchema", "true").csv(origen_ventas)
    
    # Escribimos directamente en Azure pasándole las credenciales en .options()
    df_ventas_local.write \
        .mode("overwrite") \
        .options(**storage_options) \
        .option("header", "true") \
        .csv(destino_ventas)
    
    # Deliveries 
    print("Transfiriendo y leyendo 'deliveries_gps.csv'...")
    df_deliveries_local = spark.read.option("header", "true").option("inferSchema", "true").csv(origen_deliveries)
    
    df_deliveries_local.write \
        .mode("overwrite") \
        .options(**storage_options) \
        .option("header", "true") \
        .csv(destino_deliveries)

    print("Los archivos creados con éxito en la zona 1-bronze de Azure\n")

except Exception as e:
    print(f"Error durante la transferencia de los archivos: {str(e)}")


#validar datos en azure

df_ventas = spark.read \
    .options(**storage_options) \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(destino_ventas)

df_deliveries = spark.read \
    .options(**storage_options) \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(destino_deliveries)


#Datos totales
print(f"Registros totales en ventas_initial: {df_ventas.count()}")
print(f"Registros totales en deliveries_gps: {df_deliveries.count()}")

print("Ventas Iniciales:")
display(df_ventas)

print("\nDeliveries GPS:")
display(df_deliveries.limit(20))