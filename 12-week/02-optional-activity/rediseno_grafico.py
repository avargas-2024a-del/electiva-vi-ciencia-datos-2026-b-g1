import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

URL = ("https://raw.githubusercontent.com/curran/data/gh-pages/"
       "superstoreSales/superstoreSales.csv")

# ---------------------------------------------------------------
# 1) DATOS: ventas totales por año
# ---------------------------------------------------------------
df = pd.read_csv(URL, encoding="mac_roman")
df.columns = (df.columns.str.strip().str.lower()
                        .str.replace(r"[\s\-]+", "_", regex=True))
df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")

anual = df.groupby(df["order_date"].dt.year)["sales"].sum()
anios = [str(a) for a in anual.index]
millones = anual / 1_000_000

print("Ventas por año (millones):")
print(millones.round(2))

cambio_09_11 = (anual[2011] / anual[2009] - 1) * 100
cambio_11_12 = (anual[2012] / anual[2011] - 1) * 100
print(f"\nCambio 2009 -> 2011: {cambio_09_11:.1f} %")
print(f"Cambio 2011 -> 2012: {cambio_11_12:+.1f} %")

# ---------------------------------------------------------------
# 2) EVIDENCIA DEL PROBLEMA: cuánto exagera el eje truncado
# ---------------------------------------------------------------
BASE = 3.3                                    # el eje "antes" empieza aquí
real = anual[2009] / anual[2011]
visual = (millones[2009] - BASE) / (millones[2011] - BASE)
print(f"\nRazón real 2009 / 2011:           {real:.2f} veces")
print(f"Razón visual en el gráfico ANTES: {visual:.2f} veces")

# ---------------------------------------------------------------
# 3) GRÁFICO ANTES (mal hecho a propósito)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(anios, millones, color=["#ff0000", "#00ff00", "#0000ff", "#ffff00"])
ax.set_ylim(BASE, 4.3)                        # eje truncado
ax.set_title("Ventas")                        # título sin información
ax.grid(True, color="black", linewidth=1)     # cuadrícula pesada
fig.tight_layout()
fig.savefig("grafico_antes.svg")
plt.close(fig)

# ---------------------------------------------------------------
# 4) GRÁFICO DESPUÉS (rediseñado)
# ---------------------------------------------------------------
GRIS, ROJO = "#9ca3af", "#b91c1c"
colores = [GRIS, GRIS, ROJO, GRIS]            # solo el mínimo (2011) se resalta

fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(anios, millones, color=colores, width=0.6)
ax.set_ylim(0, 5)                             # el eje empieza en cero

for barra, valor in zip(barras, millones):    # etiquetas directas
    ax.text(barra.get_x() + barra.get_width() / 2, valor + 0.07,
            f"{valor:.2f}", ha="center", fontweight="bold")

ax.set_title(f"Las ventas cayeron {abs(cambio_09_11):.0f} % entre 2009 y 2011 "
             f"y se recuperaron {cambio_11_12:.0f} % en 2012",
             fontsize=12, fontweight="bold", loc="left")
ax.set_ylabel("Ventas totales (millones)")
ax.set_xlabel("Año")
ax.yaxis.grid(True, color="#e5e7eb")
ax.set_axisbelow(True)
for lado in ["top", "right"]:
    ax.spines[lado].set_visible(False)
fig.text(0.01, 0.01, "Fuente: Superstore Sales (8,399 líneas de pedido)",
         fontsize=8, color="#6b7280")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("grafico_despues.svg")
plt.close(fig)

print("\nGráficos guardados: grafico_antes.svg y grafico_despues.svg")
