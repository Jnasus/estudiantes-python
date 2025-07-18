from funciones import *
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n=== MINI SISTEMA ACADÉMICO ===")
    print("1. Registrar nuevo estudiante")
    print("2. Buscar estudiante")
    print("3. Mostrar todos los estudiantes")
    print("4. Ver estadísticas")
    print("5. Exportar datos a CSV")
    print("6. Cargar datos desde CSV")
    print("7. Salir")
    return input("Seleccione una opción: ")

def registrar_estudiante_menu(estudiantes):
    print("\n=== REGISTRO DE ESTUDIANTE ===")
    nombre = input("Nombre: ")
    edad = int(input("Edad: "))
    carrera = input("Carrera: ")
    print("Ingrese las 3 notas:")
    notas = [float(input(f"Nota {i+1}: ")) for i in range(3)]
    tiene_beca = input("¿Tiene beca? (s/n): ").lower() == 's'
    
    estudiante = registrar_estudiante(estudiantes, nombre, edad, carrera, notas, tiene_beca)
    print(f"\nEstudiante registrado exitosamente: {estudiante.nombre}")

def buscar_estudiante_menu(estudiantes):
    print("\n=== BUSCAR ESTUDIANTE ===")
    print("1. Buscar por nombre")
    print("2. Buscar por carrera")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        nombre = input("Ingrese el nombre a buscar: ")
        resultados = buscar_estudiante(estudiantes, 'nombre', nombre)
    elif opcion == "2":
        carrera = input("Ingrese la carrera a buscar: ")
        resultados = buscar_estudiante(estudiantes, 'carrera', carrera)
    else:
        print("Opción no válida")
        return
    
    if resultados:
        print("\nResultados encontrados:")
        for e in resultados:
            datos = e.mostrar_datos()
            print(f"\nNombre: {datos['nombre']}")
            print(f"Carrera: {datos['carrera']}")
            print(f"Promedio: {datos['promedio']:.2f}")
            print(f"Estado: {'Aprobado' if datos['aprobado'] else 'Desaprobado'}")
    else:
        print("No se encontraron resultados")

def mostrar_estudiantes(estudiantes):
    print("\n=== LISTA DE ESTUDIANTES ===")
    if not estudiantes:
        print("No hay estudiantes registrados")
        return
    
    for e in estudiantes:
        datos = e.mostrar_datos()
        print(f"\nNombre: {datos['nombre']}")
        print(f"Edad: {datos['edad']}")
        print(f"Carrera: {datos['carrera']}")
        print(f"Notas: {datos['notas']}")
        print(f"Promedio: {datos['promedio']:.2f}")
        print(f"Estado: {'Aprobado' if datos['aprobado'] else 'Desaprobado'}")
        print(f"Beca: {'Sí' if datos['tiene_beca'] else 'No'}")

def mostrar_estadisticas(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados para generar estadísticas")
        return
    
    estadisticas, df = generar_estadisticas(estudiantes)
    
    print("\n=== ESTADÍSTICAS ===")
    print(f"Total de estudiantes: {estadisticas['total_estudiantes']}")
    print(f"Promedio general: {estadisticas['promedio_general']:.2f}")
    print(f"Mediana: {estadisticas['mediana']:.2f}")
    print(f"Moda: {estadisticas['moda']}")
    print(f"Nota máxima: {estadisticas['nota_maxima']:.2f}")
    print(f"Nota mínima: {estadisticas['nota_minima']:.2f}")
    print(f"Desviación estándar: {estadisticas['desviacion_estandar']:.2f}")
    print(f"Estudiantes aprobados: {estadisticas['aprobados']}")
    print(f"Estudiantes desaprobados: {estadisticas['desaprobados']}")

def main():
    estudiantes = []
    
    while True:
        opcion = mostrar_menu()
        limpiar_pantalla()
        
        if opcion == "1":
            registrar_estudiante_menu(estudiantes)
        elif opcion == "2":
            buscar_estudiante_menu(estudiantes)
        elif opcion == "3":
            mostrar_estudiantes(estudiantes)
        elif opcion == "4":
            mostrar_estadisticas(estudiantes)
        elif opcion == "5":
            archivo = exportar_a_csv(estudiantes)
            print(f"\nDatos exportados exitosamente a {archivo}")
        elif opcion == "6":
            estudiantes = cargar_desde_csv()
            print("\nDatos cargados exitosamente")
        elif opcion == "7":
            print("\n¡Gracias por usar el sistema!")
            break
        else:
            print("\nOpción no válida")
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()

if __name__ == "__main__":
    main()
