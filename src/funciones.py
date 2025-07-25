import pandas as pd
import numpy as np
from clases import Estudiante, Becado

def registrar_estudiante(estudiantes, nombre, edad, carrera, notas, tiene_beca=False):
    """Registra un nuevo estudiante en el sistema."""
    if tiene_beca:
        estudiante = Becado(nombre, edad, carrera, notas)
    else:
        estudiante = Estudiante(nombre, edad, carrera, notas)
    estudiantes.append(estudiante)
    return estudiante

def buscar_estudiante(estudiantes, criterio, valor):
    """Busca estudiantes por nombre o carrera."""
    resultados = []
    for estudiante in estudiantes:
        if criterio == 'nombre' and valor.lower() in estudiante.nombre.lower():
            resultados.append(estudiante)
        elif criterio == 'carrera' and valor.lower() in estudiante.carrera.lower():
            resultados.append(estudiante)
    return resultados

def contar_aprobados_desaprobados(estudiantes):
    """Cuenta la cantidad de estudiantes aprobados y desaprobados."""
    aprobados = sum(1 for e in estudiantes if e.es_aprobado())
    desaprobados = len(estudiantes) - aprobados
    return aprobados, desaprobados

def generar_estadisticas(estudiantes):
    """Genera estadísticas usando pandas y numpy."""
    # Convertir datos a DataFrame
    datos = [e.mostrar_datos() for e in estudiantes]
    df = pd.DataFrame(datos)
    
    # Calcular estadísticas
    estadisticas = {
        'promedio_general': df['promedio'].mean(),
        'mediana': df['promedio'].median(),
        'moda': df['promedio'].mode().iloc[0] if not df['promedio'].mode().empty else 'N/A',
        'nota_maxima': df['promedio'].max(),
        'nota_minima': df['promedio'].min(),
        'desviacion_estandar': df['promedio'].std(),
        'total_estudiantes': len(estudiantes),
        'aprobados': sum(df['aprobado']),
        'desaprobados': len(estudiantes) - sum(df['aprobado'])
    }
    
    return estadisticas, df

def exportar_a_csv(estudiantes, nombre_archivo='estudiantes.csv'):
    """Exporta los datos de los estudiantes a un archivo CSV."""
    datos = [e.mostrar_datos() for e in estudiantes]
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
    return nombre_archivo

def cargar_desde_csv(nombre_archivo='estudiantes.csv'):
    """Carga datos desde un archivo CSV."""
    try:
        df = pd.read_csv(nombre_archivo)
        estudiantes = []
        for _, row in df.iterrows():
            notas = eval(row['notas'])  # Convertir string de lista a lista
            if row['tiene_beca']:
                estudiante = Becado(row['nombre'], row['edad'], row['carrera'], notas)
            else:
                estudiante = Estudiante(row['nombre'], row['edad'], row['carrera'], notas)
            estudiantes.append(estudiante)
        return estudiantes
    except FileNotFoundError:
        return []
