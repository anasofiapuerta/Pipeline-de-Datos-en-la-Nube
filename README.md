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