### Azure Data Factory
#### Título
Uso de Azure Data Factory como orquestador principal del pipeline de datos de DataCo

#### Contexto
DataCo enfrenta una fragmentación crítica de sus datos: cuatro sistemas fuente completamente aislados entre sí. El ERP de ventas corre sobre SAP On-premise sin API REST disponible, lo que obliga a trabajar con archivos CSV o JSON depositados por SFTP. El sistema de inventario opera sobre Oracle Database local, el GPS de flota genera archivos CSV exportados manualmente y el CRM comercial vive en Salesforce Cloud. Esta desintegración le cuesta a la empresa entre 3 y 5 días hábiles para consolidar un informe ejecutivo semanal, y el equipo de gerencia toma decisiones con hasta 72 horas de rezago en los datos de inventario.

Se necesita una herramienta que permita encadenar la ingesta desde esas cuatro fuentes hacia Azure Data Lake Storage Gen2, disparar los notebooks de transformación en Databricks y finalmente cargar los datos limpios en Azure SQL Database, todo dentro de un presupuesto mensual que no puede superar los $80 USD. El equipo de datos está formado por dos analistas con conocimientos de SQL y Python básico, sin experiencia en Spark ni administración de clusters, por lo que la operabilidad también fue un factor determinante en la evaluación.

Para tomar esta decisión se identificaron los drivers que condicionan directamente el comportamiento del orquestador: en el plano funcional, la herramienta debe ser capaz de mover datos diarios desde las cuatro fuentes heterogéneas (SAP por CSV/SFTP, Oracle por exportación JDBC, GPS por CSV manual y Salesforce por API REST), invocar notebooks de Databricks para la limpieza, estandarización de códigos de producto y cliente, eliminación de duplicados y enriquecimiento, y encadenar actividades con dependencias, condiciones de éxito o fallo y reintentos automáticos por cada fuente de forma independiente. Además, debe ejecutarse de forma programada cada 4 horas para cumplir el rezago máximo requerido, garantizar que si una de las cuatro fuentes falla en un ciclo las demás se procesen igualmente sin interrumpir el pipeline completo, ofrecer logs por actividad y visibilidad completa de cada ejecución para cumplir las políticas internas de gobierno de datos, e invocar notebooks de Azure Databricks y cargar resultados directamente en Azure SQL Database desde el mismo pipeline.

En el plano no funcional, los atributos que no pueden sacrificarse son: la escalabilidad para procesar hasta 5 millones de registros por ejecución y soportar cierres de mes y temporadas altas sin intervención manual; la seguridad mediante control de acceso por roles (RBAC) e integración con Key Vault para el manejo seguro de credenciales de las cuatro fuentes; el costo, con un presupuesto mensual máximo de $80 USD en fase piloto bajo un modelo pay-per-use sin costo en reposo; la mantenibilidad, para que los dos analistas SQL/Python puedan operar y mantener el pipeline sin necesidad de asistencia externa permanente; y la integración con el repositorio GitHub del proyecto para el versionamiento de pipelines y el despliegue controlado.


---

#### Alternativas evaluadas
##### Alternativa S1 — Azure Data Factory (ADF)

> **Ventajas:** Entre las ventajas de ADF se destacan que está diseñado para mover y transformar datos en batch a gran escala (TB/PB), que ofrece integración nativa con todo el stack —ADLS Gen2, Databricks y Azure SQL— sin necesidad de construir puentes adicionales, y que su tier gratuito de 5 actividades/mes es suficiente para la fase piloto sin comprometer el presupuesto de $80 USD. Además, su monitor de ejecución con logs por actividad garantiza la trazabilidad completa exigida por el gobierno de datos de DataCo, el aislamiento de fallos por rama asegura que si SAP falla los demás sistemas se procesen igualmente, y cuenta con CI/CD nativo con GitHub y Azure DevOps para el versionamiento de pipelines.

> **Desventajas:** En cuanto a las desventajas, ADF presenta un cold-start de 20 a 40 segundos que lo hace no apto para casos en tiempo real, una curva de aprendizaje moderada que obligará al equipo a formarse en ADF Studio y en el modelo de DIU, un precio por DIU que puede escalar de forma inesperada en Data Flows de alto volumen si no se monitorea, y la limitación de no ser apto para latencias sub-segundo, lo que implicaría complementarlo si DataCo requiere streaming en el futuro.

##### Alternativa S2 — Azure Logic Apps (ALA)

> **Ventajas:** Las ventajas de Logic Apps incluyen su diseñador visual intuitivo sin código, que es accesible para los dos analistas SQL/Python sin necesidad de formación en Spark; su latencia sub-segundo nativa, ideal para workflows event-driven y respuesta a eventos en tiempo real; su catálogo de más de 400 conectores para servicios empresariales, incluyendo el CRM Salesforce utilizado en DataCo; y la ausencia de gestión de clusters o infraestructura propia, lo que reduce la carga operativa del equipo.

> **Desventajas:** Como desventajas, Logic Apps no está diseñado para mover grandes volúmenes de datos en batch y trabaja únicamente con mensajes ligeros; carece de transformaciones complejas nativas como Spark o Data Flows para la limpieza avanzada de datos; tiene un modelo de precio por acción que resulta costoso a alto volumen y representa un riesgo real de superar los $80 USD mensuales; y no cuenta con actividad nativa para invocar notebooks de Databricks ni cargar datos directamente en Azure SQL.

#### Decisión

Después de evaluar las alternativas tecnológicas, DataCo decide adoptar Azure Data Factory como orquestador principal del pipeline de datos corporativo. La decisión se fundamenta en que ADF es la herramienta que mejor se ajusta a los requerimientos funcionales y no funcionales definidos para el proyecto, especialmente en escenarios de integración híbrida y procesamiento batch de múltiples fuentes heterogéneas. Su capacidad para conectarse de manera nativa con SAP mediante archivos CSV/SFTP, Oracle Database, Salesforce y Azure Data Lake Storage Gen2 permite centralizar la ingesta de datos sin desarrollar integraciones personalizadas complejas, reduciendo el esfuerzo operativo del equipo de analistas
---

#### Consecuencias

#### Ventajas obtenidas:

La implementación de Azure Data Factory permitirá a DataCo obtener una mejora considerable en la eficiencia operativa y en la disponibilidad de la información. Gracias a la automatización del pipeline de datos, la empresa reducirá drásticamente los tiempos de consolidación de reportes, permitiendo que la gerencia tome decisiones basadas en datos más recientes y confiables. Esto también disminuirá la carga manual del equipo de analistas, quienes ya no tendrán que ejecutar procesos repetitivos de integración y limpieza de datos, pudiendo enfocarse en actividades de análisis y generación de valor para el negocio.

---
#### Trade-offs (Renuncias)
Al seleccionar Azure Data Factory, DataCo acepta renunciar a ciertas capacidades que otras alternativas como Azure Logic Apps ofrecen de manera más eficiente. La principal renuncia es la capacidad de trabajar con procesamiento en tiempo real o latencias sub-segundo, ya que ADF está orientado principalmente a procesos batch y no a arquitecturas event-driven o streaming. Esto significa que la empresa prioriza estabilidad y procesamiento masivo de datos sobre velocidad inmediata de respuesta.