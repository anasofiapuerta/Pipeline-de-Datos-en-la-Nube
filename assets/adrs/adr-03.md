### Título
**Uso de Azure Data Lake Storage Gen2 con Espacio de Nombres Jerárquico para el almacenamiento del pipeline de DataCo.**

---

#### Contexto
La situación tecnológica de DataCo presenta una fragmentación crítica donde sistemas como SAP, Oracle y Salesforce operan de forma aislada. Para resolver esto, se requiere cumplir con el RF de centralizar los datos en un único repositorio que elimine los silos actuales.

Dado que el volumen de datos puede alcanzar una carga de escritura masiva de hasta 5 millones de registros por ejecución (RNF), es imperativo contar con un servicio que garantice baja latencia en operaciones de entrada/salida (I/O) para no exceder la ventana de actualización de máximo 4 horas de rezago.

Bajo este escenario de escalabilidad y persistencia (ASR), el sistema debe ser capaz de persistir esta carga masiva en el contenedor Raw sin errores de tiempo de espera y permitir que Databricks realice lecturas concurrentes. Todo esto debe lograrse bajo la Restricción presupuestaria de no superar los $80 USD mensuales y siguiendo el Acuerdo de organizar los datos por fuente y fecha en zonas Raw, Silver y Gold.

---

#### Alternativas evaluadas
##### Alternativa 1: Azure Blob Storage Estándar

> **Ventajas:** Representa el costo de almacenamiento más bajo en la nube de Azure, lo cual facilitaría el cumplimiento del límite presupuestario de $80 USD si solo se considerara la persistencia estática de los archivos de SAP y Oracle.

> **Desventajas:** Carece de un sistema de archivos jerárquico real (usa carpetas virtuales), lo que genera una degradación del rendimiento en Spark al listar o renombrar archivos en directorios con millones de registros. 

##### Alternativa 2: Azure Data Lake Storage Gen2

> **Ventajas:** Su Espacio de Nombres Jerárquico (HNS) permite que el pipeline trate los directorios como carpetas físicas reales. Esto es vital para la Arquitectura de Medallón, ya que permite que Databricks mueva y renombre archivos entre las zonas Raw, Silver y Gold de forma atómica y ultrarrápida. Además, permite el uso del protocolo ABFS, optimizado específicamente para que los 5 millones de registros se transfieran con el alto rendimiento necesario para garantizar la frescura de los datos cada 4 horas.

> **Desventajas:** Existe un incremento marginal en el costo de las transacciones de metadatos. Sin embargo, para el volumen de DataCo, este incremento es despreciable frente al ahorro de dinero que se logra al reducir el tiempo de ejecución de los clusters de Databricks.

---

#### Decisión
Se elige implementar Azure Data Lake Storage Gen2 (Tier Standard LRS) con la funcionalidad de Hierarchical Namespace (HNS) habilitada. Esta decisión se fundamenta en la necesidad de garantizar el cumplimiento del SLA de 4 horas. Aunque el costo transaccional es ligeramente superior al Blob Storage tradicional, la capacidad de realizar operaciones atómicas sobre carpetas físicas reduce drásticamente el tiempo de procesamiento en Databricks. Al procesar 5 millones de registros, cada minuto de reducción en el tiempo de ejecución del clúster representa un ahorro directo que permite mantener la factura total del pipeline por debajo de la restricción de $80 USD mensuales.

---

#### Consecuencias
##### Ganancias:
La implementación de esta arquitectura genera ganancias significativas en el rendimiento operativo mediante el uso del protocolo ABFS, que elimina cuellos de botella en la ingesta masiva al comunicarse nativamente con Spark. Asimismo, facilita una organización profesional basada en la Arquitectura de Medallón, permitiendo una separación física clara entre las zonas Bronze, Silver y Gold, además de ofrecer una seguridad granular mediante ACLs para proteger datos sensibles.

##### Trade-offs (Renuncias):
Esta decisión implica una renuncia a la simplicidad administrativa inicial, ya que requiere una gestión más detallada de la estructura jerárquica de carpetas y permisos en comparación con un almacenamiento plano. Adicionalmente, se asume un costo marginalmente superior en las transacciones de metadatos, el cual se acepta bajo la premisa de ser compensado por el ahorro económico derivado de la reducción en los tiempos de ejecución de los clusters de Databricks.

---

