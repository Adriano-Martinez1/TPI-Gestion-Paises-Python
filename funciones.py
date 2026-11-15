import csv
import os
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Inicializa la consola de Rich para imprimir con colores, tablas y paneles
console = Console()

# Calcula la ruta exacta de la carpeta donde está guardado el archivo (funciones.py)
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "paises.csv")

# Tupla con los continentes válidos para evitar errores de tipeo
CONTINENTES_VALIDOS = ("América", "Europa", "Asia", "África", "Oceanía")

# Estilo visual para resaltar la línea seleccionada y los separadores en los menús de Questionary
ESTILO_MENU = questionary.Style([
    ("qmark", "fg:#00ffff bold"),
    ("question", "bold"),
    ("pointer", "fg:#00ffff bold"),
    ("highlighted", "bg:#005f87 fg:#ffffff bold"),
    ("selected", "fg:#00ffff bold"),
    ("separator", "fg:#5f87af"),
])


# Reemplaza las vocales con tilde por vocales sin tilde para evitar fallos en búsquedas y filtros
def quitar_tildes(texto):
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for con_tilde, sin_tilde in reemplazos:
        texto = texto.replace(con_tilde, sin_tilde)
    return texto


# Verifica que el texto contenga solo letras y espacios/guiones válidos
def es_texto_valido(texto):
    tiene_letras = False
    for caracter in texto:
        if caracter.isalpha():
            tiene_letras = True
        elif caracter not in (" ", "-", "."):
            return False
    return tiene_letras


# Solicita un texto no vacío por consola; devuelve None si se ingresa "0" para cancelar
def pedir_texto(mensaje, solo_letras=False):
    while True:
        entrada = input(mensaje).strip()
        if entrada == "0":
            console.print("[bold yellow]Operación cancelada. Volviendo al menú principal...[/bold yellow]")
            return None
        if entrada == "":
            console.print("[bold red]Error:[/bold red] El campo no puede estar vacío.")
            continue
        if solo_letras and not es_texto_valido(entrada):
            console.print("[bold red]Error:[/bold red] Debe contener solo letras.")
            continue
        return entrada


