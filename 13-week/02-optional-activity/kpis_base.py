import pandas as pd

URL = ("https://raw.githubusercontent.com/curran/data/gh-pages/"
       "superstoreSales/superstoreSales.csv")

# ---------------------------------------------------------------
# 1) CARGA Y PREPARACIÓN
# ---------------------------------------------------------------
df = pd.read_csv(URL, encoding="mac_roman")
df.columns = (df.columns.str.strip().str.lower()
                        .str.replace(r"[\s\-]+", "_", regex=True))
df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")
df["region"] = df["region"].replace({"Prarie": "Prairie"})   # error de ortografía del archivo
df["anio"] = df["order_date"].dt.year
df["dias_envio"] = (df["ship_date"] - df["order_date"]).dt.days

# ---------------------------------------------------------------
# 2) VALORES BASE DE LOS 3 KPIs, POR AÑO
# ---------------------------------------------------------------
por_anio = df.groupby("anio").agg(ventas=("sales", "sum"),
                                  utilidad=("profit", "sum"),
                                  dias_envio_prom=("dias_envio", "mean"),
                                  lineas=("sales", "count"))
por_anio["margen_pct"] = por_anio["utilidad"] / por_anio["ventas"] * 100
por_anio["pct_envio_3dias"] = (df.assign(ok=df["dias_envio"] <= 3)
                                 .groupby("anio")["ok"].mean() * 100)

print("KPIs base por año:")
print(por_anio[["ventas", "margen_pct", "dias_envio_prom", "pct_envio_3dias"]]
      .round(2).to_string())

print("\nPromedio del margen 2009-2011:",
      round(por_anio.loc[2009:2011, "margen_pct"].mean(), 2), "%")

# ---------------------------------------------------------------
# 3) CAMPOS DISPONIBLES PARA LOS FILTROS
# ---------------------------------------------------------------
for campo in ["region", "product_category", "customer_segment", "ship_mode", "order_priority"]:
    print(f"\n{campo}: {sorted(df[campo].dropna().unique())}")
