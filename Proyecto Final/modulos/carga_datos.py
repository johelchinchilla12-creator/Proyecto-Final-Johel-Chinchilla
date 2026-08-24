"""
Módulo de carga de datos
-------------------------
Se encarga de leer el archivo con los registros de población (CSV o JSON)
y convertirlo en una lista de diccionarios "en crudo" (sin limpiar todavía).

Cada registro esperado tiene la forma:
    {
        "provincia": "San José",
        "sexo": "Femenino",
        "grupo_edad": "0-14",
        "anio": "2023",
        "poblacion": "164730"
    }

En este punto los valores pueden venir como texto (aunque representen
números) porque así los entrega el lector de CSV; la conversión de tipos
se realiza más adelante, en el módulo de limpieza.
"""

import csv
import json
import os


def cargar_datos(ruta_archivo):
    """
    Lee un archivo CSV o JSON con datos de población y devuelve una lista
    de diccionarios con los registros encontrados.

    Parámetros:
        ruta_archivo (str): ruta del archivo a cargar.

    Retorna:
        list[dict]: lista de registros "en crudo".
        None: si ocurrió un error (archivo inexistente, formato no válido, etc.)
    """

    # 1) Verificar que el archivo exista antes de intentar abrirlo
    if not os.path.isfile(ruta_archivo):
        print(f"\n[ERROR] No se encontró el archivo: '{ruta_archivo}'")
        return None

    # 2) Determinar el tipo de archivo según su extensión
    _, extension = os.path.splitext(ruta_archivo)
    extension = extension.lower()

    try:
        if extension == ".csv":
            registros = _cargar_csv(ruta_archivo)
        elif extension == ".json":
            registros = _cargar_json(ruta_archivo)
        else:
            print(f"\n[ERROR] Formato de archivo no soportado: '{extension}'. "
                  "Use un archivo .csv o .json.")
            return None
    except (OSError, csv.Error, json.JSONDecodeError) as error:
        # Cualquier problema al leer o interpretar el archivo se captura aquí
        print(f"\n[ERROR] No fue posible leer el archivo '{ruta_archivo}': {error}")
        return None

    if not registros:
        print(f"\n[AVISO] El archivo '{ruta_archivo}' no contiene registros.")
        return None

    print(f"\nSe cargaron {len(registros)} registros desde '{ruta_archivo}'.")
    return registros


def _cargar_csv(ruta_archivo):
    """Lee un archivo CSV y devuelve una lista de diccionarios (una fila = un diccionario)."""
    registros = []
    with open(ruta_archivo, mode="r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            registros.append(dict(fila))
    return registros


def _cargar_json(ruta_archivo):
    """Lee un archivo JSON (una lista de objetos) y la devuelve como lista de diccionarios."""
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        contenido = json.load(archivo)

    # El archivo JSON debe contener una lista de registros; si no, se avisa.
    if not isinstance(contenido, list):
        raise ValueError("El archivo JSON debe contener una lista de registros.")

    # Se asegura que cada valor quede como texto, igual que al leer un CSV,
    # para que el módulo de limpieza trate ambos formatos de la misma manera.
    registros = []
    for item in contenido:
        registros.append({clave: str(valor) for clave, valor in item.items()})
    return registros