# Solicita un número entero mayor o igual a 'minimo'; devuelve None si se ingresa "0" para cancelar
def pedir_entero(mensaje, minimo=1):
    while True:
        entrada = input(mensaje).strip()
        if entrada == "0":
            console.print("[bold yellow]Operación cancelada. Volviendo al menú principal...[/bold yellow]")
            return None
        try:
            valor = int(entrada)
            if valor < minimo:
                console.print(f"[bold red]Error:[/bold red] El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            console.print("[bold red]Error:[/bold red] Ingrese un número entero válido sin letras ni puntos.")


# Busca un país por coincidencia exacta (ignorando tildes y mayúsculas) y devuelve su diccionario o None
def obtener_pais_exacto(lista_paises, nombre):
    nombre_normalizado = quitar_tildes(nombre.lower())
    for pais in lista_paises:
        if quitar_tildes(pais["nombre"].lower()) == nombre_normalizado:
            return pais
    return None


# Muestra cualquier lista de países en una tabla formateada con Rich
def mostrar_tabla_paises(lista, titulo="LISTADO DE PAÍSES"):
    if len(lista) == 0:
        console.print("[bold yellow]No hay países para mostrar.[/bold yellow]")
        return

    tabla = Table(title=titulo, show_header=True, header_style="bold magenta", border_style="bright_blue")
    tabla.add_column("País", style="bold cyan", no_wrap=True)
    tabla.add_column("Continente", style="green")
    tabla.add_column("Población", justify="right", style="white")
    tabla.add_column("Superficie (km²)", justify="right", style="white")

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
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            
            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    if not es_texto_valido(nombre) or not es_texto_valido(continente):
                        raise ValueError("Campos de texto inválidos o vacíos")

                    poblacion = int(fila["poblacion"])
                    superficie = int(fila["superficie"])
                    if poblacion <= 0 or superficie <= 0:
                        raise ValueError("Valores numéricos no positivos")

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
        encabezados = ["nombre", "poblacion", "superficie", "continente"]
        with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(lista_paises)
    except PermissionError:
        console.print("[bold red]Error:[/bold red] El archivo está abierto en otro programa. Ciérrelo para poder guardar.")
    except Exception as e:
        console.print(f"[bold red]Ocurrió un error inesperado al guardar:[/bold red] {e}")


# Solicita los datos de un nuevo país, valida las entradas y lo persiste en el CSV
def agregar_pais(lista_paises):
    console.print("\n[bold cyan]--- AGREGAR NUEVO PAÍS ---[/bold cyan]")
    console.print("[yellow]Escriba [bold cyan]0[/bold cyan] en cualquier campo para cancelar y volver al menú.[/yellow]")
    
    # 1. Valida el nombre y la verificación de duplicados
    while True:
        nombre = pedir_texto("Ingrese el nombre del país: ", solo_letras=True)
        if nombre is None:
            return
        existente = obtener_pais_exacto(lista_paises, nombre)
        if existente is not None:
            console.print(f"[bold red]Error:[/bold red] El país '{existente['nombre']}' ya existe.")
            continue
        break

    # 2. Selección de continente válido con Questionary
    continente = questionary.select(
        "Seleccione el continente:",
        choices=list(CONTINENTES_VALIDOS) + [questionary.Separator("──"), "Cancelar y volver al menú"],
        instruction=" ",
        style=ESTILO_MENU
    ).ask()

    if continente is None or continente == "Cancelar y volver al menú":
        console.print("[bold yellow]Operación cancelada. Volviendo al menú principal...[/bold yellow]")
        return

    # 3. Validación de población y superficie
    poblacion = pedir_entero("Ingrese la población: ", minimo=1)
    if poblacion is None:
        return

    superficie = pedir_entero("Ingrese la superficie en km2: ", minimo=1)
    if superficie is None:
        return

    # 4. Guardado en memoria y disco
    lista_paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })
    guardar_datos(lista_paises)
    console.print(f"[bold green]¡Éxito![/bold green] El país '[cyan]{nombre}[/cyan]' se agregó correctamente.")


# Busca un país por nombre y actualiza su población y superficie
def actualizar_pais(lista_paises):
    console.print("\n[bold cyan]--- ACTUALIZAR PAÍS ---[/bold cyan]")
    console.print("[yellow]Escriba [bold cyan]0[/bold cyan] en cualquier campo para cancelar y volver al menú.[/yellow]")

    while True:
        entrada = pedir_texto("Ingrese el nombre del país que desea actualizar: ")
        if entrada is None:
            return
        pais_obj = obtener_pais_exacto(lista_paises, entrada)
        if pais_obj is None:
            console.print("[bold red]Error:[/bold red] No se encontró ningún país con ese nombre.")
            continue
        break

    console.print(f"País encontrado: [bold cyan]{pais_obj['nombre']}[/bold cyan] | Población actual: {pais_obj['poblacion']:,} | Superficie: {pais_obj['superficie']:,} km²")

    nueva_poblacion = pedir_entero("Ingrese la nueva población: ", minimo=1)
    if nueva_poblacion is None:
        return

    nueva_superficie = pedir_entero("Ingrese la nueva superficie en km2: ", minimo=1)
    if nueva_superficie is None:
        return

    pais_obj["poblacion"] = nueva_poblacion
    pais_obj["superficie"] = nueva_superficie
    guardar_datos(lista_paises)
    console.print("[bold green]¡Éxito![/bold green] Los datos fueron actualizados correctamente.")


