#### Título
Uso de Power BI Desktop como solución principal para la capa de visualización e inteligencia de negocio de DataCo

---

#### Contexto
DataCo requiere definir la herramienta principal para la capa de visualización e inteligencia de negocio del proyecto, considerando tanto los requerimientos funcionales como las restricciones técnicas y operativas existentes. Dentro de las necesidades identificadas se encuentra la conexión a múltiples fuentes de datos, la construcción de dashboards interactivos, la publicación y compartición de reportes, la actualización programada de información y el control de acceso por roles. Asimismo, se contemplan atributos no funcionales relacionados con rendimiento, escalabilidad, disponibilidad, seguridad, gobernanza, costos operativos y facilidad de mantenimiento.

Durante el análisis arquitectónico se evaluaron dos alternativas principales: Power BI Desktop junto con Power BI Service, y Azure Analysis Services como capa semántica centralizada consumida desde Power BI. La evaluación surgió debido a la necesidad de contar con una plataforma que permitiera autonomía a los analistas de negocio, integración con múltiples conectores de datos y facilidad para construir visualizaciones sin depender constantemente del equipo de ingeniería.

Dentro de los drivers arquitectónicos más relevantes se identificó la necesidad de minimizar costos operativos iniciales, reducir la complejidad de administración y facilitar la adopción tecnológica por parte del equipo actual. Adicionalmente, se consideró importante mantener una solución escalable que permitiera una futura evolución hacia modelos semánticos centralizados en caso de crecimiento del volumen de datos o mayores requerimientos de gobernanza.

El análisis evidenció que Power BI Desktop ofrece una interfaz intuitiva, integración nativa con diversas fuentes de información y una baja curva de aprendizaje, lo cual favorece la productividad del equipo y reduce tiempos de implementación. Sin embargo, presenta limitaciones relacionadas con la centralización del modelo de datos, el manejo de grandes volúmenes de información y la gobernanza distribuida entre múltiples archivos .pbix.

Por otro lado, Azure Analysis Services proporciona un modelo semántico centralizado, soporte para grandes datasets, integración nativa con Azure Active Directory y capacidades avanzadas de seguridad mediante RLS centralizado. No obstante, implica mayores costos operativos, necesidad de conocimientos especializados en modelado tabular y una complejidad de administración superior para el estado actual del proyecto.

#### Alternativas evaluadas
##### Alternativa 1: Power BI Desktop con Power BI Service

> **Ventajas:** Permite a los analistas de negocio crear y publicar reportes de manera autónoma sin dependencia constante del equipo técnico. Además, posee una interfaz intuitiva y una curva de aprendizaje baja, facilitando la adopción dentro del proyecto. Integra de forma nativa múltiples conectores de datos como Excel, SQL y APIs, y facilita la creación de dashboards interactivos y visuales. Su costo operativo es bajo para equipos pequeños y medianos, y permite la actualización programada de datos mediante Power BI Service y gateway.

> **Desventajas:** El modelo de datos se almacena localmente en archivos .pbix, generando silos de información. Presenta limitaciones para datasets superiores a 1 GB en licencias Pro. La gobernanza y centralización de métricas es limitada, mientras que el control de acceso y seguridad avanzada depende de configuraciones distribuidas. Además, la escalabilidad depende principalmente del dispositivo del usuario.

##### Alternativa 2: Azure Analysis Services

> **Ventajas:** Proporciona un modelo semántico único, centralizado y versionado para toda la organización. Además, soporta grandes volúmenes de datos sin limitaciones prácticas significativas y ofrece escalabilidad horizontal en la nube con alto rendimiento. Integra seguridad avanzada mediante Azure Active Directory y RLS centralizado, garantizando mayor disponibilidad y gobernanza de los datos. Asimismo, mantiene una latencia de consultas estable y consistente.

> **Desventajas:** Presenta un costo operativo elevado desde las configuraciones iniciales y requiere conocimientos avanzados en SSAS, DAX y administración de infraestructura Azure. También incrementa la complejidad de mantenimiento y configuración, reduce la autonomía de los analistas para construir soluciones de manera independiente y posee una curva de aprendizaje considerablemente más alta.


---

#### Decisión
Se decide implementar Power BI como solución principal para la capa de visualización e inteligencia de negocio de DataCo. Esta decisión se fundamenta en la necesidad de contar con una herramienta que permita construir dashboards interactivos, integrar múltiples fuentes de datos y facilitar el acceso a información analítica de manera rápida y eficiente. Power BI ofrece una interfaz intuitiva y una baja curva de aprendizaje, permitiendo que los analistas de negocio desarrollen reportes sin una dependencia constante del equipo técnico. Además, su integración con el ecosistema Microsoft y Azure facilita la conexión con los datos centralizados del proyecto. La solución también permite mantener bajos los costos operativos y simplificar la administración de la plataforma analítica. Por estas razones, se considera la alternativa más adecuada para las necesidades actuales de DataCo.

---

#### Consecuencias
**Ventajas obtenidas:**

Power BI permite construir dashboards interactivos y reportes analíticos de manera rápida, reduciendo significativamente los tiempos de implementación del proyecto. Su integración nativa con múltiples fuentes de datos y con el ecosistema Microsoft facilita la conexión con Azure y los repositorios centralizados de DataCo. La interfaz intuitiva y la baja curva de aprendizaje brindan mayor autonomía a los analistas de negocio, disminuyendo la dependencia constante del equipo técnico. Además, la publicación y actualización programada de reportes simplifica el acceso a información actualizada para la toma de decisiones. El costo operativo inicial es bajo y se ajusta a las restricciones presupuestarias definidas para el proyecto.

**Trade-offs asumidos:**

Power BI presenta limitaciones en la centralización y gobernanza de los modelos de datos debido al uso distribuido de archivos .pbix, lo que puede generar duplicidad de métricas y lógica de negocio. Las licencias Power BI Pro también poseen restricciones en el tamaño de datasets y capacidad de procesamiento, lo que podría afectar el rendimiento si el volumen de datos crece significativamente. Asimismo, la administración de seguridad avanzada y control centralizado es más limitada en comparación con soluciones empresariales como Azure Analysis Services. La escalabilidad depende parcialmente de la capacidad de los equipos cliente y de la infraestructura asociada al servicio. Si DataCo incrementa considerablemente sus necesidades analíticas y de gobernanza, será necesario evolucionar hacia una arquitectura semántica centralizada más robusta.

---