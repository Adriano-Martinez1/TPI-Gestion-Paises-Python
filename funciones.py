import csv
import os
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Inicializamos la consola de Rich para imprimir con colores, tablas y paneles
console = Console()

# Calculamos la ruta exacta de la carpeta donde está guardado este archivo (funciones.py)
# Así nos aseguramos de que siempre lea y escriba el 'paises.csv' correcto sin importar desde dónde se ejecute
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "paises.csv")


# Reemplaza las vocales con tilde por vocales sin tilde para evitar fallos en búsquedas y filtros
def quitar_tildes(texto):
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for con_tilde, sin_tilde in reemplazos:
        texto = texto.replace(con_tilde, sin_tilde)
    return texto


# Muestra cualquier lista de países en una tabla formateada con Rich
def mostrar_tabla_paises(lista, titulo="LISTADO DE PAÍSES"):
    if len(lista) == 0:
        console.print("[bold yellow]No hay países para mostrar.[/bold yellow]")
        return

    # Creamos la tabla y definimos sus columnas y estilos
    tabla = Table(title=titulo, show_header=True, header_style="bold magenta", border_style="bright_blue")
    tabla.add_column("País", style="bold cyan", no_wrap=True)
    tabla.add_column("Continente", style="green")
    tabla.add_column("Población", justify="right", style="white")
    tabla.add_column("Superficie (km²)", justify="right", style="white")

    # Recorremos la lista y agregamos cada país como una fila de la tabla
    for pais in lista:
        tabla.add_row(
            pais["nombre"],
            pais["continente"],
            f"{pais['poblacion']:,}",
            f"{pais['superficie']:,}"
        )

    console.print()
    console.print(tabla)


# Lee los registros desde el archivo CSV y los devuelve como una lista de diccionarios
def cargar_datos(ruta_archivo=RUTA_CSV):
    lista_paises = []
    
    try:
        # Abrimos el archivo en modo lectura ("r") con codificación UTF-8
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            
            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    # Validamos que existan todas las columnas esperadas y no estén vacías
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    if not nombre or not continente:
                        raise ValueError("Campos de texto vacíos")

                    # Convertimos población y superficie a números enteros
                    poblacion = int(fila["poblacion"])
                    superficie = int(fila["superficie"])

                    lista_paises.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente
                    })
                except (ValueError, KeyError, TypeError):
                    console.print(f"[bold yellow]Advertencia:[/bold yellow] Fila {numero_fila} del CSV con formato inválido. Se omitirá.")
                
    except FileNotFoundError:
        console.print(f"[bold yellow]Aviso:[/bold yellow] El archivo '{ruta_archivo}' no se encontró. Se iniciará con una lista vacía.")
    except Exception as e:
        console.print(f"[bold red]Ocurrió un error inesperado al leer el archivo:[/bold red] {e}")
        
    return lista_paises


# Guarda la lista completa de países en el archivo CSV
def guardar_datos(lista_paises, ruta_archivo=RUTA_CSV):
    try:
        # Definimos el orden exacto de las columnas (las claves del diccionario)
        encabezados = ["nombre", "poblacion", "superficie", "continente"]
        
        # Abrimos en modo escritura ("w") con newline="" para evitar saltos de línea extra
        with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()            # Escribe la primera fila con los títulos
            escritor.writerows(lista_paises)  # Vuelca todos los datos al archivo
    except PermissionError:
        console.print("[bold red]Error:[/bold red] El archivo está abierto en otro programa. Ciérrelo para poder guardar.")
    except Exception as e:
        console.print(f"[bold red]Ocurrió un error inesperado al guardar:[/bold red] {e}")


# Solicita los datos de un nuevo país, valida las entradas y lo persiste en el CSV
def agregar_pais(lista_paises):
    console.print("\n[bold cyan]--- AGREGAR NUEVO PAÍS ---[/bold cyan]")
    
    # 1. Pedimos los datos de texto y usamos strip() para limpiar espacios extra
    nombre = input("Ingrese el nombre del país: ").strip()
    continente = input("Ingrese el continente: ").strip()
    
    # Validamos que no hayan dejado campos vacíos
    if nombre == "" or continente == "":
        console.print("[bold red]Error:[/bold red] El nombre y el continente no pueden estar vacíos.")
        return

    # Validamos que el país no esté duplicado
    for pais in lista_paises:
        if quitar_tildes(pais["nombre"].lower()) == quitar_tildes(nombre.lower()):
            console.print(f"[bold red]Error:[/bold red] El país '{pais['nombre']}' ya existe en el sistema.")
            return
        
    # 2. Pedimos los datos numéricos con un try-except para atajar errores de tipeo
    try:
        poblacion = int(input("Ingrese la población: "))
        superficie = int(input("Ingrese la superficie en km2: "))
        if poblacion <= 0 or superficie <= 0:
            console.print("[bold red]Error:[/bold red] La población y la superficie deben ser mayores a cero.")
            return
    except ValueError:
        console.print("[bold red]Error:[/bold red] La población y la superficie deben ser números enteros sin letras ni puntos.")
        return
        
    # 3. Si todo está bien, armamos el diccionario del nuevo país
    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    
    # 4. Lo agregamos a la lista en memoria y guardamos los cambios en el disco
    lista_paises.append(nuevo_pais)
    guardar_datos(lista_paises)
    console.print(f"[bold green]¡Éxito![/bold green] El país '[cyan]{nombre}[/cyan]' se agregó correctamente.")