# Busca países por coincidencia parcial o exacta en el nombre
def buscar_pais(lista_paises):
    console.print("\n[bold cyan]--- BUSCAR PAÍS ---[/bold cyan]")
    console.print("[yellow]Escriba [bold cyan]0[/bold cyan] para cancelar y volver al menú.[/yellow]")

    entrada = pedir_texto("Ingrese el nombre (o parte del nombre) del país: ")
    if entrada is None:
        return

    termino = quitar_tildes(entrada.lower())
    encontrados = [p for p in lista_paises if termino in quitar_tildes(p["nombre"].lower())]
            
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
            questionary.Separator("──"),
            "Volver al menú"
        ],
        instruction=" ",
        style=ESTILO_MENU
    ).ask()

    if opcion_filtro is None or opcion_filtro == "Volver al menú":
        console.print("[bold yellow]Operación cancelada. Volviendo al menú principal...[/bold yellow]")
        return

    encontrados = []
    
    if opcion_filtro.startswith("1."):
        continente_elegido = questionary.select(
            "Seleccione el continente a filtrar:",
            choices=list(CONTINENTES_VALIDOS) + [questionary.Separator("──"), "Cancelar y volver al menú"],
            instruction=" ",
            style=ESTILO_MENU
        ).ask()

        if continente_elegido is None or continente_elegido == "Cancelar y volver al menú":
            console.print("[bold yellow]Operación cancelada. Volviendo al menú principal...[/bold yellow]")
            return
        
        continente_buscado = quitar_tildes(continente_elegido.lower())
        encontrados = [p for p in lista_paises if quitar_tildes(p["continente"].lower()) == continente_buscado]
                
    else:
        # Unifica el filtrado por rango numérico para población y superficie
        es_poblacion = opcion_filtro.startswith("2.")
        campo = "poblacion" if es_poblacion else "superficie"
        etiqueta = "población" if es_poblacion else "superficie en km2"

        console.print("[yellow]Escriba [bold cyan]0[/bold cyan] en cualquier campo para cancelar y volver al menú.[/yellow]")
        minimo = pedir_entero(f"Ingrese la {etiqueta} mínima: ", minimo=1)
        if minimo is None:
            return

        maximo = pedir_entero(f"Ingrese la {etiqueta} máxima: ", minimo=minimo)
        if maximo is None:
            return

        encontrados = [p for p in lista_paises if minimo <= p[campo] <= maximo]

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
            questionary.Separator("──"),
            "Volver al menú"
        ],
        instruction=" ",
        style=ESTILO_MENU
    ).ask()

    if criterio is None or criterio == "Volver al menú":
        console.print("[bold yellow]Operación cancelada. Volviendo al menú principal...[/bold yellow]")
        return

    orden = questionary.select(
        "Elija el sentido del orden:",
        choices=[
            "1. Ascendente (Menor a Mayor / A-Z)",
            "2. Descendente (Mayor a Menor / Z-A)"
        ],
        instruction=" ",
        style=ESTILO_MENU
    ).ask()

    if orden is None:
        return
        
    reverso = orden.startswith("2.")
    
    if criterio.startswith("1."):
        lista_ordenada = sorted(lista_paises, key=lambda x: quitar_tildes(x["nombre"].lower()), reverse=reverso)
    elif criterio.startswith("2."):
        lista_ordenada = sorted(lista_paises, key=lambda x: x["poblacion"], reverse=reverso)
    else:
        lista_ordenada = sorted(lista_paises, key=lambda x: x["superficie"], reverse=reverso)
        
    mostrar_tabla_paises(lista_ordenada, "PAÍSES ORDENADOS")


# Calcula y muestra estadísticas generales y cantidad de países por continente
def mostrar_estadisticas(lista_paises):
    if len(lista_paises) == 0:
        console.print("[bold yellow]No hay países cargados para calcular estadísticas.[/bold yellow]")
        return
        
    total_poblacion = 0
    total_superficie = 0
    conteo_continentes = {}
    
    for pais in lista_paises:
        total_poblacion += pais["poblacion"]
        total_superficie += pais["superficie"]
        cont = pais["continente"]
        conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1
        
    promedio_poblacion = total_poblacion / len(lista_paises)
    promedio_superficie = total_superficie / len(lista_paises)
    
    pais_max_pob = max(lista_paises, key=lambda x: x["poblacion"])
    pais_min_pob = min(lista_paises, key=lambda x: x["poblacion"])
    pais_max_sup = max(lista_paises, key=lambda x: x["superficie"])
    pais_min_sup = min(lista_paises, key=lambda x: x["superficie"])

    detalle_continentes = "".join(f"  • {cont}: {cant}\n" for cont, cant in conteo_continentes.items())
    
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