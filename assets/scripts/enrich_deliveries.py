# Databricks notebook source
dbutils.widgets.text("carpeta_origen", "Carga_Default")
nombre_carpeta = dbutils.widgets.get("carpeta_origen")

# LECTURA: Lee el archivo limpio de Silver
ORIGEN_SILVER = f"abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/2-silver/{nombre_carpeta}/ventas_clean"

# ESCRITURA: Guarda el Parquet final en Gold
DESTINO_GOLD = f"abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/3-gold/{nombre_carpeta}/deliveries_enriched"
from pyspark.sql.functions import col

#CONFIGURACIÓN DE ACCESOS Y RUTAS
#credencial en Databricks Secrets por peticion de seguridad, no se expone en el código
ACCOUNT_KEY = dbutils.secrets.get(scope="dataco", key="storage-key")
BASE_PATH = "abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/"

#Rutas
silver_ventas_path = BASE_PATH + "2-silver/ventas_clean"         
bronze_gps_path = BASE_PATH + "1-bronze/deliveries_gps.csv"    
gold_output_path = BASE_PATH + "3-gold/deliveries_enriched" # Nombre estándar de salida    

storage_options = {
    "fs.azure.account.key.adlsinpipecentralcanada1.dfs.core.windows.net": ACCOUNT_KEY.strip()
}

#LEER DATOS DESDE STORAGE
print("Leyendo datos limpios de Ventas desde la zona Silver...")
df_ventas = spark.read \
    .options(**storage_options) \
    .option("header", "true") \
    .csv(silver_ventas_path)

print("Leyendo datos de Deliveries GPS desde la zona Bronze...")
df_gps = spark.read \
    .options(**storage_options) \
    .option("header", "true") \
    .csv(bronze_gps_path)


#PROCESO DE ENRIQUECIMIENTO (JOIN POR ID_FACTURA)
print("\nRealizando la unión de datos (Join por ID de Factura)...")

# CORRECCIÓN: Cruzamos por la columna en común real que vincula ambos datasets
df_enrich = df_ventas.join(df_gps, on="id_factura", how="inner")


#COMPROBACIÓN Y AUDITORÍA DE REGISTROS
print(f"Registros en Ventas (Silver):       {df_ventas.count()}")
print(f"Registros en GPS (Bronze):          {df_gps.count()}")
print(f"Registros Finales Cruzados (Gold): {df_enrich.count()}")

#Mostrar una vista previa antes de guardar
display(df_enrich.limit(20))


#GUARDAR EN LA ZONA GOLD EN FORMATO PARQUET
print(f"Guardando los datos enriquecidos en formato Parquet en: {gold_output_path}")

(df_enrich.write
 .mode("overwrite")
 .options(**storage_options)
 .parquet(gold_output_path))

print("¡El proceso de enriquecimiento para la zona Gold ha finalizado con éxito!")