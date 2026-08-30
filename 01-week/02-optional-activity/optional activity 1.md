# Actividad Semana 1 — Encuadra un proyecto de datos
## Calidad: Defectos de producción

**Programa:** Ingeniería Industrial | **Asignatura:** Ciencia de Datos | **Unidad:** 1 — Fundamentos de Ciencia de Datos y Big Data | **Periodo:** 2026-B | **Estudiante:** Angelica Vargas Zambrano

---

## 1. Marco de referencia y conceptos

### 1.1 Ciencia de datos

La ciencia de datos se define como un campo interdisciplinario que combina métodos científicos, estadística, programación y conocimiento del dominio para extraer valor y conocimiento a partir de los datos, con el propósito de apoyar la toma de decisiones (CORHUILA, 2026).

Dentro de esta disciplina resulta útil distinguir tres niveles, siguiendo la guía del curso (CORHUILA, 2026):

- **Dato:** un hecho aislado sin contexto (por ejemplo, "35 °C").
- **Información:** un dato situado en un contexto (por ejemplo, "la máquina 3 alcanzó 35 °C a las 2 p.m.").
- **Conocimiento:** un patrón accionable que permite tomar decisiones (por ejemplo, "temperaturas superiores a 33 °C generan falla en 1 hora").

Este tránsito de dato a conocimiento es precisamente el que se busca recorrer en un proyecto como el que se plantea en esta actividad: partir de variables del proceso productivo (dato) para llegar a un patrón que explique y anticipe los defectos (conocimiento).

### 1.2 Ciclo de vida de un proyecto de datos

De acuerdo con el material del curso (CORHUILA, 2026), un proyecto de ciencia de datos sigue un ciclo que va desde la **pregunta de negocio**, pasando por la **obtención de datos**, la **limpieza**, el **análisis**, el **modelado** y la **comunicación**, hasta llegar a la **decisión**. Formular correctamente la pregunta de negocio en esta primera etapa es crítico, porque de ella se derivan los datos que se necesitan y el tipo de análisis que resulta pertinente; esta misma lógica es la que estructura la presente actividad.

### 1.3 Tipos de analítica de datos

La literatura de analítica de negocios distingue clásicamente cuatro tipos de analítica, que responden a preguntas distintas sobre los datos:

- **Analítica descriptiva:** responde a "¿qué ocurrió?", resumiendo datos históricos (por ejemplo, tasas de defecto por turno).
- **Analítica diagnóstica:** responde a "¿por qué ocurrió?", buscando relaciones causales o asociaciones entre variables del proceso y el resultado observado.
- **Analítica predictiva:** responde a "¿qué es probable que ocurra?", usando modelos estadísticos o de aprendizaje automático entrenados con datos históricos para estimar la probabilidad de eventos futuros.
- **Analítica prescriptiva:** responde a "¿qué se debería hacer?", recomendando acciones concretas a partir de los resultados de los modelos predictivos.

Esta tipología permite ubicar con precisión el tipo de análisis que necesita este proyecto: uno diagnóstico y predictivo, en la misma línea del enfoque que David y Firdaus (2024) aplicaron sobre este mismo problema de defectos de manufactura.

### 1.4 Analítica aplicada a la calidad y el control de defectos en manufactura

La aplicación de técnicas de aprendizaje automático al control de calidad en manufactura cuenta con respaldo empírico directo sobre el propio conjunto de datos de esta actividad. David y Firdaus (2024) entrenaron un modelo de clasificación K-Nearest Neighbor sobre el *Predicting Manufacturing Defects Dataset* para predecir la tasa de defectos a partir de variables del proceso productivo, obteniendo una exactitud (*accuracy*) del 86.41 % con la distancia de Minkowski y una partición 80/20 de los datos. Este resultado confirma que variables como la velocidad de línea, la temperatura, el turno o el proveedor —contempladas en el dataset seleccionado— tienen poder explicativo real sobre la ocurrencia de defectos, y que un enfoque diagnóstico-predictivo como el planteado en este proyecto es viable y está validado en la literatura académica.

---

## 2. Enunciado del proyecto

### 2.1 Pregunta de negocio

> **¿Qué factores del proceso productivo (velocidad de línea, temperatura, turno, proveedor) aumentan la probabilidad de que un producto salga defectuoso?**

Esta pregunta se formula para ser **clara y accionable**, condición de excelencia del criterio "Pregunta de negocio" de la rúbrica:

