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