# Busca un país por nombre y actualiza su población y superficie
def actualizar_pais(lista_paises):
    console.print("\n[bold cyan]--- ACTUALIZAR PAÍS ---[/bold cyan]")
    nombre_buscado = quitar_tildes(input("Ingrese el nombre del país que desea actualizar: ").strip().lower())
    
    pais_encontrado = False
    
    # Recorremos la lista buscando una coincidencia
    for pais in lista_paises:
        if quitar_tildes(pais["nombre"].lower()) == nombre_buscado:
            pais_encontrado = True
            console.print(f"País encontrado: [bold cyan]{pais['nombre']}[/bold cyan] | Población actual: {pais['poblacion']:,} | Superficie: {pais['superficie']:,} km²")
            
            try:
                nueva_poblacion = int(input("Ingrese la nueva población: "))
                nueva_superficie = int(input("Ingrese la nueva superficie en km2: "))

                if nueva_poblacion <= 0 or nueva_superficie <= 0:
                    console.print("[bold red]Error:[/bold red] Los valores deben ser mayores a cero. Cancelando actualización.")
                    return
                
                # Actualizamos el diccionario en memoria
                pais["poblacion"] = nueva_poblacion
                pais["superficie"] = nueva_superficie
                
                # Guardamos los cambios en el disco
                guardar_datos(lista_paises)
                console.print("[bold green]¡Éxito![/bold green] Los datos fueron actualizados correctamente.")
                
            except ValueError:
                console.print("[bold red]Error:[/bold red] Debe ingresar números enteros válidos. Cancelando actualización.")
            
            break
            
    if not pais_encontrado:
        console.print("[bold red]Error:[/bold red] No se encontró ningún país con ese nombre.")


# Busca países por coincidencia parcial o exacta en el nombre
def buscar_pais(lista_paises):
    console.print("\n[bold cyan]--- BUSCAR PAÍS ---[/bold cyan]")
    termino = quitar_tildes(input("Ingrese el nombre (o parte del nombre) del país: ").strip().lower())
    
    if termino == "":
        console.print("[bold red]Error:[/bold red] No ingresó ningún término de búsqueda.")
        return
        
    encontrados = []
    
    for pais in lista_paises:
        if termino in quitar_tildes(pais["nombre"].lower()):
            encontrados.append(pais)
            
    if len(encontrados) > 0:
        mostrar_tabla_paises(encontrados, f"COINCIDENCIAS PARA '{termino.upper()}'")
    else:
        console.print("[bold yellow]No se encontraron países que coincidan con su búsqueda.[/bold yellow]")


# Filtra la lista de países por continente, rango de población o rango de superficie
def filtrar_paises(lista_paises):
    console.print("\n[bold cyan]--- FILTRAR PAÍSES ---[/bold cyan]")
    
    opcion_filtro = questionary.select(
        "Elija un criterio de filtro:",
        choices=[
            "1. Por Continente",
            "2. Por Rango de Población",
            "3. Por Rango de Superficie",
            "Volver al menú"
        ]
    ).ask()

    if opcion_filtro is None or opcion_filtro == "Volver al menú":
        return

    encontrados = []
    
    if opcion_filtro.startswith("1."):
        continente_buscado = quitar_tildes(input("Ingrese el continente: ").strip().lower())
        if continente_buscado == "":
            console.print("[bold red]Error:[/bold red] Debe ingresar un continente válido.")
            return
        
        for pais in lista_paises:
            continente_pais = quitar_tildes(pais["continente"].lower())
            if continente_pais == continente_buscado:
                encontrados.append(pais)
                
    elif opcion_filtro.startswith("2."):
        try:
            min_pob = int(input("Ingrese la población mínima: "))
            max_pob = int(input("Ingrese la población máxima: "))
            if min_pob > max_pob:
                console.print("[bold red]Error:[/bold red] La población mínima no puede ser mayor que la máxima.")
                return
            for pais in lista_paises:
                if min_pob <= pais["poblacion"] <= max_pob:
                    encontrados.append(pais)
        except ValueError:
            console.print("[bold red]Error:[/bold red] Debe ingresar números enteros válidos.")
            return
            
    elif opcion_filtro.startswith("3."):
        try:
            min_sup = int(input("Ingrese la superficie mínima en km2: "))
            max_sup = int(input("Ingrese la superficie máxima en km2: "))
            if min_sup > max_sup:
                console.print("[bold red]Error:[/bold red] La superficie mínima no puede ser mayor que la máxima.")
                return
            for pais in lista_paises:
                if min_sup <= pais["superficie"] <= max_sup:
                    encontrados.append(pais)
        except ValueError:
            console.print("[bold red]Error:[/bold red] Debe ingresar números enteros válidos.")
            return

    if len(encontrados) > 0:
        mostrar_tabla_paises(encontrados, f"PAÍSES FILTRADOS ({len(encontrados)})")
    else:
        console.print("[bold yellow]No se encontraron países que cumplan con este filtro.[/bold yellow]")


