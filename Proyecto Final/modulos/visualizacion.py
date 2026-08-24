"""
Módulo de visualización
---------------------------
Genera gráficos con matplotlib a partir de los datos organizados y de las
estadísticas calculadas. Cada gráfico se guarda como imagen PNG dentro de
la carpeta "graficos/" y además se muestra en pantalla.
"""

import os
import matplotlib.pyplot as plt

from modulos import estadisticas

CARPETA_GRAFICOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "graficos")


def _preparar_carpeta_salida():
    """Crea la carpeta 'graficos/' si todavía no existe."""
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)


def graficar_poblacion_por_provincia(datos_organizados):
    """Gráfico de barras con la población total de cada provincia."""
    _preparar_carpeta_salida()

    provincias = sorted(datos_organizados.keys())
    poblaciones = [
        estadisticas.poblacion_total_provincia(datos_organizados, provincia)
        for provincia in provincias
    ]

    plt.figure(figsize=(9, 5))
    barras = plt.bar(provincias, poblaciones, color="#2E86AB")
    plt.title("Población total por provincia (Costa Rica)")
    plt.xlabel("Provincia")
    plt.ylabel("Población")
    plt.xticks(rotation=30, ha="right")

    # Se muestra el valor exacto encima de cada barra
    for barra, valor in zip(barras, poblaciones):
        plt.text(barra.get_x() + barra.get_width() / 2, valor, f"{valor:,}",
                  ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    ruta_salida = os.path.join(CARPETA_GRAFICOS, "poblacion_por_provincia.png")
    plt.savefig(ruta_salida)
    print(f"\nGráfico guardado en: {ruta_salida}")
    plt.show()


def graficar_distribucion_edad(datos_organizados, provincia):
    """Gráfico circular con la distribución por grupo de edad de una provincia."""
    if provincia not in datos_organizados:
        print(f"\n[AVISO] No hay datos para la provincia '{provincia}'.")
        return

    _preparar_carpeta_salida()
    distribucion = estadisticas.distribucion_por_edad(datos_organizados, provincia)

    grupos = list(distribucion.keys())
    porcentajes = list(distribucion.values())

    plt.figure(figsize=(6, 6))
    plt.pie(porcentajes, labels=grupos, autopct="%1.1f%%", startangle=90,
            colors=["#F4A261", "#2A9D8F", "#E76F51"])
    plt.title(f"Distribución por grupo de edad — {provincia}")
    plt.tight_layout()

    nombre_archivo = f"distribucion_edad_{provincia.lower().replace(' ', '_')}.png"
    ruta_salida = os.path.join(CARPETA_GRAFICOS, nombre_archivo)
    plt.savefig(ruta_salida)
    print(f"\nGráfico guardado en: {ruta_salida}")
    plt.show()


def graficar_indice_dependencia(datos_organizados):
    """Gráfico de barras con el índice de dependencia demográfica de cada provincia."""
    _preparar_carpeta_salida()

    provincias = sorted(datos_organizados.keys())
    indices = []
    for provincia in provincias:
        indice = estadisticas.indice_dependencia(datos_organizados, provincia)
        indices.append(indice if indice is not None else 0)

    plt.figure(figsize=(9, 5))
    barras = plt.bar(provincias, indices, color="#6A4C93")
    plt.title("Índice de dependencia demográfica por provincia")
    plt.xlabel("Provincia")
    plt.ylabel("Personas dependientes por cada 100 en edad productiva")
    plt.xticks(rotation=30, ha="right")

    for barra, valor in zip(barras, indices):
        plt.text(barra.get_x() + barra.get_width() / 2, valor, f"{valor:.1f}",
                  ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    ruta_salida = os.path.join(CARPETA_GRAFICOS, "indice_dependencia.png")
    plt.savefig(ruta_salida)
    print(f"\nGráfico guardado en: {ruta_salida}")
    plt.show()
