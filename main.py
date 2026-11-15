import os
import questionary
from rich.console import Console
from rich.panel import Panel
# Importa las funciones 
from funciones import (
    cargar_datos, agregar_pais, actualizar_pais, 
    buscar_pais, filtrar_paises, ordenar_paises, 
    mostrar_estadisticas, mostrar_tabla_paises, ESTILO_MENU
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
    
    # 2. Bucle para mantener el menú activo
    while True:
        limpiar_pantalla()
        # Muestra el título principal y el estado del sistema dentro de un panel con Rich
        console.print(Panel.fit(
            f"[bold cyan]🌍 SISTEMA DE GESTIÓN DE PAÍSES[/bold cyan]\n"
            f"[dim]Base de datos activa: [bold white]{len(paises)}[/bold white] países registrados[/dim]",
            border_style="bright_blue",
            padding=(1, 4)
        ))
        
        # Menú interactivo con flechas del teclado usando Questionary
        opcion = questionary.select(
            "Use las flechas para navegar y Enter para seleccionar:",
            choices=[
                questionary.Separator("── Gestión de Datos ──"),
                "1. ➕ Agregar un país",
                "2. 📋 Ver países cargados",
                "3. ✏️  Actualizar datos de un país",
                questionary.Separator("── Consultas y Análisis ──"),
                "4. 🔍 Buscar un país",
                "5. 🌪️  Filtrar países",
                "6. 📊 Ordenar países",
                "7. 📈 Ver estadísticas",
                questionary.Separator("── Sistema ──"),
                "8. 🚪 Salir"
            ],
            instruction=" ",
            style=ESTILO_MENU
        ).ask()
        
        # Evalua la opción elegida
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

if __name__ == "__main__":
    menu_principal()