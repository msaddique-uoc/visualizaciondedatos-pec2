
import pandas as pd
import plotly.express as px
from pathlib import Path

# 1. Descargar datos reales de Palmer Penguins
url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
df = pd.read_csv(url)

# Eliminar registros sin medidas
df = df.dropna(subset=["species", "flipper_length_mm"])

# 2. Crear el gráfico de violín
fig = px.violin(
    df,
    x="species",
    y="flipper_length_mm",
    color="species",
    box=True,
    points="all",
    title="Comparación de la longitud de aletas por especie",
    labels={
        "species": "Especie de pingüino",
        "flipper_length_mm": "Longitud de aleta (mm)"
    },
    color_discrete_map={
        "Adelie": "#2196F3",
        "Chinstrap": "#FF9800",
        "Gentoo": "#9C27B0"
    },
    template="plotly_white"
)

# 3. Mejorar la presentación
fig.update_traces(
    jitter=0.12,
    pointpos=0,
    opacity=0.8,
    marker=dict(size=4, opacity=0.5)
)

fig.update_layout(
    title_x=0.5,
    title_font_size=22,
    font=dict(size=14),
    showlegend=False,
    height=650,
    yaxis_title="Longitud de aleta (mm)",
    xaxis_title="Especie",
    annotations=[
        dict(
            text="Fuente: Palmer Penguins · Licencia CC0",
            x=0, y=-0.16,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=11, color="gray")
        )
    ],
    margin=dict(b=110)
)

# 4. Guardar como página HTML interactiva
Path("docs").mkdir(exist_ok=True)
fig.write_html("docs/violin.html")

# Mostrar el gráfico
fig.show()

print("Gráfico creado: docs/violin.html")
print("Número de observaciones utilizadas:", len(df))
