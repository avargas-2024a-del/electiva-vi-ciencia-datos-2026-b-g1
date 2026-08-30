# Actividad Semana 3 — Diseña una arquitectura de datos
## Calidad: Defectos de producción

**Programa:** Ingeniería Industrial | **Asignatura:** Ciencia de Datos | **Unidad:** 1 — Fundamentos de Ciencia de Datos y Big Data | **Periodo:** 2026-B | **Estudiante:** Angelica Vargas Zambrano

Esta actividad da continuidad al proyecto de las Semanas 1 y 2 (*Calidad — Defectos de producción*), cuya pregunta de negocio es: **¿qué factores del proceso (velocidad de línea, temperatura, turno, proveedor) aumentan la probabilidad de que un producto salga defectuoso?**, y cuyas seis fuentes de datos (estructuradas, semiestructuradas y no estructuradas) fueron identificadas en la Semana 2.

---

## 1. Marco de referencia y conceptos

### 1.1 Arquitectura de datos: de la fuente al valor

Una arquitectura de datos organiza el flujo de la información en cinco etapas enlazadas: **fuentes → ingesta → almacenamiento → procesamiento → análisis/BI**, cada una con una responsabilidad específica: el origen de la información, los mecanismos para capturarla, los repositorios donde se guarda, las transformaciones que la depuran y estructuran, y la visualización que la convierte en decisiones (CORHUILA, 2026). Diseñar correctamente esta arquitectura es lo que permite que las seis fuentes identificadas en la Semana 2 —sensores IoT, sistema MES/ERP, registros SCADA, imágenes y notas de operarios, entre otras— terminen convertidas en el conocimiento accionable que requiere la decisión esperada del proyecto.

### 1.2 Data lake vs. data warehouse

Un **data lake** almacena datos crudos de cualquier tipo tal como llegan, lo que lo hace económico, flexible y adecuado para exploración e investigación; un **data warehouse**, en cambio, almacena información ya estructurada y procesada, optimizada para consultas y reportes empresariales (CORHUILA, 2026). En la práctica moderna, ambos enfoques ya no se ven como mutuamente excluyentes: Zaharia, Ghodsi, Xin y Armbrust (2021) proponen el concepto de *lakehouse*, una arquitectura que combina el almacenamiento crudo y económico del data lake con las garantías de calidad, esquema y rendimiento de consulta propias de un data warehouse, evitando así la duplicación de datos entre ambos sistemas. Este concepto es especialmente relevante cuando una organización necesita, como en este proyecto, conservar datos no estructurados (imágenes de piezas defectuosas, notas de operarios) junto con datos ya curados y listos para reportes de calidad.

### 1.3 Procesamiento por lotes (batch) vs. en tiempo real (streaming)

El procesamiento **por lotes** (*batch*) opera sobre grandes volúmenes de datos acumulados en intervalos programados (por ejemplo, un análisis nocturno), mientras que el procesamiento en **tiempo real** (*streaming*) procesa los datos de forma continua conforme van llegando, como ocurre con la telemetría de sensores (CORHUILA, 2026). Akidau et al. (2015), en su propuesta del *Dataflow Model*, muestran que un mismo sistema de procesamiento puede tratar de forma unificada datos acotados (batch) y datos no acotados (streaming), permitiendo equilibrar de manera explícita la latencia, el costo y la exactitud requeridos por cada caso de uso en lugar de forzar una elección única para toda la arquitectura.

### 1.4 Herramientas típicas del ecosistema de Big Data

El ecosistema de herramientas de Big Data cubre cada etapa de la arquitectura: para la **ingesta** en tiempo real se usan colas de eventos como Kafka; para el **almacenamiento** distribuido, sistemas como Hadoop; para el **procesamiento**, motores de análisis en memoria como Spark o herramientas de transformación como dbt; y para la **orquestación** de flujos ETL, herramientas como Airflow o n8n (CORHUILA, 2026). Un error frecuente en este ecosistema es convertir el data lake en un "pantano de datos" (*data swamp*) por falta de catalogación, o adoptar streaming de forma innecesaria cuando el caso de uso no lo requiere (CORHUILA, 2026); ambas advertencias se tienen en cuenta en el diseño propuesto a continuación.

---

## 2. Enunciado de la actividad

### 2.1 Arquitectura del flujo de datos (fuentes → ingesta → almacenamiento → procesamiento → análisis/BI)

