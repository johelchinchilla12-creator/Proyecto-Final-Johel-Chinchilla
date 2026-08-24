# Guion para explicar el proyecto — Análisis Demográfico de Costa Rica

Guía de estudio para la exposición (10-15 min). No es para leer palabra por palabra:
apréndete las ideas clave de cada sección y explícalas con tus palabras.

---

## 1. Introducción (1-2 min)

**El problema, en una frase:**
> "Costa Rica no tiene una herramienta simple para que alguien cargue sus propios
> datos de población, los limpie automáticamente, y calcule indicadores como el
> índice de dependencia demográfica por provincia. Mi programa hace exactamente eso."

**Por qué importa:** conocer cómo está distribuida la población (niños, adultos,
adultos mayores) por provincia ayuda a planificar servicios públicos — salud,
educación, infraestructura.

**Qué construí, en una frase:**
> "Un sistema de consola en Python con menú interactivo, que carga datos CSV o JSON,
> los limpia, los organiza, calcula estadísticas y genera gráficos con matplotlib."

---

## 2. Los datos (2 min)

- Columnas: `provincia, sexo, grupo_edad, anio, poblacion`
- 3 grupos de edad: `0-14`, `15-64` (edad productiva), `65+`
- 7 provincias de Costa Rica
- **Detalle importante que te van a notar:** metí defectos a propósito en el CSV
  (duplicados, valores vacíos, un valor de texto raro, una fila sin provincia)
  **para poder demostrar en vivo que el módulo de limpieza funciona de verdad**,
  no solo que "no falla" con datos perfectos.

---

## 3. Implementación en Python — arquitectura (3-4 min)

El programa está dividido en módulos, cada uno con una responsabilidad (esto es
"modularizar", parte de la metodología IteraFlex). El flujo es una cadena, cada
función recibe el resultado de la anterior:

```
cargar_datos()  →  limpiar_datos()  →  organizar_datos()  →  estadisticas / visualizacion
```

### `carga_datos.py` — lee el archivo
- Detecta si es `.csv` o `.json` por la extensión y usa el lector correcto.
- Si el archivo no existe: `os.path.isfile()` lo detecta antes de intentar abrirlo,
  y muestra un error claro en vez de que el programa se caiga.
- Usa `try/except` para capturar errores de lectura o de formato.
- **Explícalo así:** "Este módulo es el punto de entrada de datos externos —
  por eso es el que más maneja errores."

### `limpieza_datos.py` — el más importante para explicar
Hace 3 cosas sobre cada fila:
1. **Descarta filas incompletas** (sin provincia, sexo o grupo de edad — no se
   pueden clasificar).
2. **Convierte texto a número** con una función auxiliar `_texto_a_entero()` que
   devuelve `None` si el valor no es válido (por ejemplo `"N/D"`).
3. **Elimina duplicados** usando un `set()` de tuplas `(provincia, sexo, grupo_edad, año)`
   como "huella" — si ya vio esa combinación exacta, la descarta.

Al final imprime un resumen: cuántos registros originales, cuántos duplicados,
cuántos descartados, cuántos quedaron limpios.

### `organizacion_datos.py` — arma la estructura de datos central
Convierte la lista plana de registros en un **diccionario anidado**:

```python
{
  "San José": {
      "0-14":  {"Femenino": 164730, "Masculino": 165270},
      "15-64": {"Femenino": 539402, "Masculino": 582598},
      "65+":   {"Femenino": 106574, "Masculino": 91426},
  },
  "Alajuela": { ... },
}
```

**Por qué un diccionario anidado y no una lista:** porque después necesito acceder
directo por `datos["San José"]["0-14"]["Femenino"]` sin recorrer toda la lista cada
vez que quiero un dato — es más eficiente para calcular estadísticas repetidamente.

### `estadisticas.py` — los cálculos
- Población total por provincia y nacional (`sum()`).
- Porcentaje por sexo.
- Distribución por grupo de edad.
- **Índice de dependencia demográfica** (el indicador estrella):

```
índice = (población 0-14 + población 65+) / población 15-64 × 100
```

