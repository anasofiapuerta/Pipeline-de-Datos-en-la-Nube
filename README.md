 # Nombre proyecto: InsightPipeline

 ## Tabla de control de cambios 
| ID  |  Autor        | Descripción del cambio           | Fecha      |
|:----| :--- |:---------------------------------|:-----------|
| 01  |Ana Sofia Puerta| Creación de documento            | 02-05-2026 |
| 02  | Ana Sofia Puerta, Ximena Gaibao,Jhosep Tabares, Yoseth lloreda, Oscar Uñates| Incorporación del diagrama de C1 | 05-05-2026 |
| 03 | Ana Sofia Puerta, Ximena Gaibao,Jhosep Tabares, Yoseth lloreda, Oscar Uñates| Incorporación de ADRs | 07-05-2026 |

---

## Arquitectura
### Diagrama de C1
El diagrama de contexto muestra una visión general del Pipeline de datos de DataCo como una caja negra, identificar sus roles principales y los sistemas externos con los que se relaciona (SAP, Oracle, GPS, Salesforce, Power BI).

<div align="center">
  <figure>
    <img src="assets/c4_model/final/c1_final.drawio.png" 
         alt="System Context Diagram showing how people (actors, roles, personas, etc) and software systems are related." 
         width="85%">
    <figcaption>
      <br>
      <i><b>Figure 1:</b> System Context Diagram.</i>
    </figcaption>
  </figure>
</div>

### Analista de Power BI
Este rol se encarga de analizar y visualizar los datos del negocio mediante dashboards e informes. Se conecta a Power BI, el cual obtiene la información desde el Pipeline de Datos DataCo, donde previamente se integran y transforman los datos provenientes de sistemas como SAP, Oracle, GPS y Salesforce. De esta manera, el analista no trabaja con datos crudos, sino con información ya limpia y estructurada.

Dentro del proyecto, su función está en la etapa final del flujo de datos, ya que convierte toda la información procesada en conocimiento útil para el negocio. Sus dashboards y reportes son utilizados por el Gerente Comercial para la toma de decisiones, por lo que actúa como un puente entre los datos técnicos y el uso estratégico de la información

### Gerente Comercial
El gerente comercial toma decisiones estratégicas basadas en información confiable y actualizada, accediendo a dashboards en Power BI donde visualiza indicadores clave del negocio como ventas e inventario.

Utiliza datos procesados por el Pipeline de Datos DataCo y almacenados en Azure SQL, los cuales provienen de sistemas como SAP ERP, Oracle Database y Salesforce CRM, para definir acciones comerciales y evaluar el desempeño.

### Auditor 
Este se encarga de garantizar que los datos de la empresa sean confiables y tengan trazabilidad. No consume dashboards de Power BI; su acceso es directo al sistema.

**Revisar auditoría** sobre el Pipeline de Datos DataCo, verificando que cada transformación aplicada sobre los datos quede registrada y sea trazable.
Esto incluye los logs de ejecución de Azure Data Factory y las tablas de auditoría en Azure SQL.
Este rol es importante para el cumplimiento de las políticas internas de datos de DataCo.

### Sistemas externos
Los sistemas externos son las fuentes de datos que alimentan el pipeline.
Todos envían la información hacia el sistema Pipeline.

**SAP** Es on-premise, sin API. Exporta ventas, pedidos y devoluciones en CSV vía SFTP de forma manual.

**Oracle** Es on-premise, sin API. Exporta stock, movimientos y fechas de vencimiento en archivos planos.

**GPS** No tiene integración automática. Un operador exporta manualmente CSV con rutas, tiempos de entrega, etc.

**Salesforce** Funciona con API REST. Es el único sistema con integración automática. Contiene información de visitas, acuerdos y cartera.

**Power BI** se conecta a Azure SQL y refresca automáticamente los datos cada 4 horas. Lo usa el Analista de BI para construir reportes y el Gerente Comercial para consultarlos.

### Diagrama de C2

## 5 ADRs
### Azure Data Lake Storage Gen2
#### Título
Uso de Azure Data Lake Storage Gen2 con Espacio de Nombres Jerárquico para el almacenamiento del pipeline de DataCo.

---

#### Contexto
La situación tecnológica de DataCo presenta una fragmentación crítica donde sistemas como SAP, Oracle y Salesforce operan de forma aislada. Para resolver esto, se requiere cumplir con el RF de centralizar los datos en un único repositorio que elimine los silos actuales.

Dado que el volumen de datos puede alcanzar una carga de escritura masiva de hasta 5 millones de registros por ejecución (RNF), es imperativo contar con un servicio que garantice baja latencia en operaciones de entrada/salida (I/O) para no exceder la ventana de actualización de máximo 4 horas de rezago.

Bajo este escenario de escalabilidad y persistencia (ASR), el sistema debe ser capaz de persistir esta carga masiva en el contenedor Raw sin errores de tiempo de espera y permitir que Databricks realice lecturas concurrentes. Todo esto debe lograrse bajo la Restricción presupuestaria de no superar los $80 USD mensuales y siguiendo el Acuerdo de organizar los datos por fuente y fecha en zonas Raw, Silver y Gold.

---

#### Alternativas evaluadas
##### Alternativa 1: Azure Blob Storage Estándar

> **Ventajas:** Es la opción de almacenamiento más económica en Azure y es ideal para almacenar grandes cantidades de datos no estructurados.

> **Desventajas:** Carece de un sistema de archivos jerárquico real (usa carpetas virtuales), lo que genera una degradación del rendimiento en Spark al listar o renombrar archivos en directorios con millones de registros.

##### Alternativa 2: Azure Data Lake Storage Gen2

> **Ventajas:** Combina el bajo costo de Blob Storage con el Hierarchical Namespace (HNS). Esto permite que las operaciones sobre directorios sean atómicas (más rápidas) y ofrece seguridad granular mediante Listas de Control de Acceso (ACLs).

> **Desventajas:** La habilitación del espacio de nombres jerárquico implica un costo ligeramente superior en las transacciones de metadatos en comparación con el Blob estándar.

---

#### Decisión
<!-- DEJAR EN BLANCO -->

---

#### Consecuencias
<!-- DEJAR EN BLANCO -->

---

### Azure Data Factory
#### Título
Uso de Azure Data Factory como orquestador principal del pipeline de datos de DataCo

---

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

---

#### Decisión
<!-- DEJAR EN BLANCO -->

---

#### Consecuencias
<!-- DEJAR EN BLANCO -->

---