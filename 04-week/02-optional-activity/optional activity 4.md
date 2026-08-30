# Actividad Semana 4 — Tipos de analítica y ética
## Calidad: Defectos de producción

**Programa:** Ingeniería Industrial | **Asignatura:** Ciencia de Datos | **Unidad:** 1 — Fundamentos de Ciencia de Datos y Big Data | **Periodo:** 2026-B | **Estudiante:** Angelica Vargas Zambrano

Esta actividad da continuidad al proyecto de las Semanas 1 a 3 (*Calidad — Defectos de producción*), cuya pregunta de negocio es: **¿qué factores del proceso (velocidad de línea, temperatura, turno, proveedor) aumentan la probabilidad de que un producto salga defectuoso?**

---

## 1. Marco de referencia y conceptos

### 1.1 Los cuatro tipos de analítica

La madurez analítica de un proyecto de datos avanza de forma progresiva a través de cuatro niveles, cada uno de los cuales responde a una pregunta distinta y aporta mayor valor a costa de requerir más datos y técnicas más sofisticadas (CORHUILA, 2026):

| Tipo | Pregunta que responde | Ejemplo general |
|---|---|---|
| **Descriptiva** | ¿Qué pasó? | Reporte de producción mensual |
| **Diagnóstica** | ¿Por qué pasó? | Análisis de causas de fallas |
| **Predictiva** | ¿Qué pasará? | Estimación de demanda futura |
| **Prescriptiva** | ¿Qué debo hacer? | Recomendaciones de niveles de inventario |

### 1.2 Aprendizaje supervisado y no supervisado

El aprendizaje automático permite que un modelo identifique patrones en los datos para predecir o clasificar, sin necesidad de programar reglas explícitas (CORHUILA, 2026). Dentro de este campo, Jordan y Mitchell (2015) distinguen los dos paradigmas centrales: el **aprendizaje supervisado**, en el que el modelo aprende a partir de ejemplos ya etiquetados con la respuesta correcta (por ejemplo, lotes ya marcados como defectuosos o no) para luego predecir o clasificar casos nuevos; y el **aprendizaje no supervisado**, en el que el modelo identifica agrupaciones, patrones o estructuras ocultas en los datos sin que existan etiquetas previas. La elección entre uno y otro depende de si se dispone (o no) de una variable objetivo conocida para entrenar el modelo, criterio que se aplica en la sección 2.2 para decidir el tipo de aprendizaje más adecuado en las etapas predictiva y prescriptiva del proyecto.

### 1.3 Ética, sesgo y transparencia en ciencia de datos

Un proyecto de ciencia de datos responsable debe atender tres consideraciones éticas centrales: la **privacidad** de los datos personales, la **transparencia** en los procesos de toma de decisión, y el **sesgo (bias)**, entendido como la tendencia de un modelo a aprender y reproducir los sesgos presentes en sus datos de entrenamiento (CORHUILA, 2026). Mehrabi et al. (2021), en su revisión sistemática sobre sesgo y equidad en aprendizaje automático, documentan que estos sesgos no surgen únicamente de la composición de los datos, sino también de decisiones humanas previas incorporadas en las etiquetas (por ejemplo, criterios de evaluación inconsistentes entre distintas personas que etiquetan los mismos casos), y proponen mitigarlos mediante auditorías del proceso de etiquetado, métricas de desempeño desagregadas por subgrupo y supervisión humana antes de convertir la salida del modelo en una acción con consecuencias reales. Este marco es el que se aplica en la sección 2.3 al riesgo ético identificado en el proyecto.

---

## 2. Enunciado de la actividad

### 2.1 Cuatro preguntas sobre el caso, una por tipo de analítica

| Tipo de analítica | Pregunta sobre el caso (Calidad — Defectos de producción) |
|---|---|
| **Descriptiva** | ¿Cuál fue la tasa de defectos por turno y por proveedor durante el último periodo de producción? |
| **Diagnóstica** | ¿Por qué el turno nocturno presenta una tasa de defectos más alta que el turno diurno: se debe a la temperatura de operación, a la velocidad de línea o al proveedor de materia prima asignado a ese turno? |
| **Predictiva** | Dadas la velocidad de línea, la temperatura, el turno y el proveedor de un lote específico, ¿cuál es la probabilidad de que ese lote resulte defectuoso? |
| **Prescriptiva** | ¿Qué ajuste concreto de velocidad de línea y temperatura debería aplicarse en el turno y proveedor de mayor riesgo, y en qué condiciones conviene reforzar la inspección de calidad para minimizar la tasa de defectos? |

