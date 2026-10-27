import pandas as pd
import matplotlib
matplotlib.use("Agg")                      # permite guardar el gráfico sin abrir ventana
import matplotlib.pyplot as plt

URL = ("https://raw.githubusercontent.com/curran/data/gh-pages/"
       "superstoreSales/superstoreSales.csv")

# ---------------------------------------------------------------
# 1) CARGA: la fecha del pedido se convierte en el índice
# ---------------------------------------------------------------
df = pd.read_csv(URL, encoding="mac_roman")
df.columns = (df.columns.str.strip().str.lower()
                        .str.replace(r"[\s\-]+", "_", regex=True))
df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")

ventas = df.set_index("order_date").sort_index()["sales"]

print("Registros:", len(ventas))
print("Tipo de índice:", type(ventas.index).__name__)
print("Rango de fechas:", ventas.index.min().date(), "->", ventas.index.max().date())
print("Nulos en ventas:", int(ventas.isnull().sum()))

# ---------------------------------------------------------------
# 2) AGREGACIÓN MENSUAL (resample) Y MEDIA MÓVIL (rolling)
# ---------------------------------------------------------------
mensual = ventas.resample("MS").sum()                  # MS = inicio de cada mes
media_3m = mensual.rolling(window=3).mean()            # media móvil de 3 meses
media_12m = mensual.rolling(window=12).mean()          # media móvil de 12 meses

tabla = pd.DataFrame({"ventas_mes": mensual,
                      "media_movil_3m": media_3m,
                      "media_movil_12m": media_12m}).round(2)

print("\nMeses en la serie:", len(mensual))
print("Meses sin ventas:", int((mensual == 0).sum()))
print("\nPrimeras filas:")
print(tabla.head(14).to_string())

# ---------------------------------------------------------------
# 3) APOYO PARA LA INTERPRETACIÓN
# ---------------------------------------------------------------
print("\nVentas por año:")
print(mensual.groupby(mensual.index.year).sum().round(2))

print("\nPromedio de ventas por mes del año (estacionalidad):")
print(mensual.groupby(mensual.index.month).mean().round(2))

print("\nMedia móvil de 12 meses al cierre de cada año:")
print(media_12m[media_12m.index.month == 12].round(2))

# ---------------------------------------------------------------
# 4) GRÁFICO: serie mensual + medias móviles
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(mensual.index, mensual / 1000, color="#9ca3af", marker="o",
        markersize=3.5, linewidth=1.2, label="Ventas mensuales")
ax.plot(media_3m.index, media_3m / 1000, color="#2563eb", linewidth=2.2,
        label="Media móvil 3 meses")
ax.plot(media_12m.index, media_12m / 1000, color="#dc2626", linewidth=2.8,
        label="Media móvil 12 meses")
ax.set_title("Ventas mensuales y media móvil (Superstore, 2009-2012)", fontsize=14, fontweight="bold")
ax.set_xlabel("Mes")
ax.set_ylabel("Ventas (miles)")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("grafico_serie_tiempo.svg")
print("\nGráfico guardado: grafico_serie_tiempo.svg")
