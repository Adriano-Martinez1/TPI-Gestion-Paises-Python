# Sistema de Gestión de Países

## Descripción del Problema y Objetivo
La gestión manual de información demográfica y geográfica (como población, superficie y continente de distintos países) suele presentar dificultades para realizar búsquedas rápidas, aplicar filtros combinados o calcular indicadores estadísticos sin errores.

El objetivo de este proyecto es desarrollar una aplicación de consola modular en Python que permita administrar una base de datos de países almacenada en un archivo CSV (`paises.csv`), ofreciendo persistencia automática, validación de datos de entrada y una interfaz interactiva por terminal.

---

## Características Principales

* **Persistencia de datos (`paises.csv`):** Carga automática al iniciar el programa y guardado inmediato ante cada alta o modificación, resolviendo la ruta relativa de forma segura.
* **Gestión de registros (CRUD):**
  * **Alta de países:** Validación de campos vacíos y control de tipos numéricos (`try-except`) para población y superficie.
  * **Listado completo:** Visualización en tablas formateadas con columnas alineadas y separadores de miles.
  * **Actualización de datos:** Búsqueda insensible a mayúsculas y tildes para modificar población y superficie de países existentes.
* **Búsqueda y Filtrado:**
  * Búsqueda por coincidencia parcial en el nombre del país, normalizando vocales con tilde (ej. buscar `"japon"` encuentra `"Japón"`).
  * Filtrado por continente exacto (ignorando tildes y mayúsculas), rango de población o rango de superficie en $\text{km}^2$.
* **Ordenamiento dinámico:** Ordenamiento ascendente o descendente por nombre, población o superficie mediante `sorted()` y expresiones `lambda`.
* **Panel de Estadísticas:** Cálculo de cantidad total de registros, población total combinada, promedios de población y superficie, e identificación de valores máximos y mínimos.

---

## Estructura del Proyecto

```text
TPI_Programacion/
│
├── main.py             # Punto de entrada y bucle principal de navegación
├── funciones.py        # Lógica de negocio, persistencia CSV, validaciones y vistas
├── paises.csv          # Base de datos en texto plano (separada por comas)
├── requirements.txt    # Dependencias externas del proyecto
└── README.md           # Documentación del sistema
```

---

## Librerías Utilizadas

### Librerías Estándar de Python
* **`csv`:** Lectura y escritura estructurada de registros mediante `DictReader` y `DictWriter`.
* **`os`:** Resolución dinámica de rutas de archivos (`os.path`) y limpieza de pantalla multiplataforma (`os.system`).

### Librerías Externas
* **`rich`:** Formateo visual en consola mediante tablas (`Table`), paneles (`Panel`) y estilos de color para diferenciar mensajes de éxito, advertencia y error.
* **`questionary`:** Menús interactivos navegables mediante las flechas del teclado (`↑` / `↓`), reduciendo errores de tipeo en la selección de opciones.

---

## Instalación y Ejecución

1. **Descargar o clonar** la carpeta del proyecto en su equipo.
2. **Abrir una terminal** ubicada dentro de la carpeta `TPI_Programacion`:
   ```bash
   cd TPI_Programacion
   ```
3. **Instalar las dependencias** listadas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```

---

## Instrucciones de Uso

1. Al ejecutar `main.py`, el sistema carga automáticamente los registros desde `paises.csv` y despliega el menú principal.
2. Utilice las **flechas del teclado (`↑` / `↓`)** para desplazarse por las opciones y presione **`Enter`** para confirmar:
   * **1. Agregar un país:** Solicita nombre, continente, población (entero) y superficie en $\text{km}^2$ (entero). Guarda el registro automáticamente.
   * **2. Ver países cargados:** Muestra todos los registros actuales en una tabla formateada.
   * **3. Actualizar datos de un país:** Busca un país por su nombre exacto y permite sobrescribir su población y superficie.
   * **4. Buscar un país:** Permite ingresar un texto parcial o completo para listar coincidencias.
   * **5. Filtrar países:** Despliega un submenú para filtrar por continente, rango de población o rango de superficie.
   * **6. Ordenar países:** Permite elegir el criterio (nombre, población o superficie) y el sentido (ascendente o descendente).
   * **7. Ver estadísticas:** Muestra un panel resumen con totales, promedios y extremos.
   * **8. Salir:** Finaliza la ejecución del programa.
3. Tras visualizar el resultado de cada operación, presione **`Enter`** para regresar al menú principal.

---

## Ejemplos de Entradas y Salidas

### 1. Agregar un país (Opción 1)
**Entrada del usuario:**
```text
Ingrese el nombre del país: Chile
Ingrese el continente: América
Ingrese la población: 19600000
Ingrese la superficie en km2: 756102
```
**Salida del sistema:**
```text
¡Éxito! El país 'Chile' se agregó correctamente.
```

---

### 2. Filtrar por continente ignorando tildes (Opción 5 $\rightarrow$ Por Continente)
**Entrada del usuario:**
```text
Ingrese el continente: america
```
**Salida del sistema:**
```text
                 PAÍSES FILTRADOS (2)
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ País      ┃ Continente ┃  Población ┃ Superficie (km²) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Argentina │ América    │ 46,234,830 │        2,780,400 │
│ Chile     │ América    │ 19,600,000 │          756,102 │
└───────────┴────────────┴────────────┴──────────────────┘
```

---

### 3. Manejo de errores ante entrada inválida (Opción 1 o 3)
**Entrada del usuario:**
```text
Ingrese el nombre del país: Uruguay
Ingrese el continente: América
Ingrese la población: tres millones
```
**Salida del sistema:**
```text
Error: La población y la superficie deben ser números enteros sin letras ni puntos.
```

---

### 4. Visualización de estadísticas (Opción 7)
**Salida del sistema:**
```text
╭────────────── ESTADÍSTICAS DEL SISTEMA ──────────────╮
│ Cantidad total de países en el sistema: 4            │
│ Población total combinada: 204,434,830 hab.          │
│ Población promedio: 51,108,707.50 hab.               │
│ Superficie promedio: 973,618.75 km²                  │
│                                                      │
│ ▲ Mayor población: Japón (125,100,000 hab.)          │
│ ▼ Menor población: Alemania (83,200,000 hab.)        │
│ ▲ Mayor superficie: Argentina (2,780,400 km²)        │
│ ▼ Menor superficie: Alemania (357,588 km²)           │
╰──────────────────────────────────────────────────────╯
```