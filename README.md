# Sistema de Gestión de Países

## Descripción del Problema y Objetivo
La gestión manual de información demográfica y geográfica (como población, superficie y continente de distintos países) suele presentar dificultades para realizar búsquedas rápidas, aplicar filtros combinados o calcular indicadores estadísticos sin errores.

El objetivo de este proyecto es desarrollar una aplicación de consola modular en Python que permita administrar una base de datos de países almacenada en un archivo CSV (`paises.csv`), ofreciendo persistencia automática, validación iterativa de datos de entrada y una interfaz interactiva por terminal.

---

## Características Principales

- **Persistencia de datos (`paises.csv`):** Carga automática al iniciar el programa (con control de errores de formato por fila) y guardado inmediato ante cada alta o modificación, resolviendo la ruta relativa de forma segura.
- **Gestión de registros (CRUD):**
  * **Alta de países:** Validación de texto (solo letras), control de duplicados, selección de continente mediante menú desplegable y validación de números enteros positivos (`try-except`) para población y superficie.
  * **Listado completo:** Visualización en tablas formateadas con columnas alineadas y separadores de miles.
  * **Actualización de datos:** Búsqueda insensible a mayúsculas y tildes para modificar población y superficie de países existentes.
- **Búsqueda y Filtrado:**
  * Búsqueda por coincidencia parcial en el nombre del país, normalizando vocales con tilde (ej. buscar `"japon"` encuentra `"Japón"`).
  * Filtrado por continente (mediante selector de continentes válidos), rango de población o rango de superficie en km².
- **Ordenamiento dinámico:** Ordenamiento ascendente o descendente por nombre, población o superficie mediante `sorted()` y expresiones `lambda`.
- **Panel de Estadísticas:** Cálculo de cantidad total de registros, población total combinada, promedios de población y superficie, identificación de valores máximos y mínimos, y desglose de cantidad de países por continente.
- **Navegación y control de flujo:** Validación con reintento automático ante errores y posibilidad de ingresar `0` en cualquier entrada de texto o numérica para cancelar la operación y volver al menú principal.

---

## Estructura del Proyecto

```text
TPI-Gestion-Paises-Python/
│
├── main.py                  # Punto de entrada, encabezado dinámico y menú principal
├── funciones.py             # Lógica de negocio, persistencia CSV, validaciones y vistas
├── paises.csv               # Base de datos en texto plano (separada por comas)
├── requirements.txt         # Dependencias externas del proyecto
├── Informe_TPI_Paises.pdf   # Documentación académica y técnica del proyecto
└── README.md                # Guía y documentación general del repositorio
```

---

## Librerías Utilizadas

### Librerías Estándar de Python
- **`csv`:** Lectura y escritura estructurada de registros mediante `DictReader` y `DictWriter`.
- **`os`:** Resolución dinámica de rutas de archivos (`os.path`) y limpieza de pantalla multiplataforma (`os.system`).

### Librerías Externas
- **`rich`:** Formateo visual en consola mediante tablas (`Table`), paneles (`Panel`) y estilos de color para diferenciar mensajes de éxito, advertencia y error.
- **`questionary`:** Menús interactivos con separadores por categoría y barra de selección resaltada, navegables mediante las flechas del teclado (`↑` / `↓`).

---

## Instalación y Ejecución

1. **Descargar o clonar** el repositorio en su equipo:
   ```bash
   git clone [https://github.com/Adriano-Martinez1/TPI-Gestion-Paises-Python.git](https://github.com/Adriano-Martinez1/TPI-Gestion-Paises-Python.git)
   ```
2. **Abrir una terminal** ubicada dentro de la carpeta del proyecto:
   ```bash
   cd TPI-Gestion-Paises-Python
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

1. Al ejecutar `main.py`, el sistema carga automáticamente los registros desde `paises.csv` y despliega el menú principal junto con el contador de países registrados.
2. Utilice las **flechas del teclado (`↑` / `↓`)** para desplazarse por las opciones y presione **`Enter`** para confirmar:
   * **1. Agregar un país:** Solicita nombre, continente (mediante selector), población (entero) y superficie en km² (entero). Guarda el registro automáticamente.
   * **2. Ver países cargados:** Muestra todos los registros actuales en una tabla formateada.
   * **3. Actualizar datos de un país:** Busca un país por su nombre y permite sobrescribir su población y superficie.
   * **4. Buscar un país:** Permite ingresar un texto parcial o completo para listar coincidencias.
   * **5. Filtrar países:** Despliega un submenú para filtrar por continente, rango de población o rango de superficie.
   * **6. Ordenar países:** Permite elegir el criterio (nombre, población o superficie) y el sentido (ascendente o descendente).
   * **7. Ver estadísticas:** Muestra un panel resumen con totales, promedios, extremos y cantidad de países por continente.
   * **8. Salir:** Finaliza la ejecución del programa.
3. En cualquier operación que solicite ingresar datos por teclado, puede escribir **`0`** para cancelar y regresar directamente al menú principal.
4. Tras visualizar el resultado de cada operación, presione **`Enter`** para limpiar la pantalla y volver al menú.

---

## Ejemplos de Entradas y Salidas

### 1. Agregar un país (Opción 1)
**Entrada del usuario:**
```text
--- AGREGAR NUEVO PAÍS ---
Escriba 0 en cualquier campo para cancelar y volver al menú.
Ingrese el nombre del país: Chile
? Seleccione el continente: América
Ingrese la población: 19600000
Ingrese la superficie en km2: 756102
```
**Salida del sistema:**
```text
¡Éxito! El país 'Chile' se agregó correctamente.
```

---

### 2. Filtrar por continente (Opción 5 -> 1. Por Continente)
**Selección del usuario:**
```text
? Seleccione el continente a filtrar: América
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

### 3. Validación iterativa ante entrada inválida (Opción 1 o 3)
**Entrada del usuario:**
```text
Ingrese el nombre del país: Uruguay
? Seleccione el continente: América
Ingrese la población: tres millones
```
**Salida del sistema (y solicitud de reingreso):**
```text
Error: Ingrese un número entero válido sin letras ni puntos.
Ingrese la población: 3426000
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
│                                                      │
│ Cantidad de países por continente:                   │
│   • América: 2                                       │
│   • Asia: 1                                          │
│   • Europa: 1                                        │
╰──────────────────────────────────────────────────────╯
```

---

## Documentación y Video Demostrativo

- **Informe Técnico (PDF):** Disponible directamente en la raíz de este repositorio (`Informe_TPI_Paises.pdf`).
- **Video Demostrativo (10-15 min):** [Pegar aquí el enlace público al video]

---

## Participación de los Integrantes

- **Adriano Salvador Martínez Barbuzza:** Diseño de la arquitectura modular, implementación de la persistencia en CSV, desarrollo de las funcionalidades, filtros, ordenamientos y estadísticas en Python, diseño de interfaz en consola (`rich` y `questionary`), redacción de documentación técnica y pruebas del sistema.