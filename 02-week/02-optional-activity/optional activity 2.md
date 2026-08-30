# Actividad Semana 2 — Clasifica datos y las V del Big Data
## Calidad: Defectos de producción

**Programa:** Ingeniería Industrial | **Asignatura:** Ciencia de Datos | **Unidad:** 1 — Fundamentos de Ciencia de Datos y Big Data | **Periodo:** 2026-B | **Estudiante:** Angelica Vargas Zambrano

Esta actividad da continuidad al proyecto de la Semana 1 (*Calidad — Defectos de producción*), cuya pregunta de negocio es: **¿qué factores del proceso (velocidad de línea, temperatura, turno, proveedor) aumentan la probabilidad de que un producto salga defectuoso?**

---

## 1. Marco de referencia y conceptos

### 1.1 Big Data: definición

El Big Data se define como conjuntos de datos tan grandes, rápidos o variados que superan la capacidad de las herramientas tradicionales de almacenamiento y análisis, por lo que requieren tecnologías distribuidas para procesarse (CORHUILA, 2026). Esta noción tiene su origen en el trabajo seminal de Laney (2001), quien —en un informe del META Group— caracterizó por primera vez el crecimiento de los datos empresariales a lo largo de tres dimensiones críticas de gestión: **volumen** (cantidad de datos), **velocidad** (rapidez con la que se generan y deben procesarse) y **variedad** (diversidad de formatos y fuentes), sentando así la base conceptual de lo que hoy se conoce como las "V" del Big Data.

### 1.2 Las V del Big Data

A las tres dimensiones originales de Laney (2001) se han sumado posteriormente la **veracidad** (calidad y confiabilidad de los datos) y el **valor** (utilidad real de los datos para la toma de decisiones), configurando el modelo de cinco V ampliamente usado en la actualidad (CORHUILA, 2026):

| V | Descripción | Ejemplo en un caso industrial |
|---|---|---|
| **Volumen** | Cantidad masiva de información generada | Sensores de planta en operación continua |
| **Velocidad** | Datos generados y requeridos en tiempo real | Telemetría de máquinas |
| **Variedad** | Múltiples formatos: números, texto, imágenes, logs | Información heterogénea del proceso |
| **Veracidad** | Calidad y confiabilidad de los datos | Lecturas con ruido o datos faltantes |
| **Valor** | Utilidad de los datos para tomar decisiones | Predicción preventiva de fallos |

La pertinencia de este modelo para entornos de manufactura está respaldada empíricamente: Syafrudin et al. (2018) implementaron y evaluaron un sistema de monitoreo en tiempo real basado en sensores IoT para una planta de manufactura automotriz, mostrando que el volumen y la velocidad de los datos generados por los sensores de línea, junto con su veracidad (ruido, valores atípicos y datos faltantes propios de la captura por sensores), son factores determinantes tanto del desempeño del sistema de monitoreo como de la calidad de las predicciones de fallos y defectos obtenidas a partir de esos datos.

### 1.3 Clasificación de los datos por estructura

De acuerdo con el material del curso (CORHUILA, 2026), los datos se clasifican según su nivel de estructura en tres categorías:

- **Estructurados:** organizados en tablas con filas y columnas fijas (bases de datos relacionales, archivos CSV).
- **Semiestructurados:** tienen una estructura flexible o autodescriptiva, pero no tabular rígida (JSON, XML).
- **No estructurados:** carecen de un formato fijo (texto libre, imágenes, audio, video).

Esta clasificación es la que se aplica a continuación sobre las fuentes de datos del proyecto de calidad y defectos de producción.

---

## 2. Enunciado de la actividad

### 2.1 Fuentes de datos del caso, clasificadas por estructura

Para responder la pregunta de negocio del proyecto (Semana 1) se requieren, en un escenario real de planta, al menos las siguientes seis fuentes de datos, cada una clasificada de forma **correcta** —criterio de excelencia de la rúbrica— según los tres tipos definidos en la sección 1.3:

| # | Fuente de datos | Descripción | Clasificación |
|---|---|---|---|
| 1 | Dataset de proceso y defectos (Kaggle) | Registro tabular histórico con velocidad de línea, temperatura, turno, proveedor y tasa de defectos por lote (El Kharoua, s.f.) | **Estructurado** |
| 2 | Sensores IoT de línea de producción | Series de tiempo de temperatura, velocidad y vibración capturadas automáticamente por sensores de planta | **Estructurado** |
| 3 | Sistema MES/ERP de producción | Base de datos relacional con órdenes de producción, turnos de trabajo y proveedores de materia prima | **Estructurado** |
| 4 | Registros del sistema SCADA de mantenimiento | Bitácoras de eventos y alarmas de máquina exportadas en formato JSON | **Semiestructurado** |
| 5 | Fotografías de piezas defectuosas | Imágenes capturadas por las cámaras del puesto de inspección de calidad | **No estructurado** |
| 6 | Notas y correos de los operarios de turno | Observaciones en texto libre sobre incidencias o condiciones inusuales durante la producción | **No estructurado** |


