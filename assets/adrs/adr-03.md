<table width="100%" style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td align="left" style="border: none;">
      <a href="../../README.md#5-adrs">
        <img src="https://img.shields.io/badge/-%E2%AC%85%EF%B8%8F%20Volver%20al%20README-24292e?style=for-the-badge" alt="Volver al README">
      </a>
    </td>
    <td align="right" style="border: none;">
      <img src="https://img.shields.io/badge/Documento-ADR--03-0078d4?style=for-the-badge" alt="ADR-03">
    </td>
  </tr>
</table>

---

#### Título
**Uso de Azure Data Lake Storage Gen2 con Espacio de Nombres Jerárquico para el almacenamiento del pipeline de DataCo.**

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

