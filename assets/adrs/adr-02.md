#### Título

Uso de Azure Databricks Premium sobre Azure Synapse Analytics para la transformación de datos del pipeline de DataCo.

---

#### Contexto

DataCo opera con cuatro sistemas aislados (SAP, Oracle, GPS y Salesforce) que generan datos en formatos inconsistentes. Para resolver esto se requiere cumplir con el requisito funcional de limpiar, estandarizar y enriquecer los datos antes de cargarlos en Azure SQL, eliminando el proceso manual que actualmente tarda entre 3 y 5 días hábiles.

Dado que el volumen de datos puede alcanzar hasta 5 millones de registros por ejecución, el motor de transformación debe garantizar un procesamiento distribuido capaz de completarse dentro de la ventana de máximo 4 horas de rezago.

En este contexto de escalabilidad y calidad de datos (ASR), el sistema debe resolver problemas concretos como fechas mal formateadas, códigos de producto distintos entre SAP y Oracle y la falta de trazabilidad entre facturas y entregas. Todo esto debe lograrse bajo la restricción de presupuesto de no superar los $80 USD mensuales y con un equipo que tiene conocimientos básicos de Python y SQL, sin experiencia previa en Spark ni administración de clústeres.

Durante la implementación se identificó que Databricks Community Edition no permite conexiones directas con los servicios de Azure Portal (Data Lake Storage Gen2, Azure SQL Database), por lo que fue necesario migrar a Azure Databricks Premium integrado al portal de Azure, que sí soporta autenticación nativa mediante roles IAM y conexiones directas sin configuración manual de credenciales.

---

#### Alternativas evaluadas

##### Alternativa 1: Azure Synapse Analytics

>**Ventajas:** Es una plataforma unificada que integra Spark, SQL pools y orquestación en un solo workspace, con alta escalabilidad empresarial desde el inicio, SLA garantizado e integración nativa y profunda con Data Lake Storage Gen2 y Azure SQL.

>**Desventajas:** El nivel mínimo de cómputo (Dedicated SQL Pool DWU100c) tiene un costo aproximado de $1.20 USD/hora, lo que supera el presupuesto mensual de $80 USD en pocos días de uso. Además, su curva de aprendizaje es alta ya que requiere comprender pools, pipelines y workspaces integrados, lo que no se ajusta al perfil del equipo de DataCo.

##### Alternativa 2: Azure Databricks Premium

>**Ventajas:** Permite conexiones directas y nativas con Data Lake Storage Gen2 y Azure SQL Database mediante roles IAM, sin necesidad de configurarcredenciales manualmente, se puede hacer uso de la Suscripción de Azure respetando completamente el presupuesto de la fase piloto. Los notebooks en Python y SQL reducen la curva de aprendizaje para un equipo sin experiencia en Spark. El procesamiento distribuido en Apache Spark permite escalar hasta 5 millones de registros por ejecución, con integración nativa con Data Lake Storage Gen2 mediante ABFS, Azure SQL y soporte nativo para formato Parquet.

>**Desventajas:** Tiene costo asociado a diferencia de Community Edition,aunque se mantiene dentro del presupuesto del piloto. Requiere gestión de permisos IAM y roles de Azure que añaden complejidad inicial.

---

#### Decisión
Se elige Azure Databricks Premium como motor de transformación del Pipeline de DataCo.

La migración desde Community Edition fue necesaria porque esta no permite conexiones directas con los servicios de Azure Portal, lo que bloqueaba
la integración con Data Lake Storage Gen2 y Azure SQL Database. Azure Databricks Premium resuelve esto mediante autenticación nativa por roles
IAM, eliminando la necesidad de gestionar credenciales manualmente. Azure Synapse Analytics requiere un clúster dedicado que su costo mensualmente supera los $80 USD establecidos para la fase piloto lo que lo descarta desde el punto de vista financiero.

Además, Databricks permite a los analistas trabajar en notebooks Python y SQL (lenguajes que el equipo ya maneja) sin necesidad de administrar infraestructura de clústeres. Para las transformaciones requeridas en DataCo: limpieza de duplicados en `clean_inventory.py`, estandarización de fechas y códigos entre SAP y Oracle, correlación de facturas con entregas GPS en `enrich_deliveries.py`, y conversión a Parquet en `load_warehouse py` — las capacidades de Azure Databricks son suficientes.

---

#### Consecuencias
##### Ventajas obtenidas:
El costo puede ser poco durante la fase piloto, respetando el presupuesto de $80 USD mensuales. Conexiones directas y nativas con Data Lake Storage Gen2 y Azure SQL mediante roles IAM, eliminando la gestión manual de credenciales. La arquitectura modular que permite a Azure Data Factory orquestar los notebooks de forma independiente para las 4 fuentes de datos cada 4 horas. Los notebooks en Python y SQL reducen la curva de aprendizaje del equipo. El procesamiento distribuido en Spark permite escalar a 5 millones de registros por ejecución. El formato Parquet en zona curated mejora el rendimiento de las consultas en Power BI. Integración nativa con Data Lake Storage Gen2 y Azure SQL.

##### Trade-offs asumidos:
Azure Databricks Premium tiene costo asociado que debe monitorearse para no superar el presupuesto de $80 USD mensuales. La gestión de roles IAM añade complejidad inicial al equipo. La dependencia de notebooks puede dificultar la automatización avanzada sin participación del equipo técnico. Si el volumen de datos crece más allá de los 5 millones de registros, será necesario escalar al clúster con impacto en el costo mensual.

---