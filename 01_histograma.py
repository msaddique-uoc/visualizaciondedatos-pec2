
from pathlib import Path
import pandas as pd
import plotly.express as px

# 1. Descargar el conjunto de datos abierto Palmer Penguins
URL = (
    "https://raw.githubusercontent.com/allisonhorst/"
    "palmerpenguins/main/inst/extdata/penguins.csv"
)

df = pd.read_csv(URL)

# 2. Seleccionar la variable y eliminar valores ausentes
datos = df.dropna(subset=["flipper_length_mm"]).copy()

print("Número de observaciones válidas:", len(datos))
print(datos["flipper_length_mm"].describe())

# 3. Crear un histograma de frecuencias
fig = px.histogram(
    datos,
    x="flipper_length_mm",
    nbins=16,
    title="Distribución de la longitud de aletas de pingüinos",
    labels={
        "flipper_length_mm": "Longitud de la aleta (mm)"
    },
    color_discrete_sequence=["#148C91"],
    template="plotly_white"
)

fig.update_traces(
    marker_line_color="white",
    marker_line_width=1,
    hovertemplate="Longitud: %{x} mm<br>Frecuencia: %{y}<extra></extra>"
)

fig.update_layout(
    xaxis_title="Longitud de la aleta (mm)",
    yaxis_title="Número de pingüinos",
    bargap=0.02,
    font=dict(family="Arial", size=15, color="#243447"),
    title=dict(x=0.5, font=dict(size=22)),
    margin=dict(l=75, r=40, t=100, b=115),
    annotations=[
        dict(
            text=(
                "Fuente: Palmer Penguins (Gorman et al.; "
                "Horst, Hill y Gorman). Licencia CC0."
            ),
            xref="paper", yref="paper",
            x=0, y=-0.24,
            showarrow=False,
            font=dict(size=11, color="#667085"),
            xanchor="left"
        )
    ]
)

# 4. Guardar HTML interactivo
Path("docs").mkdir(exist_ok=True)
fig.write_html("docs/histograma.html", include_plotlyjs="cdn")

fig.show()
print("Creado: docs/histograma.html")
