import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
from functools import lru_cache
import numpy as np
import time

# -----------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------
MAX_VALUE = 1024
st.set_page_config(page_title="Conjetura PD - Explorador Completo", layout="wide")

# -----------------------------------------------------------
# PERMUTACIONES OPTIMIZADAS
# -----------------------------------------------------------
@lru_cache(maxsize=None)
def get_valid_permutations(n):
    digits = str(n)
    perms = set()

    for p in set(permutations(digits)):
        if p[0] == "0":
            continue
        v = int("".join(p))
        if v != n and v <= MAX_VALUE:
            perms.add(v)

    return perms

# -----------------------------------------------------------
# GENERADOR DE GRAFO
# -----------------------------------------------------------
@st.cache_data(show_spinner=True)
def generar_grafo_conjetura(max_value=MAX_VALUE):
    G = nx.DiGraph()

    for n in range(1, max_value + 1):
        G.add_node(n)

        # regla: duplicación
        dup = n * 2
        if dup <= max_value:
            G.add_edge(n, dup, tipo="duplicación")

        # regla: permutación
        if n >= 10:
            for p in get_valid_permutations(n):
                G.add_edge(n, p, tipo="permutación")

    return G

# -----------------------------------------------------------
# CAMINOS
# -----------------------------------------------------------
def camino_mas_corto(G, destino):
    try:
        return nx.shortest_path(G, source=1, target=destino)
    except:
        return None

def comprimir_ruta(G, destino):
    path = camino_mas_corto(G, destino)
    if not path:
        return None, None

    pasos = []
    for a, b in zip(path[:-1], path[1:]):
        tipo = G[a][b]["tipo"]
        pasos.append("D" if tipo == "duplicación" else "P")

    return path, "".join(pasos)

# -----------------------------------------------------------
# ANALIZADOR DE ESTABILIDAD PD
# -----------------------------------------------------------
def analizar_pd_estabilidad(n, max_iteraciones=20):
    historial = []
    actual = n

    for k in range(max_iteraciones):
        historial.append(actual)
        digitos = set(str(actual))

        perms = get_valid_permutations(actual)
        union_digitos = set("".join(str(p) for p in perms))

        faltantes = digitos - union_digitos

        if faltantes:
            return {
                "estable": False,
                "iteraciones": k,
                "ruptura_en": k,
                "numero_fallido": actual,
                "digitos_faltantes": faltantes,
                "historial": historial
            }

        actual *= 2

    return {
        "estable": True,
        "iteraciones": max_iteraciones,
        "ruptura_en": None,
        "numero_fallido": None,
        "digitos_faltantes": None,
        "historial": historial
    }

# -----------------------------------------------------------
# HEATMAP
# -----------------------------------------------------------
def generar_heatmap_datos(historial):
    filas = []
    max_len = max(len(str(n)) for n in historial)

    for num in historial:
        digs = [int(d) for d in str(num)]
        while len(digs) < max_len:
            digs.insert(0, -1)
        filas.append(digs)

    return np.array(filas)

def mostrar_heatmap(historial):
    matriz = generar_heatmap_datos(historial)

    fig, ax = plt.subplots(figsize=(7, 4))
    cax = ax.imshow(matriz, aspect='auto')

    ax.set_title("Heatmap de evolución de dígitos (PD)")
    ax.set_xlabel("Posición del dígito")
    ax.set_ylabel("Iteración")

    fig.colorbar(cax, ax=ax)
    st.pyplot(fig)

# -----------------------------------------------------------
# APP STREAMLIT
# -----------------------------------------------------------
st.title("🧠 Conjetura PD — Explorador Interactivo Completo")

G = generar_grafo_conjetura()

seccion = st.sidebar.radio("Elegir sección", [
    "Explorar número",
    "Animación de crecimiento",
    "Análisis global",
    "Estabilidad PD"
])

# -----------------------------------------------------------
# 1) EXPLORAR NÚMERO
# -----------------------------------------------------------
if seccion == "Explorar número":
    st.header("🔍 Explorar caminos desde 1 hasta un número")

    num = st.number_input("Elige un número", 1, 1024, 128)

    if st.button("Buscar camino"):
        path, comp = comprimir_ruta(G, num)

        if path:
            st.success(f"Camino más corto: {path}")
            st.info(f"Ruta comprimida: {comp}")
        else:
            st.warning("No existe un camino hacia ese número.")

# -----------------------------------------------------------
# 2) ANIMACIÓN DEL GRAFO
# -----------------------------------------------------------
elif seccion == "Animación de crecimiento":
    st.header("🎞 Animación del Grafo PD")

    max_n = st.slider("Nodos a mostrar", 10, 200, 50)
    pos = nx.spring_layout(G, seed=20)

    fig, ax = plt.subplots(figsize=(10, 7))
    placeholder = st.empty()

    nodos = []
    edges = []

    for i in range(1, max_n + 1):
        nodos.append(i)

        for suc in G.successors(i):
            if suc <= max_n:
                edges.append((i, suc))

        ax.clear()
        nx.draw_networkx_nodes(G, pos, nodelist=nodos, node_color="#90CAF9", node_size=350, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="#B0BEC5", arrows=True, ax=ax)
        nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in nodos}, font_size=8, ax=ax)

        ax.set_title("Crecimiento del grafo PD")
        ax.axis("off")

        placeholder.pyplot(fig)
        time.sleep(0.05)

# -----------------------------------------------------------
# 3) ANÁLISIS GLOBAL
# -----------------------------------------------------------
elif seccion == "Análisis global":
    st.header("📊 Análisis Completo del Grafo PD")

    nodos_huerfanos = [n for n in G.nodes() if G.out_degree(n) == 0]
    dup = sum(1 for u, v in G.edges() if G[u][v]["tipo"] == "duplicación")
    perm = sum(1 for u, v in G.edges() if G[u][v]["tipo"] == "permutación")

    col1, col2, col3 = st.columns(3)
    col1.metric("Nodos totales", G.number_of_nodes())
    col2.metric("Aristas totales", G.number_of_edges())
    col3.metric("Permutaciones", perm)

    st.metric("Duplicaciones", dup)
    st.metric("Nodos sin salida", len(nodos_huerfanos))

    if st.checkbox("Mostrar nodos huérfanos"):
        st.code(nodos_huerfanos)

# -----------------------------------------------------------
# 4) ESTABILIDAD PD
# -----------------------------------------------------------
elif seccion == "Estabilidad PD":
    st.header("🔎 Análisis de Estabilidad PD")

    n = st.number_input("Número a evaluar", 1, 1024, 128)

    if st.button("Analizar estabilidad"):
        res = analizar_pd_estabilidad(n)

        if res["estable"]:
            st.success(f"✨ {n} es PD-estable al menos por {res['iteraciones']} iteraciones")
        else:
            st.error(f"❌ {n} se rompe en la iteración {res['ruptura_en']}")
            st.write("Número fallido:", res["numero_fallido"])
            st.write("Dígitos faltantes:", res["digitos_faltantes"])

        st.subheader("Historial de duplicaciones")
        st.code(res["historial"])

        st.subheader("Heatmap de evolución")
        mostrar_heatmap(res["historial"])