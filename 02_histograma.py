
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# 1. Cargar los datos reales
url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
df = pd.read_csv(url).dropna(subset=["species", "island", "sex"])

# 2. Crear la jerarquía: especie -> isla -> sexo
arbol = {}
for (especie, isla, sexo), grupo in df.groupby(
    ["species", "island", "sex"]
):
    arbol.setdefault(especie, {}).setdefault(isla, {})[sexo] = len(grupo)

# 3. Preparar el gráfico circular
fig = go.Figure()
colores = {"Adelie": "#2196F3",
           "Chinstrap": "#FF9800",
           "Gentoo": "#9C27B0"}

hojas = [(e, i, s) for e in arbol
         for i in arbol[e] for s in arbol[e][i]]

angulos = {h: 360 * (n + 0.5) / len(hojas)
           for n, h in enumerate(hojas)}

def linea(radios, grados, color):
    fig.add_trace(go.Scatterpolar(
        r=radios, theta=grados,
        mode="lines",
        line=dict(color=color, width=2.5),
        hoverinfo="skip",
        showlegend=False
    ))

def arco(radio, inicio, fin, color):
    linea([radio] * 30,
          np.linspace(inicio, fin, 30), color)

def nodo(radio, angulo, nombre, color, cantidad):
    fig.add_trace(go.Scatterpolar(
        r=[radio], theta=[angulo],
        mode="markers+text",
        marker=dict(size=9, color=color),
        text=[nombre],
        textposition="top center",
        hovertemplate=f"{nombre}: {cantidad} pingüinos<extra></extra>",
        showlegend=False
    ))

# 4. Dibujar especies, islas y sexos
for especie, islas in arbol.items():
    color = colores[especie]
    a_especie = [angulos[h] for h in hojas if h[0] == especie]
    centro = np.mean(a_especie)

    linea([0, 1], [centro, centro], color)
    nodo(1, centro, especie, color,
         sum(len(arbol[especie][i]) for i in islas))

    arco(2, min(a_especie), max(a_especie), color)
    linea([1, 2], [centro, centro], color)

    for isla, sexos in islas.items():
        a_isla = [angulos[(especie, isla, s)] for s in sexos]
        medio = np.mean(a_isla)

        nodo(2, medio, isla, color, sum(sexos.values()))
        linea([2, 3], [medio, medio], color)
        arco(3, min(a_isla), max(a_isla), color)

        for sexo, cantidad in sexos.items():
            a = angulos[(especie, isla, sexo)]
            linea([3, 3.7], [a, a], color)
            nodo(3.7, a, sexo.capitalize(), color, cantidad)

# 5. Diseño y guardar en HTML
fig.update_layout(
    title="Dendrograma circular de pingüinos",
    template="plotly_white",
    font=dict(size=12),
    polar=dict(
        radialaxis=dict(visible=False, range=[0, 4.5]),
        angularaxis=dict(visible=False, direction="clockwise")
    ),
    width=950,
    height=850,
    margin=dict(l=80, r=80, t=100, b=80)
)

Path("docs").mkdir(exist_ok=True)
fig.write_html("docs/dendrograma.html")
fig.show()