# Ordena los países por nombre, población o superficie en sentido ascendente o descendente
def ordenar_paises(lista_paises):
    console.print("\n[bold cyan]--- ORDENAR PAÍSES ---[/bold cyan]")
    
    criterio = questionary.select(
        "Elija el criterio de ordenamiento:",
        choices=[
            "1. Por Nombre",
            "2. Por Población",
            "3. Por Superficie",
            "Volver al menú"
        ]
    ).ask()

    if criterio is None or criterio == "Volver al menú":
        return

    orden = questionary.select(
        "Elija el sentido del orden:",
        choices=[
            "1. Ascendente (Menor a Mayor / A-Z)",
            "2. Descendente (Mayor a Menor / Z-A)"
        ]
    ).ask()

    if orden is None:
        return
        
    reverso = True if orden.startswith("2.") else False
    
    if criterio.startswith("1."):
        lista_ordenada = sorted(lista_paises, key=lambda x: quitar_tildes(x["nombre"].lower()), reverse=reverso)
    elif criterio.startswith("2."):
        lista_ordenada = sorted(lista_paises, key=lambda x: x["poblacion"], reverse=reverso)
    elif criterio.startswith("3."):
        lista_ordenada = sorted(lista_paises, key=lambda x: x["superficie"], reverse=reverso)
        
    mostrar_tabla_paises(lista_ordenada, "PAÍSES ORDENADOS")


# Calcula y muestra estadísticas generales y cantidad de países por continente
def mostrar_estadisticas(lista_paises):
    if len(lista_paises) == 0:
        console.print("[bold yellow]No hay países cargados para calcular estadísticas.[/bold yellow]")
        return
        
    # Inicializamos acumuladores para sumas y un diccionario para contar países por continente
    total_poblacion = 0
    total_superficie = 0
    conteo_continentes = {}
    
    for pais in lista_paises:
        total_poblacion += pais["poblacion"]
        total_superficie += pais["superficie"]
        
        cont = pais["continente"]
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1
        else:
            conteo_continentes[cont] = 1
        
    promedio_poblacion = total_poblacion / len(lista_paises)
    promedio_superficie = total_superficie / len(lista_paises)
    
    # Buscamos el país con mayor y menor población usando max/min
    pais_max_pob = max(lista_paises, key=lambda x: x["poblacion"])
    pais_min_pob = min(lista_paises, key=lambda x: x["poblacion"])
    
    # Buscamos el país con mayor y menor superficie
    pais_max_sup = max(lista_paises, key=lambda x: x["superficie"])
    pais_min_sup = min(lista_paises, key=lambda x: x["superficie"])

    # Formateamos el desglose de países por continente
    detalle_continentes = ""
    for continente, cantidad in conteo_continentes.items():
        detalle_continentes += f"  • {continente}: {cantidad}\n"
    
    # Armamos el bloque de texto con estilos de Rich para mostrarlo dentro de un Panel
    resumen = (
        f"[bold]Cantidad total de países en el sistema:[/bold] {len(lista_paises)}\n"
        f"[bold]Población total combinada:[/bold] {total_poblacion:,} hab.\n"
        f"[bold]Población promedio:[/bold] {promedio_poblacion:,.2f} hab.\n"
        f"[bold]Superficie promedio:[/bold] {promedio_superficie:,.2f} km²\n\n"
        f"[bold green]▲ Mayor población:[/bold green] {pais_max_pob['nombre']} ({pais_max_pob['poblacion']:,} hab.)\n"
        f"[bold red]▼ Menor población:[/bold red] {pais_min_pob['nombre']} ({pais_min_pob['poblacion']:,} hab.)\n"
        f"[bold green]▲ Mayor superficie:[/bold green] {pais_max_sup['nombre']} ({pais_max_sup['superficie']:,} km²)\n"
        f"[bold red]▼ Menor superficie:[/bold red] {pais_min_sup['nombre']} ({pais_min_sup['superficie']:,} km²)\n\n"
        f"[bold cyan]Cantidad de países por continente:[/bold cyan]\n{detalle_continentes.rstrip()}"
    )

    console.print()
    console.print(Panel(resumen, title="[bold cyan]ESTADÍSTICAS DEL SISTEMA[/bold cyan]", border_style="cyan", expand=False))