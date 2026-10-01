# Ciencia de Datos · Semana 7 · Consultas SQL y pandas

**Caso:** Ventas y logística de una empresa de suministros de oficina
**Programa:** Ingeniería Industrial · **Unidad 2:** Modelamiento, transformación y conexión de datos
**Autor:** Angelica Vargas Zambrano · **GitHub:** [avargas-2024a-del](https://github.com/avargas-2024a-del) · **Periodo:** 2026-B
**Herramientas:** Python 3, pandas, SQLite (módulo `sqlite3`)

---

## Tabla de contenido

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Dataset](#2-dataset)
3. [Preparación de los datos y de la base de datos](#3-preparación-de-los-datos-y-de-la-base-de-datos)
4. [Consultas SQL](#4-consultas-sql)
5. [Equivalente en pandas (GROUP BY → groupby)](#5-equivalente-en-pandas-group-by--groupby)
6. [Conclusiones](#6-conclusiones)
7. [Cómo ejecutar el código](#7-cómo-ejecutar-el-código)
8. [Referencias](#8-referencias)

---

## 1. Descripción del proyecto

Esta guía de la Semana 7 pide, sobre un dataset público, escribir **tres consultas SQL** (una con `WHERE`, una con `JOIN` y una con `GROUP BY`), **reproducir la de `GROUP BY` en pandas** con `groupby` y **explicar qué responde cada consulta**.

Para cumplirlo se trabajó con el dataset **Superstore Sales** (ventas de una empresa de suministros de oficina en Canadá), el mismo del trabajo del Corte 2. Los datos se limpiaron con pandas, se organizaron en una **base de datos SQLite** con seis tablas (siguiendo el modelo entidad-relación del Corte 2) y se consultaron con SQL. Se usa SQLite porque viene incluido en Python (módulo `sqlite3`) y no requiere instalar ni configurar un servidor.

| Requisito de la guía | Dónde se cumple |
|---|---|
| Consulta SQL con `WHERE` | Consulta 1 (sección 4.1) |
| Consulta SQL con `JOIN` | Consulta 2 (sección 4.2) |
| Consulta SQL con `GROUP BY` | Consulta 3 (sección 4.3) |
| Equivalente de `GROUP BY` en pandas (`groupby`) | Sección 5 |
| Explicación de lo que responde cada consulta | Al final de cada consulta y en la sección 5 |

---

## 2. Dataset

| Característica | Detalle |
|---|---|
| **Nombre** | Superstore Sales (`superstoreSales.csv`) |
| **Fuente** | Repositorio público `curran/data` en GitHub, carpeta `superstoreSales` |
| **Enlace directo al CSV** | <https://raw.githubusercontent.com/curran/data/gh-pages/superstoreSales/superstoreSales.csv> |
| **Número de registros** | 8,399 (cada registro es una línea de pedido) |
| **Número de columnas** | 21 (originales) |
| **Periodo cubierto** | Pedidos entre el 1 de enero de 2009 y el 30 de diciembre de 2012 |
| **Tipo de información** | Ventas y logística: pedidos, prioridad, modo de envío, costos, utilidad, clientes, ubicación y producto |

**Columnas que se usan en las consultas** (nombres ya normalizados a `snake_case`):

| Columna | Tipo de dato | Descripción |
|---|---|---|
| `row_id` | texto (identificador) | Identificador único de cada línea de pedido. |
| `customer_name` | texto | Nombre del cliente. |
| `product_name` | texto | Nombre del producto. |
| `province` | texto | Provincia o territorio de destino. |
| `ship_mode` | texto | Modo de envío (Regular Air, Express Air, Delivery Truck). |
| `order_priority` | texto | Prioridad del pedido. |
| `customer_segment` | texto | Segmento del cliente: Consumer, Corporate, Home Office o Small Business. |
| `sales` | decimal | Valor de la venta. |
| `discount` | decimal | Descuento aplicado (fracción, por ejemplo 0.05 = 5 %). |
| `profit` | decimal | Utilidad de la línea (puede ser negativa). |

---

## 3. Preparación de los datos y de la base de datos

### 3.1 Carga y limpieza

El archivo no está codificado en UTF-8, por lo que se lee con `encoding="mac_roman"`. La limpieza es la misma del Corte 2: nombres de columnas en `snake_case`, texto sin espacios sobrantes, eliminación de duplicados (no se encontró ninguno), corrección de dos errores de ortografía (`Prarie` → `Prairie` y `Saskachewan` → `Saskatchewan`), imputación de los 63 nulos de `product_base_margin` con la mediana de su subcategoría y conversión de las fechas a tipo fecha.

```python
import sqlite3
import pandas as pd

URL = ("https://raw.githubusercontent.com/curran/data/gh-pages/"
       "superstoreSales/superstoreSales.csv")

df = pd.read_csv(URL, encoding="mac_roman")
print("Antes  -> filas y columnas:", df.shape, "| nulos:", df.isnull().sum().sum())

# Nombres de columnas en snake_case
df.columns = (df.columns.str.strip().str.lower()
                        .str.replace(r"[\s\-]+", "_", regex=True))

# Texto sin espacios sobrantes
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)

# Duplicados (ignorando el identificador de la línea)
df = df.drop_duplicates(subset=[c for c in df.columns if c != "row_id"])

# Errores de ortografía
df["region"] = df["region"].replace({"Prarie": "Prairie"})
df["province"] = df["province"].replace({"Saskachewan": "Saskatchewan"})

# Nulos: mediana del margen base por subcategoría
mediana = df.groupby("product_sub_category")["product_base_margin"].transform("median")
df["product_base_margin"] = df["product_base_margin"].fillna(mediana)

# Fechas como tipo fecha
df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")

print("Después -> filas y columnas:", df.shape, "| nulos:", df.isnull().sum().sum())
```

**Resultado:** antes, 8,399 filas × 21 columnas con 63 nulos; después, 8,399 filas × 21 columnas con 0 nulos.

### 3.2 Creación de la base de datos SQLite

Para poder usar `JOIN`, los datos se separan en **seis tablas** (el modelo del Corte 2): `categoria`, `cliente`, `provincia`, `modo_envio`, `producto` y `pedido`. Cada tabla de dimensión recibe una clave primaria numérica (`..._id`) y la tabla `pedido` guarda las claves foráneas que apuntan a ellas.

```python
def tabla_dim(columnas, id_col):
    """Crea una tabla sin repetidos y le agrega una clave primaria numérica."""
    t = df[columnas].drop_duplicates().reset_index(drop=True)
    t.insert(0, id_col, t.index + 1)
    return t

# Tablas de dimensión
d_categoria = tabla_dim(["product_category"], "categoria_id")
d_cliente   = tabla_dim(["customer_name"], "cliente_id")
d_provincia = tabla_dim(["province", "region"], "provincia_id")
d_modo      = tabla_dim(["ship_mode"], "modo_envio_id")
d_producto  = tabla_dim(["product_name", "product_sub_category", "product_category"], "producto_id")
d_producto  = d_producto.merge(d_categoria, on="product_category")

# Tabla de hechos: a cada línea se le asignan sus claves foráneas
pedido = (df.merge(d_cliente,   on="customer_name")
            .merge(d_producto[["producto_id", "product_name"]], on="product_name")
            .merge(d_provincia, on=["province", "region"])
            .merge(d_modo,      on="ship_mode"))

pedido = pedido.rename(columns={
    "order_id": "numero_pedido", "order_priority": "prioridad",
    "customer_segment": "segmento_cliente", "product_container": "empaque",
    "order_quantity": "cantidad", "unit_price": "precio_unitario",
    "discount": "descuento", "sales": "ventas", "profit": "utilidad",
    "shipping_cost": "costo_envio", "product_base_margin": "margen_base"})
pedido["fecha_pedido"] = pedido["order_date"].dt.strftime("%Y-%m-%d")
pedido["fecha_envio"] = pedido["ship_date"].dt.strftime("%Y-%m-%d")
pedido = pedido[["row_id", "cliente_id", "producto_id", "provincia_id", "modo_envio_id",
                 "numero_pedido", "fecha_pedido", "fecha_envio", "prioridad",
                 "segmento_cliente", "empaque", "cantidad", "precio_unitario",
                 "descuento", "ventas", "utilidad", "costo_envio", "margen_base"]]

# Nombres finales de las demás tablas
categoria = d_categoria.rename(columns={"product_category": "nombre"})
cliente   = d_cliente.rename(columns={"customer_name": "nombre"})
provincia = d_provincia.rename(columns={"province": "nombre"})
modo      = d_modo.rename(columns={"ship_mode": "nombre"})
producto  = d_producto[["producto_id", "categoria_id", "product_name",
                        "product_sub_category"]].rename(
                columns={"product_name": "nombre", "product_sub_category": "subcategoria"})

# Base de datos SQLite en memoria (no crea ningún archivo)
con = sqlite3.connect(":memory:")
tablas = {"categoria": categoria, "cliente": cliente, "provincia": provincia,
          "modo_envio": modo, "producto": producto, "pedido": pedido}
for nombre, tabla in tablas.items():
    tabla.to_sql(nombre, con, index=False)
    print(f"{nombre:<11} -> {len(tabla):>5} filas")
```

**Resultado:**

| Tabla | Filas | Contenido |
|---|---:|---|
| `categoria` | 3 | Categorías de producto. |
| `cliente` | 795 | Clientes. |
| `provincia` | 13 | Provincias y territorios con su región. |
| `modo_envio` | 3 | Modos de envío. |
| `producto` | 1,263 | Productos con su categoría y subcategoría. |
| `pedido` | 8,399 | Líneas de pedido con sus claves foráneas, fechas, ventas, utilidad, etc. |

Relaciones usadas en los `JOIN`: `pedido.cliente_id → cliente.cliente_id`, `pedido.producto_id → producto.producto_id` y `pedido.provincia_id → provincia.provincia_id`.

---

## 4. Consultas SQL

Todas las consultas se ejecutan con `pd.read_sql_query(consulta, con)`, que corre el SQL en SQLite y devuelve el resultado como un DataFrame.

### 4.1 Consulta 1 — Con `WHERE`

**Pregunta:** ¿Cuáles son las 10 líneas de pedido con mayores pérdidas entre las ventas grandes (más de 5,000)?

```sql
SELECT row_id, fecha_pedido, prioridad, ventas, descuento, utilidad
FROM pedido
WHERE utilidad < 0 AND ventas > 5000
ORDER BY utilidad ASC
LIMIT 10;
```

```python
consulta_1 = """
SELECT row_id, fecha_pedido, prioridad, ventas, descuento, utilidad
FROM pedido
WHERE utilidad < 0 AND ventas > 5000
ORDER BY utilidad ASC
LIMIT 10;
"""
r1 = pd.read_sql_query(consulta_1, con)
print(r1.to_string(index=False))

# Complemento: cuántas líneas cumplen el filtro y cuánto suman sus pérdidas
complemento_1 = """
SELECT COUNT(*)                 AS lineas_con_perdida,
       ROUND(SUM(utilidad), 2)  AS perdida_total,
       ROUND(AVG(descuento), 4) AS descuento_prom
FROM pedido
WHERE utilidad < 0 AND ventas > 5000;
"""
print(pd.read_sql_query(complemento_1, con).to_string(index=False))
```

**Resultado:**

| row_id | fecha_pedido | prioridad | ventas | descuento | utilidad |
|---:|---|---|---:|---:|---:|
| 5213 | 2009-03-10 | Low | 18,888.00 | 0.09 | -14,140.70 |
| 6076 | 2009-10-17 | Medium | 19,707.20 | 0.04 | -12,558.00 |
| 7223 | 2011-11-27 | Not Specified | 21,366.51 | 0.00 | -11,984.40 |
| 3284 | 2009-01-06 | Critical | 26,133.39 | 0.04 | -11,053.60 |
| 3048 | 2010-09-12 | Not Specified | 19,014.24 | 0.06 | -10,263.66 |
| 8368 | 2012-12-12 | Not Specified | 24,391.16 | 0.04 | -9,611.91 |
| 3575 | 2012-10-02 | Not Specified | 13,698.96 | 0.05 | -9,078.94 |
| 3917 | 2011-07-07 | High | 9,172.32 | 0.06 | -8,570.45 |
| 4942 | 2010-01-18 | High | 10,380.34 | 0.05 | -8,389.47 |
| 4117 | 2009-07-28 | Critical | 13,070.20 | 0.07 | -6,923.60 |

Complemento: **193 líneas** cumplen el filtro, con una pérdida total de **-301,168.89** y un descuento promedio de **0.0488** (4.88 %).

**Qué responde y hallazgo:** la consulta usa `WHERE` para quedarse solo con las líneas que tienen pérdida (`utilidad < 0`) **y** una venta mayor a 5,000, y `ORDER BY ... LIMIT 10` para mostrar las 10 peores. La mayor pérdida fue de -14,140.70 en una venta de 18,888.00 (línea 5213). En total, 193 ventas grandes terminaron en pérdida, y entre ellas hay pedidos de todas las prioridades, no solo de una. Además, el descuento promedio de esas líneas es bajo (4.88 %), por lo que los datos no indican que los descuentos expliquen estas pérdidas; la causa no se puede saber solo con este dataset (podría estar en costos u otras variables).

### 4.2 Consulta 2 — Con `JOIN`

**Pregunta:** ¿Quiénes son los clientes, y qué producto y provincia corresponden a las 5 líneas de pedido con mayor valor de venta?

La tabla `pedido` solo guarda números (claves foráneas). Para ver los **nombres** hay que unirla con `cliente`, `producto` y `provincia`.

```sql
SELECT p.row_id,
       c.nombre  AS cliente,
       pr.nombre AS producto,
       pv.nombre AS provincia,
       p.ventas
FROM pedido AS p
JOIN cliente   AS c  ON p.cliente_id   = c.cliente_id
JOIN producto  AS pr ON p.producto_id  = pr.producto_id
JOIN provincia AS pv ON p.provincia_id = pv.provincia_id
ORDER BY p.ventas DESC
LIMIT 5;
```

```python
consulta_2 = """
SELECT p.row_id,
       c.nombre  AS cliente,
       pr.nombre AS producto,
       pv.nombre AS provincia,
       p.ventas
FROM pedido AS p
JOIN cliente   AS c  ON p.cliente_id   = c.cliente_id
JOIN producto  AS pr ON p.producto_id  = pr.producto_id
JOIN provincia AS pv ON p.provincia_id = pv.provincia_id
ORDER BY p.ventas DESC
LIMIT 5;
"""
r2 = pd.read_sql_query(consulta_2, con)
print(r2.to_string(index=False))
```

**Resultado:**

| row_id | cliente | producto | provincia | ventas |
|---:|---|---|---|---:|
| 4190 | Emily Phan | Polycom ViewStation™ ISDN Videoconferencing Unit | New Brunswick | 89,061.05 |
| 452 | Jasper Cacioppo | Polycom ViewStation™ ISDN Videoconferencing Unit | Quebec | 45,923.76 |
| 4264 | Craig Carreira | Polycom ViewStation™ ISDN Videoconferencing Unit | Saskatchewan | 41,343.21 |
| 2026 | Dennis Kane | Canon imageCLASS 2200 Advanced Copier | Quebec | 33,367.85 |
| 4629 | Karen Carlisle | Canon Image Class D660 Copier | British Columbia | 29,884.60 |

**Qué responde y hallazgo:** el `JOIN` combina tres tablas a través de sus claves (`cliente_id`, `producto_id`, `provincia_id`) para convertir los números de `pedido` en información legible: quién compró, qué compró y a dónde se envió. Los resultados muestran que la venta más grande del dataset fue de 89,061.05 (Emily Phan, New Brunswick), que **las tres ventas más altas corresponden al mismo producto** (la unidad de videoconferencia Polycom ViewStation) en tres provincias distintas, y que las otras dos son copiadoras Canon. Es decir, los pedidos de mayor valor se concentran en equipos de videoconferencia y copiado.

### 4.3 Consulta 3 — Con `GROUP BY`

**Pregunta:** ¿Cuántas líneas de pedido, cuántas ventas, cuánta utilidad, qué margen y qué descuento promedio tiene cada segmento de cliente?

```sql
SELECT segmento_cliente,
       COUNT(*)                                       AS lineas,
       ROUND(SUM(ventas), 2)                          AS ventas_totales,
       ROUND(SUM(utilidad), 2)                        AS utilidad_total,
       ROUND(AVG(descuento), 4)                       AS descuento_prom,
       ROUND(100.0 * SUM(utilidad) / SUM(ventas), 2)  AS margen_pct
FROM pedido
GROUP BY segmento_cliente
ORDER BY utilidad_total DESC;
```

```python
consulta_3 = """
SELECT segmento_cliente,
       COUNT(*)                                       AS lineas,
       ROUND(SUM(ventas), 2)                          AS ventas_totales,
       ROUND(SUM(utilidad), 2)                        AS utilidad_total,
       ROUND(AVG(descuento), 4)                       AS descuento_prom,
       ROUND(100.0 * SUM(utilidad) / SUM(ventas), 2)  AS margen_pct
FROM pedido
GROUP BY segmento_cliente
ORDER BY utilidad_total DESC;
"""
r3 = pd.read_sql_query(consulta_3, con)
print(r3.to_string(index=False))
```

**Resultado:**

| segmento_cliente | lineas | ventas_totales | utilidad_total | descuento_prom | margen_pct |
|---|---:|---:|---:|---:|---:|
| Corporate | 3,076 | 5,498,904.88 | 599,746.00 | 0.0498 | 10.91 |
| Home Office | 2,032 | 3,564,763.88 | 318,354.03 | 0.0494 | 8.93 |
| Small Business | 1,642 | 2,788,320.99 | 315,708.01 | 0.0494 | 11.32 |
| Consumer | 1,649 | 3,063,611.08 | 287,959.94 | 0.0499 | 9.40 |

**Qué responde y hallazgo:** `GROUP BY segmento_cliente` agrupa las 8,399 líneas en los cuatro segmentos y, para cada uno, calcula con funciones de agregación el número de líneas (`COUNT`), las ventas y la utilidad (`SUM`) y el descuento promedio (`AVG`). El segmento **Corporate** es el más grande: tiene 3,076 líneas, 5,498,904.88 en ventas y 599,746.00 de utilidad, cerca del 39 % de la utilidad total (1,521,767.98). Sin embargo, el mayor **margen** lo tiene Small Business (11.32 %), seguido de Corporate (10.91 %), mientras que Home Office (8.93 %) tiene el más bajo. El descuento promedio es casi igual en los cuatro segmentos (entre 4.94 % y 4.99 %), por lo que las diferencias de margen no parecen venir del descuento.

---

## 5. Equivalente en pandas (GROUP BY → groupby)

La Consulta 3 se reproduce en pandas con `groupby` y `agg`. La correspondencia entre SQL y pandas es la siguiente:

| SQL | pandas |
|---|---|
| `FROM pedido` | DataFrame `pedido` |
| `GROUP BY segmento_cliente` | `.groupby("segmento_cliente")` |
| `COUNT(*)` | `("row_id", "count")` |
| `SUM(ventas)` | `("ventas", "sum")` |
| `AVG(descuento)` | `("descuento", "mean")` |
| `ROUND(..., 2)` | `.round(...)` |
| `ORDER BY utilidad_total DESC` | `.sort_values("utilidad_total", ascending=False)` |

```python
g = (pedido.groupby("segmento_cliente")
           .agg(lineas=("row_id", "count"),
                ventas_totales=("ventas", "sum"),
                utilidad_total=("utilidad", "sum"),
                descuento_prom=("descuento", "mean")))

g["margen_pct"] = g["utilidad_total"] / g["ventas_totales"] * 100

g = (g.round({"ventas_totales": 2, "utilidad_total": 2,
              "descuento_prom": 4, "margen_pct": 2})
      .sort_values("utilidad_total", ascending=False)
      .reset_index())

print(g.to_string(index=False))

# Verificación: el resultado de pandas debe ser igual al de SQL
pd.testing.assert_frame_equal(r3, g, check_dtype=False)
print("\nEl resultado de pandas es IGUAL al de la consulta SQL.")
```

**Resultado:**

| segmento_cliente | lineas | ventas_totales | utilidad_total | descuento_prom | margen_pct |
|---|---:|---:|---:|---:|---:|
| Corporate | 3,076 | 5,498,904.88 | 599,746.00 | 0.0498 | 10.91 |
| Home Office | 2,032 | 3,564,763.88 | 318,354.03 | 0.0494 | 8.93 |
| Small Business | 1,642 | 2,788,320.99 | 315,708.01 | 0.0494 | 11.32 |
| Consumer | 1,649 | 3,063,611.08 | 287,959.94 | 0.0499 | 9.40 |

**Qué responde y hallazgo:** responde la misma pregunta que la Consulta 3 y entrega **exactamente los mismos valores**, lo que se comprobó con `assert_frame_equal`: si hubiera alguna diferencia, el programa mostraría un error. Esto confirma que `groupby` + `agg` de pandas equivale a `GROUP BY` + funciones de agregación de SQL. La diferencia es de estilo: en SQL se escribe en una sola sentencia declarativa y en pandas se encadenan métodos sobre un DataFrame (y el margen se calcula en un paso aparte).

---

## 6. Conclusiones

- Se escribieron **tres consultas SQL** que cumplen lo pedido: una con `WHERE` (pérdidas en ventas grandes), una con `JOIN` (nombres de cliente, producto y provincia de las mayores ventas) y una con `GROUP BY` (resumen por segmento de cliente).
- La consulta de `GROUP BY` se **reprodujo en pandas** con `groupby` y se verificó que el resultado es idéntico.
- Para poder usar `JOIN` se organizó el dataset en seis tablas relacionadas por claves primarias y foráneas, lo que muestra para qué sirve el modelo entidad-relación.
- Los hallazgos describen lo que muestran los datos: 193 ventas grandes con pérdida, las tres mayores ventas de un mismo producto de videoconferencia, y un segmento Corporate con mayor utilidad total pero con un margen menor que el de Small Business. No se afirman causas que el dataset no permite comprobar.

---

## 7. Cómo ejecutar el código

1. Instalar pandas (`sqlite3` ya viene incluido en Python):

```bash
pip install pandas
```

2. Copiar los bloques de código **Python** de las secciones 3, 4 y 5 en un archivo (por ejemplo `consultas.py`) o en un cuaderno de Jupyter, en el mismo orden en que aparecen. Los bloques marcados como `sql` son la versión legible de cada consulta; la misma consulta ya está incluida dentro del código Python.
3. Ejecutar:

```bash
python consultas.py
```

El código descarga el CSV desde la URL de la sección 2, por lo que requiere conexión a internet. La base de datos se crea en memoria y no genera archivos. Los resultados de este documento se obtuvieron ejecutando ese mismo código.

---

## 8. Referencias

- Curran, M. (s. f.). *superstoreSales.csv* [Conjunto de datos]. Repositorio `curran/data`, GitHub. <https://raw.githubusercontent.com/curran/data/gh-pages/superstoreSales/superstoreSales.csv>
- Python Software Foundation. (s. f.). *sqlite3 — DB-API 2.0 interface for SQLite databases*. <https://docs.python.org/3/library/sqlite3.html>
- SQLite. (s. f.). *SQL As Understood By SQLite*. <https://www.sqlite.org/lang.html>
- The pandas development team. (s. f.). *Group by: split-apply-combine*. <https://pandas.pydata.org/docs/user_guide/groupby.html>
- The pandas development team. (s. f.). *pandas.read_sql_query*. <https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html>
- The pandas development team. (s. f.). *Comparison with SQL*. <https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html>
- The pandas development team. (s. f.). *pandas documentation*. <https://pandas.pydata.org/docs/>
- Corporación Universitaria del Huila – CORHUILA. (2026). *Guía de actividad práctica: Ciencia de Datos, Semana 7 · Consultas SQL y pandas*. Material de la asignatura.