```
 1. FUENTES                2. INGESTA          3. ALMACENAMIENTO             4. PROCESAMIENTO         5. ANÁLISIS / BI
 ─────────────────         ──────────          ─────────────────────         ────────────────────     ─────────────────
 · Sensores IoT de línea
   (temp., velocidad,
   vibración)
 · Sistema MES/ERP           Apache Kafka        Zona cruda (lake)             Apache Spark              Power BI
   (turnos, proveedores,     ------------        · JSON, imágenes,             ------------              ------------
   órdenes)                  Streams              logs SCADA, texto            Batch: agregación         Tableros de
 · Registros SCADA           (sensores/alarmas)   libre de operarios           diaria de defectos         tasa de defectos
   (alarmas,             ──► Lotes           ──►  · Datos tal como     ────►   Streaming: detección ──►   por turno,
   mantenimiento)             (MES/ERP, dataset    llegan                      de condiciones de           proveedor y
 · Inspección de calidad      histórico)                                       riesgo en línea             condición de
   (imágenes + reportes)                          Zona curada                                              proceso
 · Dataset histórico                              (warehouse)
   (Kaggle: proceso                               · Tablas limpias
   y defectos)                                      listas para BI
```

### 2.2 Decisión: ¿data lake o warehouse? ¿batch o streaming?

**Data lake, con una capa curada tipo warehouse (enfoque lakehouse).** El proyecto necesita un data lake porque dos de sus seis fuentes (imágenes de piezas defectuosas y notas de texto libre de los operarios, identificadas en la Semana 2) son no estructuradas y no pueden forzarse a un esquema tabular rígido sin perder información; además, los registros SCADA llegan en JSON semiestructurado que conviene conservar en su forma original para no descartar campos útiles a futuro (CORHUILA, 2026). Sin embargo, el análisis de calidad que exige la pregunta de negocio (qué factores aumentan el riesgo de defecto) depende de tablas limpias y consultables rápidamente, por lo que se justifica una capa curada tipo data warehouse sobre ese mismo repositorio, siguiendo el modelo de *lakehouse* de Zaharia et al. (2021): se evita así duplicar la infraestructura y se conserva tanto el dato crudo como la vista analítica lista para BI.

**Combinación de batch y streaming, no una sola opción.** El proyecto requiere **streaming** para la telemetría de sensores (temperatura, velocidad de línea) y las alarmas del SCADA, porque el valor de detectar una condición de riesgo depende de actuar antes de que se produzcan más unidades defectuosas; y requiere **batch** para consolidar diariamente los datos del MES/ERP, las inspecciones de calidad y el histórico del dataset de Kaggle, ya que estos no cambian con la misma urgencia y un procesamiento nocturno es más económico y suficiente para alimentar los reportes de BI. Esta combinación sigue el planteamiento de Akidau et al. (2015), quienes muestran que un mismo modelo de procesamiento puede balancear explícitamente latencia y costo en lugar de tratar toda la arquitectura como streaming "por defecto", uno de los errores frecuentes señalados en la sección 1.4.

### 2.3 Herramienta candidata por etapa, justificada

| Etapa | Herramienta candidata | Por qué es pertinente para este caso |
|---|---|---|
| **Ingesta** | **Apache Kafka** | Es una cola de eventos en tiempo real (CORHUILA, 2026) capaz de recibir simultáneamente la telemetría continua de los sensores de línea y las alarmas del SCADA (streaming), así como las cargas periódicas del MES/ERP y del dataset histórico (batch), unificando la entrada de las seis fuentes de la Semana 2 en un solo punto de ingesta. |
| **Procesamiento** | **Apache Spark** | Es un motor de procesamiento en memoria (CORHUILA, 2026) que soporta tanto trabajos por lotes (agregación diaria de tasas de defecto) como procesamiento en flujo (detección casi en tiempo real de temperaturas o velocidades fuera de rango), lo que se ajusta directamente a la combinación batch/streaming justificada en la sección 2.2, evitando adoptar dos motores distintos para cada modo. |
| **Análisis / BI** | **Power BI** | Permite construir tableros que crucen la tasa de defectos con velocidad de línea, temperatura, turno y proveedor —las variables exactas de la pregunta de negocio de la Semana 1— y refrescarse tanto desde la capa batch (reportes diarios) como desde flujos casi en tiempo real, entregando a los responsables de planta la vista necesaria para decidir dónde ajustar parámetros o reforzar inspección. |

---

## 3. Referencias bibliográficas

Akidau, T., Bradshaw, R., Chambers, C., Chernyak, S., Fernández-Moctezuma, R. J., Lax, R., McVeety, S., Mills, D., Perry, F., Schmidt, E., & Whittle, S. (2015). The dataflow model: A practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing. *Proceedings of the VLDB Endowment*, 8(12), 1792–1803. https://doi.org/10.14778/2824032.2824076

CORHUILA — Corporación Universitaria del Huila. (2026). *Ciencia de Datos · Semana 3 · Ecosistema de Big Data* [Material de curso]. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/03-week/01-session/

Zaharia, M., Ghodsi, A., Xin, R., & Armbrust, M. (2021). Lakehouse: A new generation of open platforms that unify data warehousing and advanced analytics. En *Proceedings of the 11th Conference on Innovative Data Systems Research (CIDR 2021)*.
