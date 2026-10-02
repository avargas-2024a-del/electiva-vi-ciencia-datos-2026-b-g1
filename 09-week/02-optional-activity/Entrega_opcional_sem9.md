# Ciencia de Datos · Semana 9 · Limpieza de un dataset

**Caso:** Pedidos de un restaurante de comida rápida
**Programa:** Ingeniería Industrial · **Unidad 2:** Modelamiento, transformación y conexión de datos
**Autor:** Angelica Vargas Zambrano · **GitHub:** [avargas-2024a-del](https://github.com/avargas-2024a-del) · **Periodo:** 2026-B
**Herramientas:** Python 3, pandas

---

## Tabla de contenido

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Dataset](#2-dataset)
3. [Diagnóstico: problemas de calidad encontrados](#3-diagnóstico-problemas-de-calidad-encontrados)
4. [Script de limpieza en pandas](#4-script-de-limpieza-en-pandas)
5. [Evidencia antes/después](#5-evidencia-antesdespués)
6. [Dimensiones de calidad mejoradas](#6-dimensiones-de-calidad-mejoradas)
7. [Conclusiones](#7-conclusiones)
8. [Referencias](#8-referencias)

---

## 1. Descripción del proyecto

Esta guía de la Semana 9 pide tomar un dataset con problemas de calidad y, con Python y pandas, **contar los nulos, eliminar o imputar los faltantes, quitar duplicados, corregir tipos y normalizar formatos de texto**, reportando el **antes y el después** (número de filas, nulos y duplicados) y comentando **dos dimensiones de calidad** que mejoraron.

Para cumplirlo se trabajó con un dataset público de **pedidos de un restaurante de comida rápida** (archivo `chipotle.tsv`), que tiene problemas reales: valores nulos, filas duplicadas, precios guardados como texto con el símbolo `$` y nombres de productos escritos de dos formas. No fue necesario "ensuciar" los datos: los problemas ya vienen en el archivo original.

| Requisito de la guía | Dónde se cumple |
|---|---|
| Contar nulos y eliminar/imputar faltantes | Secciones 3, 4 (paso 2.4) y 5 |
| Quitar duplicados | Secciones 3, 4 (paso 2.5) y 5 |
| Corregir tipos | Secciones 3, 4 (paso 2.3) y 5 |
| Normalizar formatos de texto | Secciones 3, 4 (pasos 2.1 y 2.2) y 5 |
| Reporte antes/después (filas, nulos, duplicados) | Sección 5 |
| Comentar 2 dimensiones de calidad mejoradas | Sección 6 |
| Script de limpieza en pandas | Sección 4 (y archivo `limpieza.py` de esta carpeta) |

---

## 2. Dataset

| Característica | Detalle |
|---|---|
| **Nombre** | Pedidos de comida rápida (`chipotle.tsv`) |
| **Fuente** | Repositorio público `justmarkham/DAT8` en GitHub (Data School), carpeta `data` |
| **Enlace directo al archivo** | <https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv> |
| **Formato** | TSV (valores separados por tabulaciones), se lee con `sep="\t"` |
| **Número de registros** | 4,622 (cada registro es una línea de un pedido) |
| **Número de columnas** | 5 |
| **Pedidos distintos** | 1,834 |
| **Tipo de información** | Pedidos: cantidad, producto, opciones elegidas y precio |

**Columnas del dataset original:**

| Columna | Tipo de dato (original) | Descripción |
|---|---|---|
| `order_id` | int64 | Número del pedido (un pedido puede tener varias líneas). |
| `quantity` | int64 | Cantidad de unidades del producto en esa línea. |
| `item_name` | texto | Nombre del producto (por ejemplo, *Chicken Bowl*). |
| `choice_description` | texto | Opciones elegidas para el producto (salsas, ingredientes, sabor de la bebida). |
| `item_price` | texto | Precio de la línea, escrito como texto con el símbolo `$` (por ejemplo, `$2.39 `). |

---

## 3. Diagnóstico: problemas de calidad encontrados

Antes de limpiar se revisó el dataset con `df.head()`, `df.dtypes`, `df.isnull().sum()` y `df.duplicated().sum()`. Estos son los problemas detectados:

| # | Problema | Evidencia | Requisito de la guía |
|---:|---|---|---|
| 1 | **Valores nulos** en `choice_description` | 1,246 nulos (26.96 % de las filas). En el archivo aparecen como el texto `NULL`, que pandas lee como valor faltante. | Nulos |
| 2 | **Filas duplicadas** | 59 filas completamente repetidas. | Duplicados |
| 3 | **Tipo incorrecto** en `item_price` | Es texto (`"$2.39 "`), con el símbolo `$` y un espacio al final en las 4,622 filas; no se puede sumar ni promediar. | Tipos |
| 4 | **Tipo poco adecuado** en `order_id` | Es un número, pero en realidad es un código identificador: no tiene sentido sumarlo ni promediarlo. | Tipos |
| 5 | **Formato de texto inconsistente** en `item_name` | 3 productos están escritos de dos formas, con guion y sin guion (por ejemplo, `Chips and Tomatillo-Green Chili Salsa` y `Chips and Tomatillo Green Chili Salsa`). Hay 50 nombres distintos, pero solo 47 productos reales. | Formatos de texto |

**Decisiones de limpieza justificadas:**

| Problema | Decisión | Justificación |
|---|---|---|
| Nulos en `choice_description` | **Imputar** con la etiqueta `"Sin opciones"` | Los 1,246 nulos pertenecen solo a 12 nombres de producto (papas, guacamole, salsas y agua) que **en ningún otro registro tienen opciones**. Es decir, el nulo significa "este producto no tiene opciones", no un dato perdido al azar. Eliminar esas filas habría borrado más de una cuarta parte de los registros (26.96 %). No se inventó ningún valor. |
| Duplicados | **Eliminar** las filas completamente repetidas (`drop_duplicates`) | Es lo que pide la guía. Hay una salvedad (ver sección 5): una fila repetida podría ser una línea que el cliente pidió dos veces a propósito; por eso se mide cuánto representan en ventas. |
| `item_price` como texto | Quitar `$` y espacios y convertir a `float64` | Permite sumar y promediar precios. |
| `order_id` | Convertir a `string` | Es un identificador, no una cantidad con la que se opere. |
| `quantity` | Pasar a `int32` | Son números enteros pequeños (máximo 15); ahorra memoria. |
| Nombres con y sin guion | Reemplazar el guion por un espacio | Une las variantes de un mismo producto. No se unieron nombres parecidos pero distintos (como `Canned Soda` y `Canned Soft Drink`), porque con estos datos no se puede asegurar que sean el mismo producto. |

---

## 4. Script de limpieza en pandas

El mismo script está en el archivo [`limpieza.py`](limpieza.py) de esta carpeta. Al ejecutarlo imprime el estado **antes**, el estado **después** y la comparación.

```python
import pandas as pd

URL = ("https://raw.githubusercontent.com/justmarkham/DAT8/master/"
       "data/chipotle.tsv")


def resumen(d, etapa):
    """Métricas de calidad: filas, columnas, nulos y duplicados."""
    return {"Etapa": etapa,
            "Filas": len(d),
            "Columnas": d.shape[1],
            "Nulos": int(d.isnull().sum().sum()),
            "Duplicados": int(d.duplicated().sum())}


# ---------------------------------------------------------------
# 1) CARGA Y ESTADO INICIAL (ANTES)
# ---------------------------------------------------------------
df = pd.read_csv(URL, sep="\t")      # el texto "NULL" del archivo se lee como nulo
antes = df.copy()

print("=== ANTES ===")
print(df.head(), "\n")
print(df.dtypes, "\n")
print("Nulos por columna:")
print(df.isnull().sum(), "\n")
print("Filas duplicadas:", df.duplicated().sum())
print("Nombres de producto distintos:", df["item_name"].nunique())

# ---------------------------------------------------------------
# 2) LIMPIEZA
# ---------------------------------------------------------------
# 2.1 Normalizar formatos de texto: quitar espacios sobrantes
for col in ["item_name", "choice_description", "item_price"]:
    df[col] = (df[col].astype("string")
                      .str.strip()
                      .str.replace(r"\s+", " ", regex=True))

# 2.2 Unificar nombres de producto escritos de dos formas (con y sin guion)
df["item_name"] = df["item_name"].str.replace("-", " ", regex=False)

# 2.3 Corregir tipos: el precio está como texto ("$2.39") y debe ser número
df["item_price"] = (df["item_price"].str.replace("$", "", regex=False)
                                    .astype("float64"))
df["order_id"] = df["order_id"].astype("string")      # es un código, no se suma
df["quantity"] = df["quantity"].astype("int32")

# 2.4 Nulos: en choice_description el nulo significa "sin opciones" (por ejemplo,
#     papas o agua), así que se reemplaza por una etiqueta explícita
df["choice_description"] = df["choice_description"].fillna("Sin opciones")

# 2.5 Duplicados: se eliminan las filas completamente repetidas
duplicadas = df[df.duplicated()]
df = df.drop_duplicates().reset_index(drop=True)

# ---------------------------------------------------------------
# 3) ESTADO FINAL (DESPUÉS) Y COMPARACIÓN
# ---------------------------------------------------------------
print("\n=== DESPUÉS ===")
print(df.head(), "\n")
print(df.dtypes, "\n")
print("Nulos por columna:")
print(df.isnull().sum(), "\n")
print("Filas duplicadas:", df.duplicated().sum())
print("Nombres de producto distintos:", df["item_name"].nunique())

comparacion = pd.DataFrame([resumen(antes, "ANTES"), resumen(df, "DESPUÉS")])
print("\n=== COMPARACIÓN ===")
print(comparacion.to_string(index=False))

# Evidencia adicional para la explicación
print("\nVentas totales antes  :", round(antes["item_price"].str.replace("$", "", regex=False).str.strip().astype(float).sum(), 2))
print("Ventas totales después:", round(df["item_price"].sum(), 2))
print("Ventas de las filas duplicadas eliminadas:", round(duplicadas["item_price"].sum(), 2))
print("Pedidos distintos antes/después:", antes["order_id"].nunique(), "/", df["order_id"].nunique())
print("% de nulos en choice_description antes:",
      round(antes["choice_description"].isnull().mean() * 100, 2), "%")
print("\nVariantes unificadas (antes -> después):")
for v in ["Chips and Tomatillo-Green Chili Salsa", "Chips and Tomatillo-Red Chili Salsa",
          "Chips and Roasted Chili-Corn Salsa"]:
    print(f"  {v}  ->  {v.replace('-', ' ')}")
print("\nProductos sin opciones (los que tenían nulos):")
print(df.loc[df["choice_description"] == "Sin opciones", "item_name"].value_counts())
```

---

## 5. Evidencia antes/después

### 5.1 Resumen de calidad

Resultado de la tabla `COMPARACIÓN` que imprime el script:

```text
  Etapa  Filas  Columnas  Nulos  Duplicados
  ANTES   4622         5   1246          59
DESPUÉS   4563         5      0           0
```

| Métrica | ANTES | DESPUÉS |
|---|---:|---:|
| **Filas** | 4,622 | 4,563 |
| Columnas | 5 | 5 |
| **Nulos (total)** | 1,246 | 0 |
| **Duplicados** | 59 | 0 |
| Nombres de producto distintos | 50 | 47 |
| Pedidos distintos | 1,834 | 1,834 |
| Ventas totales (suma de `item_price`) | 34,500.16 | 34,177.25 |

Las 59 filas eliminadas sumaban **322.91** en ventas (aprox. 0.94 % del total). Los 1,834 pedidos distintos se mantienen: la limpieza no eliminó ningún pedido completo.

### 5.2 Nulos por columna

| Columna | Nulos ANTES | Nulos DESPUÉS |
|---|---:|---:|
| `order_id` | 0 | 0 |
| `quantity` | 0 | 0 |
| `item_name` | 0 | 0 |
| `choice_description` | 1,246 | 0 |
| `item_price` | 0 | 0 |

### 5.3 Tipos de datos

| Columna | Tipo ANTES | Tipo DESPUÉS |
|---|---|---|
| `order_id` | int64 | string |
| `quantity` | int64 | int32 |
| `item_name` | texto | string |
| `choice_description` | texto | string |
| `item_price` | texto (`"$2.39 "`) | float64 (`2.39`) |

### 5.4 Muestra de filas

**ANTES** (las primeras 5 filas):

| order_id | quantity | item_name | choice_description | item_price |
|---:|---:|---|---|---|
| 1 | 1 | Chips and Fresh Tomato Salsa | NaN | `$2.39 ` |
| 1 | 1 | Izze | [Clementine] | `$3.39 ` |
| 1 | 1 | Nantucket Nectar | [Apple] | `$3.39 ` |
| 1 | 1 | Chips and Tomatillo-Green Chili Salsa | NaN | `$2.39 ` |
| 2 | 2 | Chicken Bowl | [Tomatillo-Red Chili Salsa (Hot), [Black Beans, Rice, Cheese, Sour Cream]] | `$16.98 ` |

**DESPUÉS** (las mismas 5 filas):

| order_id | quantity | item_name | choice_description | item_price |
|---:|---:|---|---|---:|
| 1 | 1 | Chips and Fresh Tomato Salsa | Sin opciones | 2.39 |
| 1 | 1 | Izze | [Clementine] | 3.39 |
| 1 | 1 | Nantucket Nectar | [Apple] | 3.39 |
| 1 | 1 | Chips and Tomatillo Green Chili Salsa | Sin opciones | 2.39 |
| 2 | 2 | Chicken Bowl | [Tomatillo-Red Chili Salsa (Hot), [Black Beans, Rice, Cheese, Sour Cream]] | 16.98 |

### 5.5 Ejemplo de filas duplicadas eliminadas

En el pedido 103, la fila 234 y la fila 238 son idénticas: `Steak Burrito`, cantidad 1, mismas opciones y precio `$11.75`. Lo mismo ocurre en el pedido 108 con dos líneas de `Canned Soda` (`[Mountain Dew]`, `$1.09`). Después de la limpieza queda una sola de cada una.

**Salvedad:** el dataset no permite saber si una fila repetida es un error de registro o un producto que el cliente pidió dos veces como líneas separadas. Se eliminaron porque la guía pide quitar duplicados, y se informa su peso en las ventas (322.91, cerca del 0.94 %) para que se pueda valorar el impacto.

### 5.6 Variantes de nombre unificadas

| Antes | Después |
|---|---|
| `Chips and Tomatillo-Green Chili Salsa` | `Chips and Tomatillo Green Chili Salsa` |
| `Chips and Tomatillo-Red Chili Salsa` | `Chips and Tomatillo Red Chili Salsa` |
| `Chips and Roasted Chili-Corn Salsa` | `Chips and Roasted Chili Corn Salsa` |

---

## 6. Dimensiones de calidad mejoradas

### 6.1 Completitud

**Qué mide:** si los datos que deberían estar, están. Una columna incompleta dificulta el análisis, porque muchas funciones omiten o fallan con valores faltantes.

**Qué se mejoró:** `choice_description` pasó de tener **1,246 nulos (26.96 %)** a tener **0 nulos (0 %)**, y el total de nulos del dataset pasó de 1,246 a 0.

**Cómo se hizo y por qué es válido:** no se rellenó con valores inventados. Al revisar los datos se vio que esos nulos corresponden solo a productos que no tienen opciones para elegir (papas, guacamole, salsas y agua), por lo que el valor faltante en realidad significa "sin opciones". Se reemplazó por la etiqueta explícita `"Sin opciones"`, que conserva esa información y permite agrupar y filtrar sin errores. Con esto se evitó eliminar más del 26 % de las filas.

### 6.2 Consistencia

**Qué mide:** si un mismo dato se escribe siempre de la misma forma en todo el dataset. Si no, un mismo producto aparece como si fueran varios y los conteos y sumas quedan repartidos.

**Qué se mejoró:** los nombres de producto pasaron de **50 variantes a 47 productos distintos**, al unificar los 3 que estaban escritos con y sin guion. Además, `item_price` pasó de texto con `$` y espacios a un número uniforme (`float64`), y se quitaron los espacios sobrantes de los textos.

**Ejemplo del efecto:** antes, `Chips and Tomatillo Green Chili Salsa` aparecía en 43 filas y `Chips and Tomatillo-Green Chili Salsa` en otras 31, como si fueran dos productos distintos; ahora ambos cuentan como uno solo, con 74 líneas. Así, un conteo de ventas por producto ya no subestima ese producto. También se pueden sumar los precios, lo que antes era imposible por ser texto.

---

## 7. Conclusiones

- Se limpió el dataset de pedidos con pandas cubriendo todo lo que pide la guía: **nulos** (1,246 → 0), **duplicados** (59 → 0), **tipos** (precio de texto a número, identificador a texto) y **formatos de texto** (50 → 47 nombres de producto).
- El **antes y el después** quedaron documentados con filas (4,622 → 4,563), nulos, duplicados, tipos, una muestra de filas y ejemplos concretos.
- Se mejoraron y explicaron dos dimensiones de calidad: **completitud** (el nulo se interpretó según su significado y no se inventaron datos) y **consistencia** (un mismo producto se escribe de una sola forma).
- Como limitación, no se puede asegurar que todas las filas duplicadas fueran errores de registro; por eso se informó su peso en las ventas (322.91, cerca del 0.94 % del total) y no se tocó ningún pedido completo (los 1,834 pedidos se mantienen).

---

## 8. Referencias

- Markham, K. (s. f.). *chipotle.tsv* [Conjunto de datos]. Repositorio `justmarkham/DAT8`, GitHub (Data School). <https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv>
- The pandas development team. (s. f.). *Working with missing data*. <https://pandas.pydata.org/docs/user_guide/missing_data.html>
- The pandas development team. (s. f.). *pandas.DataFrame.drop_duplicates*. <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html>
- The pandas development team. (s. f.). *Working with text data*. <https://pandas.pydata.org/docs/user_guide/text.html>
- The pandas development team. (s. f.). *pandas.DataFrame.astype*. <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html>
- The pandas development team. (s. f.). *pandas documentation*. <https://pandas.pydata.org/docs/>
- Corporación Universitaria del Huila – CORHUILA. (2026). *Guía de actividad práctica: Ciencia de Datos, Semana 9 · Limpieza de un dataset*. Material de la asignatura.
