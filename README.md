# 🔢 Conjetura PD (Permutación--Duplicación)

**Autor:** Luis Fernando Crespo Soliz\
**Año de inicio:** 2025

## 📘 Descripción general

La **Conjetura PD (Permutación--Duplicación)** propone un fenómeno
numérico donde ciertos números naturales mantienen una **estructura
interna persistente** bajo dos operaciones simultáneas:

1.  **Permutación de cifras**\
2.  **Duplicación repetida del número**

La hipótesis sugiere que, para algunos números, existe un conjunto
estable de permutaciones que **preservan la estructura de sus dígitos**
a lo largo de la secuencia:

    n → 2n → 4n → 8n → ...

### 🧩 Ejemplo base

Para `n = 128`, sus permutaciones útiles incluyen:

    182, 218, 281, 812, 821

Y su cadena de duplicaciones:

    128 → 256 → 512 → 1024 → 2048 → ...

El comportamiento observado indica que los **dígitos del número
original** siguen reflejándose en cada paso, manteniendo un patrón
estructural no trivial.

Este repositorio contiene una aplicación que permite **visualizar**,
**analizar** y **experimentar** con esta conjetura.

## 🚀 Demo en línea

*(Agrega aquí tu enlace cuando publiques la versión web con Streamlit
Cloud u otro hosting.)*

## ⚙️ Instalación local

### Requisitos

-   Python 3.8+
-   pip

### Instalación

``` bash
git clone https://github.com/tu_usuario/conjetura-pd-app.git
cd conjetura-pd-app
pip install -r requirements.txt
streamlit run conjetura_pd_app.py
```

## 🧠 Funcionalidades principales

-   Permutaciones válidas sin ceros iniciales\
-   Cadena completa de duplicaciones\
-   Grafo interactivo con duplicaciones y permutaciones\
-   Animación progresiva del grafo\
-   Análisis de estabilidad PD\
-   Heatmap de evolución de dígitos\
-   Historial completo de duplicaciones

## 📊 Ejemplo visual

Para n = 128:

    128 → 256 → 512 → 1024
    │      │      │      └── Permutaciones de 1024
    ├── Permutaciones de 128: [182, 218, 281, 812, 821]
    ...

## 🧮 Fundamento matemático (preliminar)

Sea n un número natural. Definimos:

-   **P(n)**: permutaciones válidas de n (sin ceros iniciales y
    diferentes a n)

La conjetura propone que:

> Los dígitos de n siguen estando representados en las permutaciones de
> cada duplicación nₖ = 2ⁿ.

Si esto ocurre indefinidamente, n es **PD-estable**.

## 🧩 Áreas abiertas de investigación

-   Existencia de infinitos números PD-estables\
-   Efecto de ceros y dígitos repetidos\
-   Comportamiento en otras bases (binario, octal, hexadecimal)\
-   Algoritmos más eficientes\
-   Representación en OEIS\
-   Análisis del grafo permutación--duplicación

## 🤝 Contribuciones

Bienvenidas:

-   Mejoras del algoritmo\
-   Nuevas visualizaciones\
-   Extensiones matemáticas\
-   Aportes teóricos o divulgativos

## 📜 Licencia

MIT License

## 📬 Contacto

**Luis Fernando Crespo Soliz**\
📧 lfcrespos@gmail.com