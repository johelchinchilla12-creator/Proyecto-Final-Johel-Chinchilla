"""
Módulo de análisis estadístico
---------------------------------
Calcula, a partir del diccionario anidado que entrega organizacion_datos.py,
los indicadores que pide el proyecto:

    - Población total por provincia y a nivel nacional.
    - Porcentaje de población por sexo.
    - Distribución porcentual por grupo de edad.
    - Índice de dependencia demográfica.

Índice de dependencia demográfica:
    Mide cuántas personas "dependientes" (menores de 15 y mayores de 64)
    hay por cada 100 personas en edad "productiva" (15-64 años).

        índice = (población 0-14 + población 65+) / población 15-64 * 100
"""

GRUPOS_DEPENDIENTES = ("0-14", "65+")
GRUPO_PRODUCTIVO = "15-64"


def poblacion_total_provincia(datos_organizados, provincia):
    """Suma la población de todos los grupos de edad y sexos de una provincia."""
    if provincia not in datos_organizados:
        return 0

    total = 0
    for grupo_edad, sexos in datos_organizados[provincia].items():
        total += sum(sexos.values())
    return total


def poblacion_total_nacional(datos_organizados):
    """Suma la población de todas las provincias."""
    return sum(
        poblacion_total_provincia(datos_organizados, provincia)
        for provincia in datos_organizados
    )


def porcentaje_por_sexo(datos_organizados, provincia):
    """
    Calcula el porcentaje de población femenina y masculina de una provincia.
    Retorna un diccionario, por ejemplo: {"Femenino": 50.8, "Masculino": 49.2}
    """
    totales_sexo = {"Femenino": 0, "Masculino": 0}

    for grupo_edad, sexos in datos_organizados.get(provincia, {}).items():
        for sexo, poblacion in sexos.items():
            totales_sexo[sexo] = totales_sexo.get(sexo, 0) + poblacion

    total_provincia = sum(totales_sexo.values())
    if total_provincia == 0:
        return {sexo: 0.0 for sexo in totales_sexo}

    return {
        sexo: round(poblacion / total_provincia * 100, 2)
        for sexo, poblacion in totales_sexo.items()
    }


def distribucion_por_edad(datos_organizados, provincia):
    """
    Calcula el porcentaje de población que representa cada grupo de edad
    dentro de una provincia.
    Retorna un diccionario, por ejemplo:
        {"0-14": 21.3, "15-64": 67.8, "65+": 10.9}
    """
    datos_provincia = datos_organizados.get(provincia, {})
    total_provincia = poblacion_total_provincia(datos_organizados, provincia)

    distribucion = {}
    for grupo_edad, sexos in datos_provincia.items():
        poblacion_grupo = sum(sexos.values())
        porcentaje = (poblacion_grupo / total_provincia * 100) if total_provincia else 0.0
        distribucion[grupo_edad] = round(porcentaje, 2)

    return distribucion


def indice_dependencia(datos_organizados, provincia):
    """
    Calcula el índice de dependencia demográfica de una provincia.

    Retorna:
        float: índice de dependencia (personas dependientes por cada
               100 personas en edad productiva). Si no hay población
               productiva registrada, retorna None (para evitar una
               división entre cero).
    """
    datos_provincia = datos_organizados.get(provincia, {})

    poblacion_dependiente = 0
    for grupo in GRUPOS_DEPENDIENTES:
        poblacion_dependiente += sum(datos_provincia.get(grupo, {}).values())

    poblacion_productiva = sum(datos_provincia.get(GRUPO_PRODUCTIVO, {}).values())

    if poblacion_productiva == 0:
        return None

    return round(poblacion_dependiente / poblacion_productiva * 100, 2)


def resumen_nacional(datos_organizados):
    """
    Construye un resumen con la población total, el porcentaje por sexo,
    la distribución por edad y el índice de dependencia de cada provincia,
    además del total nacional. Útil para mostrar un panorama general.

    Retorna:
        dict con la forma:
        {
            "total_nacional": 5083000,
            "provincias": {
                "San José": {
                    "poblacion_total": 1650000,
                    "porcentaje_sexo": {...},
                    "distribucion_edad": {...},
                    "indice_dependencia": 34.5,
                },
                ...
            }
        }
    """
    resumen = {
        "total_nacional": poblacion_total_nacional(datos_organizados),
        "provincias": {},
    }

    for provincia in datos_organizados:
        resumen["provincias"][provincia] = {
            "poblacion_total": poblacion_total_provincia(datos_organizados, provincia),
            "porcentaje_sexo": porcentaje_por_sexo(datos_organizados, provincia),
            "distribucion_edad": distribucion_por_edad(datos_organizados, provincia),
            "indice_dependencia": indice_dependencia(datos_organizados, provincia),
        }

    return resumen
