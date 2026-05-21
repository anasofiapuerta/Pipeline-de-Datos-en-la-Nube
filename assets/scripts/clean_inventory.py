# Databricks notebook source
dbutils.widgets.text("carpeta_origen", "Carga_Default")
nombre_carpeta = dbutils.widgets.get("carpeta_origen")

#Lee de Bronze usando el parámetro
ORIGEN_BRONZE = f"abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/1-bronze/{nombre_carpeta}/ventas.parquet"

#Guarda en Silver manteniendo la modularidad
DESTINO_SILVER = f"abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/2-silver/{nombre_carpeta}/ventas_clean"

from pyspark.sql.functions import trim, upper, col, try_to_date, coalesce, lit, when

#Configuración de accesos y rutas
#credencial en Databricks Secrets por peticion de seguridad, no se expone en el código
ACCOUNT_KEY = dbutils.secrets.get(scope="dataco", key="storage-key")
BASE_PATH = "abfss://insightpipeline@adlsinpipecentralcanada1.dfs.core.windows.net/"

bronze_file_path = BASE_PATH + "1-bronze/ventas_initial.csv"
silver_folder_path = BASE_PATH + "2-silver/ventas_clean"

storage_options = {
    "fs.azure.account.key.adlsinpipecentralcanada1.dfs.core.windows.net": ACCOUNT_KEY.strip()
}

#Leer desde la zona Bronze
print("Leyendo datos desde Azure Bronze...")
df_raw = spark.read \
    .options(**storage_options) \
    .option("header", "true") \
    .option("encoding", "UTF-8") \
    .csv(bronze_file_path)


print("Iniciando transformaciones de limpieza y reglas de calidad...")
#Eliminar duplicados si existieran
df_clean = df_raw.dropDuplicates()

#Limpieza de fechas
df_clean = df_clean.withColumn(
    "fecha_limpia",
    coalesce(
        try_to_date(col("fecha"), "yyyy-MM-dd"),
        try_to_date(col("fecha"), "dd/MM/yyyy"),
        try_to_date(col("fecha"), "MM-dd-yyyy"),
        try_to_date(col("fecha"), "d/M/yyyy"),
        try_to_date(col("fecha"), "M-d-yyyy")
    )
).withColumn("fecha", col("fecha_limpia")).drop("fecha_limpia")

#Estandarizar Producto a Mayúsculas
df_clean = df_clean.withColumn("producto", upper(trim(col("producto"))))

#Si el cliente viene vacío "", lo transformamos en None (Null) para poder filtrarlo
df_clean = df_clean.withColumn(
    "cliente_limpio", 
    when(trim(col("cliente")) == "", lit(None)).otherwise(upper(trim(col("cliente"))))
).withColumn("cliente", col("cliente_limpio")).drop("cliente_limpio")

#Borramos cualquier fila que tenga el Cliente o la Fecha como NULL
df_clean = df_clean.dropna(subset=["cliente", "fecha"])

#Tipos numéricos estandarizados
df_clean = df_clean.withColumn("cantidad", col("cantidad").cast("int"))
df_clean = df_clean.withColumn("valor", col("valor").cast("double"))


#Calidad de los datos
print(f"Registros procesados (Bronze):        {df_raw.count()}")
print(f"Registros limpios guardados (Silver): {df_clean.count()}")

display(df_clean.limit(20))

#Guardar en la zona Silver
print(f"Escribiendo datos limpios en la zona Silver: {silver_folder_path}")
(df_clean.coalesce(1).write
 .mode("overwrite")
 .options(**storage_options)
 .option("header", "true")
 .csv(silver_folder_path))

print("¡Proceso de limpieza de finalizado con éxito!")