### 2.2 V del Big Data críticas para el caso, justificadas

Con base en el marco conceptual de la sección 1.2, las cinco V son relevantes para este proyecto, pero con distinto nivel de criticidad según la fuente de datos:

- **Volumen (crítica):** los sensores de línea (fuente 2) generan lecturas de forma continua durante toda la operación de la planta, lo que produce un caudal de datos que una hoja de cálculo no podría manejar y que exige almacenamiento distribuido, tal como describen Laney (2001) y Syafrudin et al. (2018) para entornos IoT de manufactura.
- **Velocidad (crítica):** la telemetría de máquina (fuente 2) y las alarmas del SCADA (fuente 4) deben procesarse en tiempo real o casi real, porque la utilidad de detectar una condición de riesgo (por ejemplo, temperatura fuera de rango) depende de actuar antes de que se generen más unidades defectuosas.
- **Variedad (crítica):** el caso combina explícitamente los tres tipos de estructura identificados en la sección 2.1 —tablas (fuentes 1–3), JSON (fuente 4) e imágenes y texto libre (fuentes 5–6)—, lo que obliga a un enfoque de integración de datos heterogéneos, en línea con la definición de variedad de Laney (2001).
- **Veracidad (crítica):** es la V más sensible del proyecto, porque la pregunta de negocio depende de que la relación entre variables de proceso y defectos sea confiable; los sensores (fuente 2) y las inspecciones manuales (fuentes 5–6) son, precisamente, las fuentes con mayor riesgo de ruido, datos faltantes o subjetividad (desarrollado en la sección 2.3).
- **Valor (crítica):** es la V que justifica todo el proyecto, pues el fin último no es acumular datos sino generar el conocimiento accionable —qué parámetros ajustar y dónde reforzar inspección— descrito en la decisión esperada de la Semana 1.

### 2.3 Reto de veracidad y forma de detectarlo

**Problema de veracidad identificado:** los sensores de temperatura y velocidad de línea (fuente 2) pueden entregar lecturas erróneas por descalibración, ruido eléctrico o pérdida de conexión momentánea, generando valores atípicos (por ejemplo, picos de temperatura imposibles) o datos faltantes en ciertos intervalos de tiempo; de forma similar, la clasificación de una pieza como "defectuosa" en la inspección manual (fuentes 5–6) puede variar según el criterio subjetivo del operario de turno. Ambos casos contaminan la variable objetivo y las variables predictoras que el proyecto necesita relacionar (sección 2.2 de la Semana 1), lo que podría llevar a conclusiones incorrectas sobre qué factores realmente aumentan el riesgo de defecto.

**Cómo se detectaría (de forma concreta):**

1. **Reglas de rango y validación automática:** definir límites físicamente plausibles para cada variable de sensor (por ejemplo, temperatura entre 0 °C y 120 °C) y marcar como sospechoso todo registro fuera de ese rango.
2. **Detección estadística de valores atípicos:** calcular el puntaje z o el rango intercuartílico de cada variable de proceso por turno y señalar los registros que se desvíen de forma anómala del comportamiento habitual de la máquina.
3. **Verificación cruzada inspección vs. sensor:** comparar la tasa de defectos reportada por inspección manual (fuentes 5–6) contra la tasa estimada a partir de las variables de sensor (fuente 2) para el mismo lote; una discrepancia sistemática entre ambas fuentes es evidencia directa de un problema de veracidad en alguna de ellas.
4. **Monitoreo de completitud:** calcular el porcentaje de valores faltantes por sensor y por turno; un aumento súbito en ese porcentaje indica una falla de captura que debe corregirse antes de usar los datos en el análisis diagnóstico y predictivo.

---

## 3. Referencias bibliográficas

CORHUILA — Corporación Universitaria del Huila. (2026). *Ciencia de Datos · Semana 2 · Fundamentos de Big Data* [Material de curso]. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/02-week/01-session/

El Kharoua, R. (s.f.). *Predicting Manufacturing Defects Dataset* [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/rabieelkharoua/predicting-manufacturing-defects-dataset

Laney, D. (2001). *3D data management: Controlling data volume, velocity and variety* (META Group Research Note, Vol. 6, No. 70). META Group.

Syafrudin, M., Alfian, G., Fitriyani, N. L., & Rhee, J. (2018). Performance analysis of IoT-based sensor, big data processing, and machine learning model for real-time monitoring system in automotive manufacturing. *Sensors*, 18(9), 2946. https://doi.org/10.3390/s18092946