- **Es clara** porque delimita explícitamente el problema (defectos de producción), el contexto (proceso de manufactura) y las variables candidatas a explicarlo (velocidad de línea, temperatura, turno, proveedor), sin ambigüedad sobre qué se está preguntando.
- **Es accionable** porque su respuesta no es meramente descriptiva: identificar qué factores aumentan la probabilidad de defecto conduce directamente a una acción operativa posible (ajustar ese factor o reforzar inspección donde el riesgo es mayor), y es medible con los datos disponibles en el dataset seleccionado, es decir, es una pregunta que puede responderse y verificarse con evidencia.

### 2.2 Datos y fuentes

Para responder la pregunta se requieren datos estructurados del proceso productivo que registren, para cada lote o unidad producida, tanto las condiciones de operación como el resultado de calidad obtenido. Los datos identificados son **pertinentes** —criterio de excelencia de la rúbrica— porque corresponden exactamente a las variables que la pregunta de negocio necesita para ser respondida:

- **Variables de proceso (predictoras):** velocidad de línea, temperatura de operación, turno de trabajo y proveedor de materia prima, entre otras variables operativas registradas durante la producción.
- **Variables de resultado (objetivo):** tasa de defectos (indicador binario/continuo de si el producto salió defectuoso) y eficiencia de producción.

**Fuente:** *Predicting Manufacturing Defects Dataset* (El Kharoua, s.f.), publicado en Kaggle bajo la descripción "Insights into Factors Influencing Defect Rates and Production Efficiency" ("percepciones sobre los factores que influyen en las tasas de defectos y la eficiencia de producción"), lo que confirma su pertinencia directa para esta pregunta. La idoneidad de este conjunto de datos para tareas de predicción de defectos está además respaldada en la literatura académica: David y Firdaus (2024) utilizaron este mismo dataset para entrenar un modelo de clasificación K-Nearest Neighbor que predice la tasa de defectos a partir de las variables de proceso, alcanzando una exactitud (*accuracy*) del 86.41 %, lo que demuestra que las variables del dataset tienen, en efecto, poder explicativo sobre la ocurrencia de defectos y son adecuadas tanto para el análisis diagnóstico como predictivo que plantea este proyecto.

### 2.3 Decisión esperada

La decisión que habilita este análisis se formula de manera **concreta** —criterio de excelencia de la rúbrica—, evitando enunciados genéricos como "mejorar la calidad":

> **Con base en los factores de proceso identificados como significativos, (1) ajustar el o los parámetros de producción específicos (por ejemplo, reducir la velocidad de línea o mantener la temperatura dentro del rango asociado a menor tasa de defectos) en las condiciones donde el modelo indique mayor riesgo, y/o (2) reforzar la inspección de calidad de forma focalizada en los turnos, proveedores o rangos de operación con mayor probabilidad predicha de defecto**, en lugar de aplicar inspección uniforme a toda la producción.

Esta decisión es concreta porque especifica: **qué** se ajusta (parámetros puntuales del proceso), **dónde/cuándo** se actúa (turnos, proveedores o condiciones de mayor riesgo, no toda la planta por igual) y **con base en qué** se decide (el resultado cuantitativo del análisis diagnóstico y predictivo). El resultado del análisis no es un fin en sí mismo, sino el insumo directo para esta acción operativa, cerrando así el ciclo descrito en la sección 1.2 (de la pregunta de negocio a la decisión).

### 2.4 Tipo de analítica

El proyecto combina dos tipos de analítica (ver sección 1.3):

- **Analítica diagnóstica:** para entender *por qué* ocurren los defectos, es decir, qué relación existe entre las variables del proceso (velocidad, temperatura, turno, proveedor) y la tasa de defectos observada.
- **Analítica predictiva:** para estimar la *probabilidad* de que un producto resulte defectuoso dadas ciertas condiciones de proceso, lo que permitiría anticipar el riesgo antes de que el defecto ocurra y priorizar la inspección.

---

## 3. Referencias bibliográficas

CORHUILA — Corporación Universitaria del Huila. (2026). *Ciencia de Datos · Semana 1 · Introducción a la ciencia de datos* [Material de curso]. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/01-week/01-session/

David, M., & Firdaus, M. A. (2024). Defect rate prediction in manufacturing process using K-Nearest Neighbor algorithm. *International Journal of Informatics, Economics, Management and Science*, 3(2), 161–173. https://journal.stmikjayakarta.ac.id/index.php/ijiems/article/view/1599

El Kharoua, R. (s.f.). *Predicting Manufacturing Defects Dataset* [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/rabieelkharoua/predicting-manufacturing-defects-dataset
