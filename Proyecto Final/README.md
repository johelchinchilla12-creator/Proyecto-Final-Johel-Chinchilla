# Análisis Demográfico de Costa Rica

Proyecto Final — Fundamentos de Python
Autor: **Johel Chinchilla Oviedo**

## 1. Problema abordado

Costa Rica no cuenta con una herramienta sencilla y flexible que permita
cargar datos poblacionales propios, limpiarlos y explorarlos de forma
interactiva. Este proyecto desarrolla un sistema en Python que:

- Carga datos de población de Costa Rica por **provincia, sexo y grupo de edad**.
- Limpia los datos (duplicados, valores faltantes, tipos incorrectos).
- Calcula indicadores estadísticos simples (porcentajes por sexo, distribución
  por edad e **índice de dependencia demográfica**).
- Permite consultar los resultados mediante un **menú interactivo**.
- Genera **visualizaciones** (barras y pastel) con `matplotlib`.

Esto sirve de apoyo a la planificación de servicios públicos (salud,
educación, infraestructura) al identificar, por ejemplo, provincias con
mayor envejecimiento poblacional.

## 2. Datos utilizados

- `data/poblacion_costa_rica.csv`: dataset principal (46 filas). Es un
  conjunto de **datos ilustrativos**, construido a partir de proporciones
  poblacionales aproximadas de las 7 provincias de Costa Rica (año 2023),
  con **defectos intencionales** (3 duplicados, 3 valores faltantes/no
  numéricos en subgrupos pequeños de 65+, y 1 fila sin provincia) para
  poder **demostrar el módulo de limpieza** en la exposición sin distorsionar
  de forma exagerada los totales.
- `data/poblacion_costa_rica.json`: mismo conjunto de datos ya limpio, en
  formato JSON, para demostrar que `cargar_datos()` soporta ambos formatos.

> Para usar datos reales del INEC, basta con reemplazar el CSV manteniendo
> las columnas `provincia,sexo,grupo_edad,anio,poblacion` (grupo_edad debe
> ser `0-14`, `15-64` o `65+`).

## 3. Estructura del proyecto

```
Proyecto Final/
├── main.py                       # Punto de entrada: menú interactivo
├── requirements.txt
├── data/
│   ├── poblacion_costa_rica.csv  # dataset "crudo" (con defectos a propósito)
│   └── poblacion_costa_rica.json # dataset limpio en JSON
├── modulos/
│   ├── carga_datos.py            # cargar_datos()
│   ├── limpieza_datos.py         # limpiar_datos()
│   ├── organizacion_datos.py     # organizar_datos()
│   ├── estadisticas.py           # cálculos estadísticos e índice de dependencia
│   └── visualizacion.py          # gráficos con matplotlib
└── graficos/                     # imágenes PNG generadas al ejecutar el programa
```

Esta modularización corresponde directamente a los procedimientos
definidos en el documento IteraFlex (Pregunta G):
`cargar_datos → limpiar_datos → organizar_datos → calcular_estadisticas →
consultar_datos / graficar_resultados`.

## 4. Estructuras de datos utilizadas

- **Listas de diccionarios**: representación intermedia de los registros
  (`[{"provincia": ..., "sexo": ..., ...}, ...]`).
- **Diccionario anidado** (`provincia -> grupo_edad -> sexo -> población`):
  estructura principal para estadísticas y gráficos.
- **Conjuntos (`set`)**: para detectar duplicados de forma eficiente en
  `limpiar_datos()`.
- **Tuplas**: como "huella" inmutable de cada registro al comparar duplicados.

## 5. Cómo ejecutar el programa

```bash
cd "Proyecto Final"
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Al iniciar, el programa carga automáticamente `data/poblacion_costa_rica.csv`.
Desde el menú se puede recargar otro archivo (CSV o JSON), consultar
estadísticas por provincia, ver el índice de dependencia y generar gráficos
(que se guardan en `graficos/` y también se muestran en pantalla).

## 6. Índice de dependencia demográfica

```
índice = (población 0-14 + población 65+) / población 15-64 × 100
```

Representa cuántas personas dependientes (niños/adolescentes y personas
adultas mayores) hay por cada 100 personas en edad productiva.

## 7. Metodología IteraFlex

Este proyecto sigue el proceso IteraFlex documentado en
`AvanceProyecto_Johel_Chinchilla.docx`:

1. **Definir el problema** — necesidad de análisis demográfico flexible.
2. **Investigar** — fuentes: INEC, CCP-UCR, documentación de pandas/matplotlib.
3. **Plantear una solución** — 3 ideas evaluadas; se seleccionó la combinación
   de las ideas 1 y 3.
4. **Modularizar y algoritmo** — ver Preguntas G y H del documento.
5. **Prototipar / construir** — código de este repositorio.

## 8. Próximos pasos para la entrega

- [ ] Completar el documento IteraFlex final (PDF) con capturas del código.
- [ ] Subir el proyecto a un repositorio público en GitHub.
- [ ] Preparar la presentación (10–15 min): introducción, desarrollo,
      resultados y demostración en vivo del menú y los gráficos.
