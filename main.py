import os
import questionary
from rich.console import Console
from rich.panel import Panel
# Importamos las funciones 
from funciones import (
    cargar_datos, agregar_pais, actualizar_pais, 
    buscar_pais, filtrar_paises, ordenar_paises, 
    mostrar_estadisticas, mostrar_tabla_paises
)

# Inicializa la consola de Rich para los títulos y mensajes
console = Console()

# Limpia la consola 
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# Carga los datos iniciales y ejecuta el bucle principal del menú interactivo
def menu_principal():
    # 1. Carga los datos en memoria apenas arranca el programa
    paises = cargar_datos()
    
    # 2. Bucle infinito para mantener el menú activo
    while True:
        limpiar_pantalla()
        # Muestra el título principal dentro de un panel con Rich
        console.print(Panel.fit("[bold cyan]SISTEMA DE GESTIÓN DE PAÍSES[/bold cyan]", border_style="blue"))
        
        # Menú interactivo navegable con flechas del teclado usando Questionary
        opcion = questionary.select(
            "Use las flechas para navegar y Enter para seleccionar:",
            choices=[
                "1. Agregar un país",
                "2. Ver países cargados",
                "3. Actualizar datos de un país",
                "4. Buscar un país",
                "5. Filtrar países",
                "6. Ordenar países",
                "7. Ver estadísticas",
                "8. Salir"
            ]
        ).ask()
        
        # Evalua la opción elegida según el prefijo numérico
        if opcion is None or opcion.startswith("8."):
            console.print("\n[bold yellow]Saliendo del sistema...[/bold yellow]")
            break
        elif opcion.startswith("1."):
            agregar_pais(paises)
        elif opcion.startswith("2."):
            mostrar_tabla_paises(paises, "PAÍSES CARGADOS EN EL SISTEMA")
        elif opcion.startswith("3."):
            actualizar_pais(paises)
        elif opcion.startswith("4."):
            buscar_pais(paises)
        elif opcion.startswith("5."):
            filtrar_paises(paises)
        elif opcion.startswith("6."):
            ordenar_paises(paises)
        elif opcion.startswith("7."):
            mostrar_estadisticas(paises)
            
        # Pausa para que el usuario pueda leer el resultado antes de limpiar y volver al menú
        input("\nPresione Enter para continuar...")

# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()