> "Por cada 100 personas en edad de trabajar, hay X personas que dependen de
> ellas (niños o adultos mayores)."

Si la población productiva es 0, la función devuelve `None` en vez de crashear
por división entre cero — así se explica manejo defensivo de errores.

### `visualizacion.py` — los gráficos
Usa `matplotlib` para generar:
- Gráfico de barras: población total por provincia.
- Gráfico circular: distribución por edad de una provincia.
- Gráfico de barras: índice de dependencia por provincia.

Cada gráfico se guarda como PNG en `graficos/` y también se muestra en pantalla.

### `main.py` — el menú interactivo
Un ciclo `while True` que muestra opciones y usa `if/elif/else` para decidir qué
función llamar según lo que escribe el usuario. Valida que la opción exista antes
de ejecutarla (estructuras de control).

---

## 4. Estructuras de datos usadas (menciónalo, te lo van a preguntar)

| Estructura | Dónde se usa | Por qué |
|---|---|---|
| Lista de diccionarios | Registros crudos/limpios | Cada fila del CSV es un registro independiente |
| Diccionario anidado | `datos_organizados` | Acceso directo por provincia→edad→sexo |
| `set()` | Detección de duplicados | Búsqueda O(1) de "¿ya vi esto?" |
| Tuplas | "Huella" de cada registro | Inmutables, se pueden meter en un `set` |

---

## 5. Resultados (2-3 min) — usa estos números reales

Con el dataset de ejemplo (46 registros → 39 limpios):

- **San José** es la provincia más poblada: 1,650,000 habitantes.
- **Heredia** tiene el índice de dependencia más bajo (37.68) → más población
  en edad productiva relativa.
- **Puntarenas** tiene el índice más alto (53.85) → necesita más inversión
  relativa en servicios para niños y adultos mayores.
- El programa detectó y limpió automáticamente 7 de 46 registros con problemas,
  sin intervención manual.

---

## 6. Demo en vivo — guion de comandos

```bash
cd "Proyecto Final"
python3 main.py
```

| Escribes | Qué muestra |
|---|---|
| (arranca solo) | Resumen de limpieza: "46 → 39 registros" — explica que detectó los datos defectuosos |
| `2` | Resumen nacional: tabla de las 7 provincias |
| `3` → número de provincia | Estadísticas detalladas de una provincia |
| `4` | Solo los índices de dependencia, fácil de comparar |
| `5` | Abre el gráfico de barras de población |
| `0` | Cierra el programa |

---

## 7. Preguntas típicas y cómo responderlas

- **"¿Por qué un diccionario anidado y no una lista?"**
  → Acceso directo sin recorrer todo; más eficiente para consultas repetidas.

- **"¿Qué pasa si el archivo no existe?"**
  → `cargar_datos()` verifica con `os.path.isfile()` antes de abrir y muestra
  un error claro sin que el programa se caiga.

- **"¿Qué pasa si divides entre cero en el índice de dependencia?"**
  → `indice_dependencia()` revisa si la población productiva es 0 y devuelve
  `None` en vez de crashear.

- **"¿Por qué el CSV tiene errores a propósito?"**
  → Para poder demostrar en vivo que el módulo de limpieza funciona de verdad.

- **"¿Cómo evitas procesar datos duplicados?"**
  → Con un `set()` que guarda una tupla (provincia, sexo, grupo_edad, año) por
  cada registro ya visto; si se repite, se descarta.

- **"¿Por qué modularizaste el código en vez de un solo archivo?"**
  → Cada módulo tiene una sola responsabilidad (cargar, limpiar, organizar,
  calcular, graficar) — más fácil de leer, probar y mantener, y sigue la idea
  de IteraFlex de dividir la solución en procedimientos.

---

## 8. Estructura sugerida de tiempo (10-15 min total)

- Introducción (problema + qué construí): **2 min**
- Datos + arquitectura del código: **4 min**
- Demo en vivo del programa: **4 min**
- Resultados y conclusiones: **2-3 min**
- Preguntas: el resto
