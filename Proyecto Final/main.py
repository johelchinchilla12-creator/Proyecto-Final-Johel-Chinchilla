"""
Proyecto Final — Análisis Demográfico de Costa Rica
======================================================
Autor: Johel Chinchilla Oviedo
Curso: Fundamentos de Python

Descripción:
    Sistema de consola que carga datos de población de Costa Rica
    (organizados por provincia, sexo y grupo de edad), los limpia, calcula
    estadísticas básicas y un índice de dependencia demográfica, permite
    hacer consultas interactivas y genera visualizaciones con matplotlib.

Cómo ejecutar:
    python main.py

Estructura del programa (ver también algoritmo en el documento IteraFlex):
    1. Cargar el archivo de datos (CSV o JSON).
    2. Limpiar los datos (duplicados, valores faltantes, tipos de datos).
    3. Organizar los datos en un diccionario anidado.
    4. Mostrar un menú interactivo con ciclo while:
         - consultar por provincia
         - ver resumen nacional
         - calcular índice de dependencia
         - generar gráficos
         - salir
"""

import os

from modulos import carga_datos, limpieza_datos, organizacion_datos, estadisticas, visualizacion

# Ruta por defecto del archivo de datos (se puede cambiar desde el menú)
RUTA_DATOS_POR_DEFECTO = os.path.join("data", "poblacion_costa_rica.csv")


def cargar_y_preparar_datos(ruta_archivo):
    """
    Ejecuta el flujo completo de carga + limpieza + organización de datos.

    Retorna:
        dict | None: diccionario anidado provincia -> grupo_edad -> sexo -> población,
                      o None si no fue posible cargar los datos.
    """
    registros_crudos = carga_datos.cargar_datos(ruta_archivo)
    if registros_crudos is None:
        return None

    registros_limpios, resumen = limpieza_datos.limpiar_datos(registros_crudos)
    limpieza_datos.imprimir_resumen_limpieza(resumen)

    if not registros_limpios:
        print("\n[ERROR] No quedaron registros válidos después de la limpieza.")
        return None

    datos_organizados = organizacion_datos.organizar_datos(registros_limpios)
    return datos_organizados


def mostrar_menu_principal():
    print("\n" + "=" * 55)
    print(" ANÁLISIS DEMOGRÁFICO DE COSTA RICA — MENÚ PRINCIPAL")
    print("=" * 55)
    print("1. Cargar / recargar archivo de datos")
    print("2. Ver resumen nacional")
    print("3. Consultar estadísticas de una provincia")
    print("4. Ver índice de dependencia demográfica por provincia")
    print("5. Gráfico: población total por provincia")
    print("6. Gráfico: distribución por edad de una provincia")
    print("7. Gráfico: índice de dependencia por provincia")
    print("0. Salir")
    print("-" * 55)


def pedir_ruta_archivo():
    """Pide al usuario la ruta del archivo, o usa la ruta por defecto si no escribe nada."""
    entrada = input(
        f"Ruta del archivo (Enter para usar por defecto: '{RUTA_DATOS_POR_DEFECTO}'): "
    ).strip()
    return entrada if entrada else RUTA_DATOS_POR_DEFECTO


def elegir_provincia(datos_organizados):
    """Muestra la lista de provincias disponibles y pide al usuario elegir una por número."""
    provincias = organizacion_datos.listar_provincias(datos_organizados)

    if not provincias:
        print("\n[AVISO] No hay provincias disponibles en los datos cargados.")
        return None

    print("\nProvincias disponibles:")
    for indice, provincia in enumerate(provincias, start=1):
        print(f"  {indice}. {provincia}")

    seleccion = input("Seleccione el número de la provincia: ").strip()

    if not seleccion.isdigit() or not (1 <= int(seleccion) <= len(provincias)):
        print("\n[ERROR] Selección no válida.")
        return None

    return provincias[int(seleccion) - 1]


