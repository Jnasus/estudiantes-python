# Mini Sistema Académico con Interfaz Gráfica

Este es un sistema de gestión académica desarrollado en Python, que cuenta con una interfaz gráfica moderna construida con `ttkbootstrap`. Permite administrar datos de estudiantes, realizar análisis estadísticos y visualizar información de manera intuitiva.

*(Sugerencia: Sería ideal añadir una captura de pantalla de la aplicación aquí)*

## ✨ Características Principales

- **Interfaz Gráfica Moderna:** Interfaz amigable y responsiva creada con `ttkbootstrap`.
- **Gestión Completa de Estudiantes:**
  - **CRUD Completo:** Registra, edita y elimina estudiantes directamente desde la tabla.
  - **Asignación Automática de Becas:** El sistema asigna becas al 20% de los estudiantes con mejores promedios (que hayan aprobado).
- **Visualización de Datos Avanzada:**
  - **Tabla Interactiva:** Muestra a los estudiantes en una tabla que se puede ordenar por cualquier columna.
  - **Filtros Dinámicos:** Filtra estudiantes por carrera, estado de aprobación o estado de beca.
  - **Badges Visuales:** Usa indicadores de color para identificar rápidamente el estado de aprobación y beca.
- **Análisis Estadístico y Gráficos:**
  - **Cálculo de Estadísticas:** Usa `pandas` para calcular promedio general, nota máxima/mínima y desviación estándar.
  - **Gráficos Dinámicos:** Genera un gráfico de barras con `matplotlib` para visualizar los promedios.
- **Gestión de Carreras:** Permite agregar o eliminar carreras dinámicamente.
- **Importación y Exportación:** Guarda y carga datos de estudiantes en formato CSV.

## 🛠️ Tecnologías y Librerías

- **Python 3.6+**
- **ttkbootstrap:** Para la creación de la interfaz gráfica.
- **pandas:** Para la manipulación y análisis de datos.
- **numpy:** Para cálculos numéricos (dependencia de pandas).
- **matplotlib:** Para la generación de gráficos.
- **Pillow (PIL):** Para el manejo de las imágenes de los iconos.

## 🚀 Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Jnasus/estudiantes-python.git
    cd estudiantes-python
    ```
2.  **(Recomendado) Crear un entorno virtual:**
    ```bash
    python -m venv .venv
    # Activar en Windows: .venv\Scripts\activate
    # Activar en macOS/Linux: source .venv/bin/activate
    ```
3.  **Instalar todas las dependencias con un solo comando:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Uso

Una vez instaladas las dependencias, ejecuta el programa desde el directorio raíz del proyecto:
```bash
python src/main.py
```

## 📂 Estructura del Proyecto

- `src/`: Carpeta que contiene todo el código fuente de la aplicación.
  - `main.py`: Punto de entrada que inicia la aplicación.
  - `interfaz.py`: Define toda la interfaz gráfica y su lógica.
  - `funciones.py`: Funciones de backend (lógica de negocio).
  - `clases.py`: Clases `Estudiante` y `Becado`.
- `assets/`: Carpeta con los iconos y logos utilizados en la interfaz.
- `requirements.txt`: Lista de todas las dependencias de Python para el proyecto.
- `.gitignore`: Archivo que especifica qué archivos y carpetas ignorar en Git.
- `estudiantes.csv`: Archivo de datos por defecto (generado por la app, ignorado por Git).
- `README.md`: Este archivo de documentación.
