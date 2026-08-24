"""
Módulo de organización de datos
----------------------------------
Toma la lista de registros ya limpios (provincia, sexo, grupo_edad, anio,
poblacion) y la reorganiza en un diccionario anidado con la forma:

    {
        "San José": {
            "0-14":  {"Femenino": 164730, "Masculino": 165270},
            "15-64": {"Femenino": 539402, "Masculino": 582598},
            "65+":   {"Femenino": 106574, "Masculino": 91426},
        },
        "Alajuela": { ... },
        ...
    }

Esta estructura (diccionario dentro de diccionario) es la que después usan
los módulos de estadísticas y visualización, en lugar de recorrer la lista
plana una y otra vez.
"""


def organizar_datos(registros, anio=None):
    """
    Organiza los registros limpios en un diccionario anidado:
    provincia -> grupo_edad -> sexo -> población.

    Parámetros:
        registros (list[dict]): registros limpios (salida de limpiar_datos).
        anio (int, opcional): si se indica, solo se incluyen los registros
            de ese año. Si es None, se usan todos los registros disponibles
            (en este proyecto normalmente hay un único año en los datos).

    Retorna:
        dict: estructura anidada provincia -> grupo_edad -> sexo -> población.
    """
    datos_organizados = {}

    for registro in registros:
        # Si se pidió filtrar por año y este registro no corresponde, se salta
        if anio is not None and registro["anio"] != anio:
            continue

        provincia = registro["provincia"]
        grupo_edad = registro["grupo_edad"]
        sexo = registro["sexo"]
        poblacion = registro["poblacion"]

        # setdefault crea el diccionario/lista si todavía no existe, y en
        # caso contrario devuelve el que ya estaba, para poder ir sumando.
        datos_organizados.setdefault(provincia, {})
        datos_organizados[provincia].setdefault(grupo_edad, {})
        datos_organizados[provincia][grupo_edad][sexo] = (
            datos_organizados[provincia][grupo_edad].get(sexo, 0) + poblacion
        )

    return datos_organizados


def listar_provincias(datos_organizados):
    """Devuelve la lista de provincias disponibles, ordenada alfabéticamente."""
    return sorted(datos_organizados.keys())