def mostrar_resumen_nacional(datos_organizados):
    resumen = estadisticas.resumen_nacional(datos_organizados)

    print("\n--- Resumen nacional ---")
    print(f"Población total (según datos cargados): {resumen['total_nacional']:,}")
    print(f"{'Provincia':<12} {'Población':>12} {'% Fem.':>8} {'% Masc.':>9} {'Índ. Dependencia':>18}")
    print("-" * 65)

    # Se ordenan las provincias de mayor a menor población para facilitar la lectura
    provincias_ordenadas = sorted(
        resumen["provincias"].items(),
        key=lambda item: item[1]["poblacion_total"],
        reverse=True,
    )

    for provincia, datos in provincias_ordenadas:
        porcentaje_sexo = datos["porcentaje_sexo"]
        indice = datos["indice_dependencia"]
        indice_texto = f"{indice:.2f}" if indice is not None else "N/D"
        print(f"{provincia:<12} {datos['poblacion_total']:>12,} "
              f"{porcentaje_sexo.get('Femenino', 0):>7.2f}% "
              f"{porcentaje_sexo.get('Masculino', 0):>8.2f}% "
              f"{indice_texto:>18}")


def mostrar_estadisticas_provincia(datos_organizados):
    provincia = elegir_provincia(datos_organizados)
    if provincia is None:
        return

    total = estadisticas.poblacion_total_provincia(datos_organizados, provincia)
    porcentaje_sexo = estadisticas.porcentaje_por_sexo(datos_organizados, provincia)
    distribucion_edad = estadisticas.distribucion_por_edad(datos_organizados, provincia)
    indice = estadisticas.indice_dependencia(datos_organizados, provincia)

    print(f"\n--- Estadísticas de {provincia} ---")
    print(f"Población total: {total:,}")

    print("\nPorcentaje por sexo:")
    for sexo, porcentaje in porcentaje_sexo.items():
        print(f"  {sexo}: {porcentaje:.2f}%")

    print("\nDistribución por grupo de edad:")
    for grupo, porcentaje in sorted(distribucion_edad.items()):
        print(f"  {grupo}: {porcentaje:.2f}%")

    print("\nÍndice de dependencia demográfica: "
          f"{indice:.2f}" if indice is not None else "N/D")


def mostrar_indice_dependencia_todas(datos_organizados):
    print("\n--- Índice de dependencia demográfica por provincia ---")
    print("(personas dependientes por cada 100 personas en edad productiva)\n")

    provincias = organizacion_datos.listar_provincias(datos_organizados)
    for provincia in provincias:
        indice = estadisticas.indice_dependencia(datos_organizados, provincia)
        indice_texto = f"{indice:.2f}" if indice is not None else "N/D"
        print(f"  {provincia:<12}: {indice_texto}")


def ejecutar_programa():
    """Función principal: controla el ciclo del menú interactivo."""
    print("Bienvenido(a) al sistema de análisis demográfico de Costa Rica.")

    datos_organizados = cargar_y_preparar_datos(RUTA_DATOS_POR_DEFECTO)

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ruta = pedir_ruta_archivo()
            nuevos_datos = cargar_y_preparar_datos(ruta)
            if nuevos_datos is not None:
                datos_organizados = nuevos_datos

        elif opcion in {"2", "3", "4", "5", "6", "7"} and not datos_organizados:
            print("\n[AVISO] Primero debe cargar un archivo de datos válido (opción 1).")

        elif opcion == "2":
            mostrar_resumen_nacional(datos_organizados)

        elif opcion == "3":
            mostrar_estadisticas_provincia(datos_organizados)

        elif opcion == "4":
            mostrar_indice_dependencia_todas(datos_organizados)

        elif opcion == "5":
            visualizacion.graficar_poblacion_por_provincia(datos_organizados)

        elif opcion == "6":
            provincia = elegir_provincia(datos_organizados)
            if provincia is not None:
                visualizacion.graficar_distribucion_edad(datos_organizados, provincia)

        elif opcion == "7":
            visualizacion.graficar_indice_dependencia(datos_organizados)

        elif opcion == "0":
            print("\n¡Gracias por usar el sistema! Hasta pronto.")
            break

        else:
            print("\n[ERROR] Opción no válida. Intente de nuevo.")


# Punto de entrada del programa: este bloque solo se ejecuta si el archivo
# se corre directamente (python main.py), no si se importa desde otro módulo.
if __name__ == "__main__":
    ejecutar_programa()
