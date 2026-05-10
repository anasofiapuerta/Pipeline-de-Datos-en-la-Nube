#### Título

Uso de Azure Databricks sobre Azure Synapse Analytics para la transformación de datos del pipeline de DataCo.

---

#### Contexto

DataCo opera con cuatro sistemas aislados (SAP, Oracle, GPS y Salesforce) que generan datos en formatos inconsistentes. Para resolver esto se requiere cumplir con el requisito funcional de limpiar, estandarizar y enriquecer los datos antes de cargarlos en Azure SQL, eliminando el proceso manual que actualmente tarda entre 3 y 5 días hábiles.

Dado que el volumen de datos puede alcanzar hasta 5 millones de registros por ejecución, el motor de transformación debe garantizar un procesamiento distribuido capaz de completarse dentro de la ventana de máximo 4 horas de rezago.

En este contexto de escalabilidad y calidad de datos (ASR), el sistema debe resolver problemas concretos como fechas mal formateadas, códigos de producto distintos entre SAP y Oracle y la falta de trazabilidad entre facturas y entregas. Todo esto debe lograrse bajo la restricción de presupuesto de no superar los $80 USD mensuales y con un equipo que tiene conocimientos básicos de Python y SQL, sin experiencia previa en Spark ni administración de clústeres.

---

#### Alternativas evaluadas

##### Alternativa 1: Azure Synapse Analytics

>**Ventajas:** Es una plataforma unificada que integra Spark, SQL pools y orquestación en un solo workspace, con alta escalabilidad empresarial desde el inicio, SLA garantizado e integración nativa y profunda con Data Lake Storage Gen2 y Azure SQL.

>**Desventajas:** El nivel mínimo de cómputo (Dedicated SQL Pool DWU100c) tiene un costo aproximado de $1.20 USD/hora, lo que supera el presupuesto mensual de $80 USD en pocos días de uso. Además, su curva de aprendizaje es alta ya que requiere comprender pools, pipelines y workspaces integrados, lo que no se ajusta al perfil del equipo de DataCo.

##### Alternativa 2: Azure Databricks Community Edition

>**Ventajas:** Su costo es cero en Community Edition, respetando completamente el presupuesto de la fase piloto. Los notebooks en Python y SQL reducen la curva de aprendizaje para un equipo sin experiencia en Spark. El procesamiento distribuido en Apache Spark permite escalar hasta 5 millones de registros por ejecución, con integración nativa con Data Lake Storage Gen2 mediante ABFS, Azure SQL y soporte nativo para formato Parquet.

>**Desventajas:** No ofrece SLA en Community Edition, lo que implica riesgo de indisponibilidad sin garantía de recuperación en tiempo definido. Las capacidades de gobernanza y seguridad empresarial son limitadas frente a Synapse Analytics, y si el volumen de datos crece demasiado será necesario migrar a un tier pago.

---

#### Decisión
Se elige Azure Databricks (Community Edition) como motor de transformación del Pipeline de DataCo.

El factor clave es el presupuesto: Azure Synapse Analytics requiere un clúster dedicado que su costo mensualmente supera los $80 USD establecidos para la fase piloto lo que lo descarta desde el punto de vista financiero.

Además, Databricks permite a los analistas trabajar en notebooks Python y SQL (lenguajes que el equipo ya maneja) sin necesidad de administrar infraestructura de clústeres. Para las transformaciones requeridas en DataCo: limpieza de duplicados en `clean_inventory.py`, estandarización de fechas y códigos entre SAP y Oracle, correlación de facturas con entregas GPS en `enrich_deliveries.py`, y conversión a Parquet en `load_warehouse.py` — las capacidades de Azure Databricks son suficientes.

---

#### Consecuencias
##### Ventajas obtenidas:
Costo cero durante la fase piloto, respetando el presupuesto de $80 USD mensuales. Los notebooks en Python y SQL reducen la curva de aprendizaje del equipo. El procesamiento distribuido en Spark permite escalar a 5 millones de registros por ejecución. El formato Parquet en zona curated mejora el rendimiento de las consultas en Power BI. Integración nativa con Data Lake Storage Gen2 y Azure SQL.

##### Trade-offs asumidos:
Azure Databricks (Community Edition) no tiene SLA, lo que genera riesgo de indisponibilidad sin garantía de recuperación en un tiempo definido (crítico en los cierres de mes donde DataCo requiere procesar grandes volúmenes). Las capacidades de gobernanza y seguridad empresarial son limitadas frente a Azure Synapse, lo que puede ser un problema dado que los datos de ventas contienen información sensible de precios y clientes. Si el volumen de datos crece más allá de los 5 millones de
registros, será necesario migrar a un tier pago de Databricks. La dependencia de notebooks puede dificultar la automatización avanzada sin participación del equipo técnico.

---