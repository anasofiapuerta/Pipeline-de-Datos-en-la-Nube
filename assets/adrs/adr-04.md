#### Título

Uso de Azure SQL Database sobre Azure Cosmos DB como almacén analítico
final del pipeline de datos de DataCo.

---

#### Contexto

DataCo requiere un almacén analítico final donde Azure Databricks deposite los datos transformados —tablas de hechos de ventas, inventario y logística, y dimensiones de clientes, productos y bodegas— para que Power BI Desktop genere dashboards ejecutivos actualizados automáticamente cada 4 horas.

Los ASR y drivers que determinan esta decisión son: la seguridad granular, dado que los datos de precios y márgenes por cliente exigen restricción de acceso por roles directamente en la base de datos, capacidad que solo Azure SQL ofrece de forma nativa con Dynamic Data Masking y Row-Level Security; la restricción presupuestal de 80 USD mensuales, que descarta Cosmos DB al tener un modelo de facturación por Request Units impredecible para cargas analíticas de agregación, mientras que Azure SQL Free Tier tiene costo cero durante el piloto; las habilidades del equipo, compuesto por 2 analistas con conocimientos de SQL y Python básico sin experiencia en el modelo de documentos ni en diseño de particionamiento de Cosmos DB; la compatibilidad nativa con Power BI Desktop gratuito, que incluye el conector SQL Server de forma predeterminada sin configuraciones adicionales; y la naturaleza relacional del modelo de datos, ya que el cruce de facturas SAP con registros GPS y la unificación de clientes entre SAP y Salesforce producen un esquema estrella, no documentos JSON anidados.

---

#### Alternativas evaluadas

##### Alternativa 1: Azure SQL Database

**Ventajas:**Incluye Free Tier (32 GB, 100.000 vCore-segundos/mes) sin costo durante el piloto, soporta Dynamic Data Masking y Row-Level Security de forma nativa, se integra con Databricks vía JDBC y con Power BI Desktop sin configuración adicional, y ofrece índices columnares para consultas
analíticas sobre millones de registros.

**Desventajas:**
Su escalabilidad es principalmente vertical, por lo que volúmenes mayores al piloto requerirían migrar a Azure Synapse Analytics, y su esquema fijo
implica que cualquier cambio estructural necesita migraciones controladas.

---

##### Alternativa 2: Azure Cosmos DB

**Ventajas:**
Ofrece esquema flexible para incorporar nuevas fuentes sin migraciones previas, escalabilidad horizontal automática para cargas de alta
concurrencia y un Free Tier permanente con 1.000 RU/s y 25 GB incluidos.

**Desventajas:**
Su facturación variable por RU/s es impredecible en consultas analíticas y puede superar los 80 USD del piloto, no ofrece Dynamic Data Masking ni
Row-Level Security de forma nativa, el conector para Power BI Desktop gratuito requiere configuración adicional no disponible en la versión
licenciada por DataCo, y el modelo de documentos y particionamiento representan una curva de aprendizaje alta para el equipo.

---

#### Decisión

Se adopta **Azure SQL Database (Free Tier)** como almacén analítico final del pipeline de DataCo.

Azure SQL Database es la única opción que satisface simultáneamente los cuatro drivers del caso: el Free Tier cubre el piloto con costo cero
dentro del presupuesto de 80 USD, Dynamic Data Masking y Row-Level Security protegen los precios y márgenes de SAP sin desarrollo adicional,
el conector SQL Server nativo de Power BI Desktop elimina cualquier configuración extra sobre la licencia existente, y T-SQL es el lenguaje
que los 2 analistas del equipo ya dominan. Adicionalmente, el modelo de datos resultante de cruzar facturas de SAP con registros GPS y unificar
clientes entre SAP y Salesforce produce un esquema estrella que es el caso de uso óptimo para un motor relacional, no para documentos JSON
anidados.
---

#### Consecuencias

**Ventajas obtenidas:**
El pipeline de extremo a extremo opera con conectores nativos en todos los tramos sin dependencias externas, el equipo de DataCo puede auditar
y consultar el almacén directamente en T-SQL sin capacitación adicional, la restricción de acceso a precios y márgenes se implementa en la base
de datos garantizando que ningún perfil omita los controles de seguridad,y el costo del almacén analítico durante la fase piloto es cero,
preservando el presupuesto de 80 USD para los demás servicios del stack.

**Trade-offs asumidos:**
Si DataCo crece hasta superar los 32 GB del Free Tier o requiere cientos de usuarios concurrentes en Power BI, será necesario migrar a Azure
Synapse Analytics con el esfuerzo de migración de esquemas asociado. Además, el esquema relacional fijo exige modelar cualquier nueva fuente
de datos antes de integrarla al almacén, añadiendo un paso de diseño queCosmos DB no habría requerido.
---