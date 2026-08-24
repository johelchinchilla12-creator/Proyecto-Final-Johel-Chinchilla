"""
Módulo de limpieza de datos
-----------------------------
Recibe la lista de registros "en crudo" (tal como los entrega carga_datos.py)
y realiza tres tareas:

    1. Elimina registros duplicados.
    2. Descarta o completa valores faltantes / inválidos.
    3. Convierte los campos numéricos de texto a int.

Devuelve una lista de diccionarios ya lista para organizar_datos.py, junto
con un pequeño resumen de lo que se hizo (para mostrarlo al usuario).
"""

# Grupos de edad y sexos válidos para el proyecto; sirven para detectar
# registros con datos "raros" que no se puedan clasificar.
GRUPOS_EDAD_VALIDOS = {"0-14", "15-64", "65+"}
SEXOS_VALIDOS = {"Femenino", "Masculino"}


def limpiar_datos(registros):
    """
    Limpia una lista de registros de población.

    Parámetros:
        registros (list[dict]): registros en crudo (valores como texto).

    Retorna:
        tuple:
            list[dict]  -> registros limpios, con "anio" y "poblacion" como int.
            dict        -> resumen con la cantidad de duplicados, descartados
                            y valores corregidos.
    """

    resumen = {
        "total_original": len(registros),
        "duplicados_eliminados": 0,
        "descartados_incompletos": 0,
        "descartados_invalidos": 0,
        "total_limpio": 0,
    }

    vistos = set()          # guarda una "huella" de cada registro ya procesado
    registros_limpios = []

    for fila in registros:
        # --- 1) Normalizar espacios en blanco de los campos de texto ---
        provincia = (fila.get("provincia") or "").strip()
        sexo = (fila.get("sexo") or "").strip()
        grupo_edad = (fila.get("grupo_edad") or "").strip()
        anio_texto = (fila.get("anio") or "").strip()
        poblacion_texto = (fila.get("poblacion") or "").strip()

        # --- 2) Descartar filas con campos de texto faltantes ---
        # Si falta la provincia, el sexo o el grupo de edad, el registro
        # no se puede clasificar dentro de la estructura de datos, así que
        # se descarta (no hay forma razonable de "completarlo").
        if not provincia or not sexo or not grupo_edad:
            resumen["descartados_incompletos"] += 1
            continue

        # --- 3) Validar que sexo y grupo de edad tengan valores esperados ---
        if sexo not in SEXOS_VALIDOS or grupo_edad not in GRUPOS_EDAD_VALIDOS:
            resumen["descartados_invalidos"] += 1
            continue

        # --- 4) Convertir año y población de texto a número ---
        anio = _texto_a_entero(anio_texto)
        poblacion = _texto_a_entero(poblacion_texto)

        if anio is None or poblacion is None:
            # Población o año vacíos/no numéricos ("", "N/D", etc.)
            # En este proyecto se decide descartar el registro, ya que un
            # dato de población inventado (por ejemplo 0) distorsionaría
            # las estadísticas.
            resumen["descartados_incompletos"] += 1
            continue

        # --- 5) Detectar y eliminar duplicados exactos ---
        huella = (provincia, sexo, grupo_edad, anio)
        if huella in vistos:
            resumen["duplicados_eliminados"] += 1
            continue
        vistos.add(huella)

        registros_limpios.append({
            "provincia": provincia,
            "sexo": sexo,
            "grupo_edad": grupo_edad,
            "anio": anio,
            "poblacion": poblacion,
        })

    resumen["total_limpio"] = len(registros_limpios)
    return registros_limpios, resumen


def _texto_a_entero(texto):
    """
    Convierte un texto a entero de forma segura.
    Devuelve None si el texto está vacío o no representa un número
    (por ejemplo "N/D", "", "abc").
    """
    if not texto:
        return None
    try:
        # Se permite un punto decimal por si el dato viene como "164730.0"
        return int(float(texto))
    except ValueError:
        return None


def imprimir_resumen_limpieza(resumen):
    """Muestra en consola un resumen legible del proceso de limpieza."""
    print("\n--- Resumen de limpieza de datos ---")
    print(f"Registros originales:        {resumen['total_original']}")
    print(f"Duplicados eliminados:       {resumen['duplicados_eliminados']}")
    print(f"Descartados (incompletos):   {resumen['descartados_incompletos']}")
    print(f"Descartados (valores no válidos): {resumen['descartados_invalidos']}")
    print(f"Registros limpios finales:   {resumen['total_limpio']}")
