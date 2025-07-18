# Mini Sistema Académico con Análisis de Datos

Este es un sistema académico desarrollado en Python que permite gestionar datos de estudiantes y realizar análisis estadísticos.

## Características

- Registro de estudiantes con nombre, edad, carrera y notas
- Soporte para estudiantes becados
- Cálculo de promedios individuales y generales
- Verificación de aprobación (nota mínima 13)
- Búsqueda de estudiantes por nombre o carrera
- Análisis estadístico usando pandas y numpy
- Exportación e importación de datos en formato CSV

## Requisitos

- Python 3.6 o superior
- pandas
- numpy

## Instalación

1. Clonar o descargar este repositorio
2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar el programa principal:
```bash
python main.py
```

2. Seguir las instrucciones del menú para:
   - Registrar nuevos estudiantes
   - Buscar estudiantes
   - Ver estadísticas
   - Exportar/importar datos

## Estructura del Proyecto

- `main.py`: Programa principal con la interfaz de usuario
- `clases.py`: Definición de las clases Estudiante y Becado
- `funciones.py`: Funciones de utilidad y análisis de datos
- `requirements.txt`: Dependencias del proyecto

## Funcionalidades

1. **Registro de Estudiantes**
   - Nombre
   - Edad
   - Carrera
   - 3 notas
   - Estado de beca

2. **Procesamiento**
   - Cálculo de promedios
   - Verificación de aprobación
   - Búsqueda de estudiantes
   - Estadísticas generales

3. **Análisis de Datos**
   - Promedio general
   - Nota máxima y mínima
   - Desviación estándar
   - Exportación a CSV

## Contribución

Este proyecto fue desarrollado como trabajo final para el curso de Lenguaje de Programación. 