Cada pregunta corresponde de forma correcta a su tipo de analítica: la descriptiva se limita a resumir lo ya ocurrido; la diagnóstica busca explícitamente una causa ("por qué"); la predictiva estima la probabilidad de un evento futuro para un caso puntual; y la prescriptiva recomienda una acción concreta, sin quedarse en el diagnóstico o la predicción.

### 2.2 Aprendizaje supervisado o no supervisado para la predictiva y la prescriptiva

**Predictiva → aprendizaje supervisado.** El proyecto dispone, desde la Semana 1, de un dataset histórico (*Predicting Manufacturing Defects Dataset*, El Kharoua, s.f.) en el que cada lote ya está etiquetado con su resultado real de calidad (defectuoso / no defectuoso) junto con las variables de proceso. Esa etiqueta histórica es exactamente lo que el aprendizaje supervisado necesita (Jordan y Mitchell, 2015): un modelo de clasificación (por ejemplo, K-Nearest Neighbor, como el aplicado por David y Firdaus, 2024, sobre este mismo dataset) puede entrenarse con esos ejemplos etiquetados para predecir la probabilidad de defecto de un lote nuevo cuyas condiciones de proceso se conocen, pero cuyo resultado de calidad todavía no.

**Prescriptiva → apoyada en aprendizaje no supervisado, sobre la base del modelo supervisado anterior.** La recomendación de a qué turnos, proveedores o condiciones dirigir el ajuste de parámetros no requiere una etiqueta de "acción correcta" (esa etiqueta no existe en los datos), por lo que aquí conviene un enfoque no supervisado: un algoritmo de agrupamiento (*clustering*) sobre las combinaciones de velocidad, temperatura, turno y proveedor permitiría identificar de forma automática los grupos de condiciones de operación con mayor riesgo de defecto —según las probabilidades ya estimadas por el modelo supervisado de la etapa predictiva—, y sobre esos grupos priorizados se formula la recomendación de ajuste o de inspección reforzada. En otras palabras, la etapa prescriptiva de este proyecto combina la salida de un modelo supervisado (probabilidad de defecto) con una técnica no supervisada (agrupamiento de condiciones de riesgo) para decidir dónde actuar.

### 2.3 Riesgo ético o sesgo, y su mitigación

**Sesgo identificado:** la etiqueta "defectuoso / no defectuoso" de una parte de los datos históricos (en particular, la inspección manual de calidad, fuente identificada en la Semana 2) depende del criterio subjetivo del inspector de turno. Si, por ejemplo, los inspectores del turno nocturno aplican un criterio más estricto (o más laxo) que los del turno diurno —por cansancio, menor supervisión o distinto nivel de experiencia—, el modelo predictivo no aprenderá el verdadero efecto de las variables de proceso sobre la calidad, sino en parte el sesgo de quién inspeccionó cada lote. El riesgo ético concreto es que el modelo termine señalando un turno o un proveedor como "de mayor riesgo" no porque sus condiciones de proceso sean peores, sino porque fue evaluado con un criterio de inspección distinto, lo que podría derivar en decisiones operativas injustas (por ejemplo, sanciones o mayor presión sobre el personal de un turno específico) basadas en un sesgo de etiquetado y no en evidencia real del proceso (Mehrabi et al., 2021).

**Cómo mitigarlo (de forma concreta):**

1. **Estandarizar el criterio de inspección** entre turnos, mediante una guía o checklist único de defectos que reduzca la variabilidad humana en el etiquetado, siguiendo la recomendación de auditar el proceso de etiquetado de Mehrabi et al. (2021).
2. **Auditar el desempeño del modelo desagregado por turno y por proveedor** (no solo su exactitud global), para verificar si el modelo predice sistemáticamente más defectos en un turno específico incluso controlando por las variables de proceso, lo que sería evidencia directa de sesgo heredado del etiquetado.
3. **Mantener supervisión humana antes de actuar:** la recomendación prescriptiva (sección 2.2) debe revisarse por un responsable de calidad antes de convertirse en una acción sobre el turno o proveedor señalado, en línea con el principio de transparencia y de no automatizar decisiones con consecuencias sobre las personas sin revisión (CORHUILA, 2026).

---

## 3. Referencias bibliográficas

CORHUILA — Corporación Universitaria del Huila. (2026). *Ciencia de Datos · Semana 4 · Aplicaciones modernas de Big Data y ciencia de datos* [Material de curso]. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/04-week/01-session/

Jordan, M. I., & Mitchell, T. M. (2015). Machine learning: Trends, perspectives, and prospects. *Science*, 349(6245), 255–260. https://doi.org/10.1126/science.aaa8415

Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). A survey on bias and fairness in machine learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607
