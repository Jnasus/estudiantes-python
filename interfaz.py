import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
from funciones import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

# Paleta de colores para badges y gráficos
BADGE_APROBADO = '#51cf66'  # verde
BADGE_DESAPROBADO = '#ff6b6b'  # rojo
BADGE_BECA = '#339af0'  # azul
BADGE_NOBECA = '#adb5bd'  # gris
GRAFICO_COLORES = ['#339af0', '#51cf66', '#ffbe76', '#ff6b6b', '#845ef7', '#f783ac']

ICONOS = {
    'registrar': 'icon_registrar.png',
    'buscar': 'icon_buscar.png',
    'mostrar': 'icon_mostrar.png',
    'estadisticas': 'icon_estadisticas.png',
    'exportar': 'icon_exportar.png',
    'importar': 'icon_importar.png',
    'carreras': 'icon_carreras.png',
    'salir': 'icon_salir.png',
}

class SistemaAcademicoApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Mini Sistema Académico")
        self.geometry("1050x650")
        self.resizable(False, False)
        self.estudiantes = []
        self.carreras = ["Ing. Sistemas", "Ing. Industrial", "Administración", "Contabilidad"]
        self.iconos = self._cargar_iconos()
        self._crear_widgets()

    def _cargar_iconos(self):
        iconos = {}
        for key, filename in ICONOS.items():
            if os.path.exists(filename):
                img = Image.open(filename).resize((22, 22))
                iconos[key] = ImageTk.PhotoImage(img)
            else:
                iconos[key] = None
        return iconos

    def _crear_widgets(self):
        # Título
        titulo = tb.Label(self, text="Mini Sistema Académico", font=("Segoe UI", 28, "bold"), bootstyle=PRIMARY)
        titulo.pack(pady=10)

        # Frame de botones
        frame_botones = tb.Frame(self)
        frame_botones.pack(pady=10)
        self._crear_boton(frame_botones, "Registrar Estudiante", self.registrar_estudiante, 0, 0, 'registrar', SUCCESS, "Registrar un nuevo estudiante")
        self._crear_boton(frame_botones, "Buscar Estudiante", self.buscar_estudiante, 0, 1, 'buscar', INFO, "Buscar estudiante por nombre o carrera")
        self._crear_boton(frame_botones, "Mostrar Todos", self.mostrar_estudiantes, 0, 2, 'mostrar', SECONDARY, "Mostrar todos los estudiantes")
        self._crear_boton(frame_botones, "Ver Estadísticas", self.mostrar_estadisticas, 0, 3, 'estadisticas', WARNING, "Ver estadísticas y gráfico")
        self._crear_boton(frame_botones, "Exportar a CSV", self.exportar_csv, 1, 0, 'exportar', OUTLINE, "Exportar datos a archivo CSV")
        self._crear_boton(frame_botones, "Importar desde CSV", self.importar_csv, 1, 1, 'importar', OUTLINE, "Importar datos desde archivo CSV")
        self._crear_boton(frame_botones, "Gestionar Carreras", self.gestionar_carreras, 1, 2, 'carreras', PRIMARY, "Agregar o eliminar carreras")
        self._crear_boton(frame_botones, "Salir", self.quit, 1, 3, 'salir', DANGER, "Cerrar el sistema")

        # Tabla de estudiantes
        style = tb.Style()
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 11), padding=4)
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#e9ecef")
        style.map("Treeview", background=[('selected', '#b8daff')])

        self.tree = tb.Treeview(self, columns=("Nombre", "Edad", "Carrera", "Notas", "Promedio", "Aprobado", "Beca"), show="headings", bootstyle=INFO, selectmode="browse")
        col_widths = {
            "Nombre": 160,
            "Edad": 70,
            "Carrera": 160,
            "Notas": 240,
            "Promedio": 100,
            "Aprobado": 110,
            "Beca": 90
        }
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor="center", minwidth=col_widths[col])
        self.tree.pack(expand=True, fill="both", pady=10, padx=10)
        self.tree.tag_configure('oddrow', background='#f8f9fa')
        self.tree.tag_configure('evenrow', background='#dee2e6')

        # Filtros
        frame_filtros = tb.Frame(self)
        frame_filtros.pack(pady=5)
        tb.Label(frame_filtros, text="Filtrar por:").grid(row=0, column=0, padx=5)
        self.filtro_carrera = tb.Combobox(frame_filtros, values=["Todas"] + self.carreras, state="readonly", width=18)
        self.filtro_carrera.set("Todas")
        self.filtro_carrera.grid(row=0, column=1, padx=5)
        self.filtro_estado = tb.Combobox(frame_filtros, values=["Todos", "Aprobado", "Desaprobado"], state="readonly", width=14)
        self.filtro_estado.set("Todos")
        self.filtro_estado.grid(row=0, column=2, padx=5)
        self.filtro_beca = tb.Combobox(frame_filtros, values=["Todos", "Con beca", "Sin beca"], state="readonly", width=14)
        self.filtro_beca.set("Todos")
        self.filtro_beca.grid(row=0, column=3, padx=5)
        tb.Button(frame_filtros, text="Aplicar Filtros", bootstyle=PRIMARY, command=self.aplicar_filtros).grid(row=0, column=4, padx=5)
        tb.Button(frame_filtros, text="Limpiar Filtros", bootstyle=SECONDARY, command=self.limpiar_filtros).grid(row=0, column=5, padx=5)

        # Ordenamiento por columna
        self.orden_columna = None
        self.orden_ascendente = True
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.ordenar_por_columna(c))

        # Botones de edición y eliminación
        frame_edicion = tb.Frame(self)
        frame_edicion.pack(pady=5)
        btn_editar = tb.Button(frame_edicion, text="Editar Estudiante", bootstyle=INFO, command=self.editar_estudiante)
        btn_editar.grid(row=0, column=0, padx=10)
        btn_eliminar = tb.Button(frame_edicion, text="Eliminar Estudiante", bootstyle=DANGER, command=self.eliminar_estudiante)
        btn_eliminar.grid(row=0, column=1, padx=10)

    def _crear_boton(self, frame, texto, comando, fila, columna, icono, estilo, tooltip):
        btn = tb.Button(frame, text=texto, width=22, bootstyle=estilo, command=comando, image=self.iconos[icono], compound=LEFT)
        btn.grid(row=fila, column=columna, padx=5, pady=5)
        self._add_tooltip(btn, tooltip)

    def _add_tooltip(self, widget, text):
        def on_enter(e):
            self.tooltip = tb.Tooltip(widget, text=text, bootstyle=INFO, delay=100)
            self.tooltip.show()
        def on_leave(e):
            if hasattr(self, 'tooltip'):
                self.tooltip.hide()
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def registrar_estudiante(self):
        win = tb.Toplevel(self)
        win.title("Registrar Estudiante")
        win.geometry("420x420+{}+{}".format(self.winfo_x()+300, self.winfo_y()+120))
        win.resizable(False, False)
        win.grab_set()
        win.attributes('-topmost', True)
        win.after(10, lambda: win.focus_force())
        win.configure(borderwidth=2, relief="ridge")

        tb.Label(win, text="Nombre:").pack(pady=5)
        entry_nombre = tb.Entry(win)
        entry_nombre.pack()
        tb.Label(win, text="Edad:").pack(pady=5)
        entry_edad = tb.Entry(win)
        entry_edad.pack()
        tb.Label(win, text="Carrera:").pack(pady=5)
        carrera_var = tb.StringVar(value=self.carreras[0])
        combo_carrera = tb.Combobox(win, textvariable=carrera_var, values=self.carreras, state="readonly")
        combo_carrera.pack()
        tb.Label(win, text="Notas (separadas por '|'):").pack(pady=5)
        entry_notas = tb.Entry(win)
        entry_notas.pack()

        def guardar():
            try:
                nombre = entry_nombre.get()
                edad = int(entry_edad.get())
                carrera = carrera_var.get()
                notas_strs = [n.strip() for n in entry_notas.get().split("|") if n.strip()]
                if len(notas_strs) != 3:
                    raise ValueError("Por favor, ingrese exactamente 3 notas, separadas por '|'. Ejemplo: 15|18|20")
                notas = []
                for n in notas_strs:
                    try:
                        notas.append(float(n))
                    except ValueError:
                        raise ValueError("Por favor, ingrese solo valores numéricos para las notas, separados por '|'. Ejemplo: 15|18|20")
                estudiante = registrar_estudiante(self.estudiantes, nombre, edad, carrera, notas, False)
                self._actualizar_becas()
                messagebox.showinfo("Éxito", f"Estudiante {nombre} registrado.", parent=win)
                win.destroy()
                self.mostrar_estudiantes()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        tb.Button(win, text="Guardar", bootstyle=SUCCESS, command=guardar).pack(pady=15)

    def buscar_estudiante(self):
        criterio = simpledialog.askstring("Buscar", "Buscar por (nombre/carrera):", parent=self)
        if not criterio or criterio.lower() not in ["nombre", "carrera"]:
            messagebox.showerror("Error", "Criterio inválido.", parent=self)
            return
        valor = simpledialog.askstring("Buscar", f"Ingrese el {criterio} a buscar:", parent=self)
        if not valor:
            return
        resultados = buscar_estudiante(self.estudiantes, criterio.lower(), valor)
        self._actualizar_tabla(resultados)
        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron estudiantes.", parent=self)

    def mostrar_estudiantes(self):
        self._actualizar_tabla(self.estudiantes)

    def mostrar_estadisticas(self):
        if not self.estudiantes:
            messagebox.showinfo("Estadísticas", "No hay estudiantes registrados.", parent=self)
            return
        estadisticas, df = generar_estadisticas(self.estudiantes)
        win = tb.Toplevel(self)
        win.title("Estadísticas")
        win.geometry("900x600+{}+{}".format(self.winfo_x()+100, self.winfo_y()+60))
        win.grab_set()
        win.attributes('-topmost', True)
        win.after(10, lambda: win.focus_force())
        win.configure(borderwidth=2, relief="ridge")
        tb.Label(win, text="Estadísticas Generales", font=("Segoe UI", 18, "bold"), bootstyle=PRIMARY).pack(pady=10)
        # Mostrar estadísticas en tabla visual
        stats_frame = tb.Frame(win)
        stats_frame.pack(pady=5)
        stats_table = tb.Treeview(stats_frame, columns=("Métrica", "Valor"), show="headings", height=7, bootstyle=INFO)
        stats_table.heading("Métrica", text="Metric")
        stats_table.heading("Valor", text="Value")
        stats_table.column("Métrica", width=200, anchor="w")
        stats_table.column("Valor", width=120, anchor="center")
        stats = [
            ("Total students", estadisticas['total_estudiantes']),
            ("Average grade", f"{estadisticas['promedio_general']:.2f}"),
            ("Max grade", f"{estadisticas['nota_maxima']:.2f}"),
            ("Min grade", f"{estadisticas['nota_minima']:.2f}"),
            ("Std deviation", f"{estadisticas['desviacion_estandar']:.2f}"),
            ("Approved", estadisticas['aprobados']),
            ("Not approved", estadisticas['desaprobados'])
        ]
        for metric, value in stats:
            stats_table.insert("", "end", values=(metric, value))
        stats_table.pack()
        # Gráfico de barras de promedios compacto y adaptable
        n = len(self.estudiantes)
        fig_width = max(4, min(1.1 * n + 2, 8))  # Ajusta el ancho según la cantidad de estudiantes
        fig, ax = plt.subplots(figsize=(fig_width, 2.2))
        nombres = [e.nombre for e in self.estudiantes]
        promedios = [e.calcular_promedio() for e in self.estudiantes]
        colores = [GRAFICO_COLORES[i % len(GRAFICO_COLORES)] for i in range(len(nombres))]
        bars = ax.bar(nombres, promedios, color=colores, edgecolor='#22223b', linewidth=1.5)
        ax.set_ylabel('Promedio', fontsize=11)
        ax.set_title('Promedio por Estudiante', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 21)
        plt.xticks(rotation=25, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        for bar, promedio in zip(bars, promedios):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{promedio:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill='both', expand=True)

    def exportar_csv(self):
        if not self.estudiantes:
            messagebox.showinfo("Exportar", "No hay estudiantes para exportar.", parent=self)
            return
        archivo = exportar_a_csv(self.estudiantes)
        messagebox.showinfo("Exportar", f"Datos exportados a {archivo}", parent=self)

    def importar_csv(self):
        self.estudiantes = cargar_desde_csv()
        self._actualizar_becas()
        self.mostrar_estudiantes()
        messagebox.showinfo("Importar", "Datos importados desde estudiantes.csv", parent=self)

    def gestionar_carreras(self):
        win = tb.Toplevel(self)
        win.title("Gestionar Carreras")
        win.geometry("370x370+{}+{}".format(self.winfo_x()+350, self.winfo_y()+120))
        win.grab_set()
        win.attributes('-topmost', True)
        win.after(10, lambda: win.focus_force())
        win.configure(borderwidth=2, relief="ridge")
        tb.Label(win, text="Carreras Registradas", font=("Segoe UI", 15, "bold"), bootstyle=PRIMARY).pack(pady=10)
        lista = tb.Listbox(win, height=8)
        lista.pack(pady=5, fill="x", padx=10)
        for c in self.carreras:
            lista.insert("end", c)
        entry = tb.Entry(win)
        entry.pack(pady=5)
        def agregar():
            val = entry.get().strip()
            if val and val not in self.carreras:
                self.carreras.append(val)
                lista.insert("end", val)
                entry.delete(0, "end")
        def eliminar():
            sel = lista.curselection()
            if sel:
                idx = sel[0]
                carrera = lista.get(idx)
                if carrera in self.carreras:
                    self.carreras.remove(carrera)
                    lista.delete(idx)
        tb.Button(win, text="Agregar", bootstyle=SUCCESS, command=agregar).pack(side="left", padx=10, pady=10)
        tb.Button(win, text="Eliminar", bootstyle=DANGER, command=eliminar).pack(side="right", padx=10, pady=10)

    def _actualizar_tabla(self, lista):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, e in enumerate(lista):
            datos = e.mostrar_datos()
            # Formatear notas a dos decimales y alineadas
            notas_str = " | ".join(f"{n:05.2f}" for n in datos['notas'])
            # Badge para aprobado
            aprobado = datos['aprobado']
            badge_aprobado = f"\u25CF Sí" if aprobado else f"\u25CF No"
            # Badge para beca
            beca = datos['tiene_beca']
            badge_beca = f"\u2605 Sí" if beca else f"\u2606 No"
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(
                datos['nombre'], datos['edad'], datos['carrera'],
                notas_str, f"{datos['promedio']:.2f}",
                badge_aprobado, badge_beca
            ), tags=(tag,))

    def _actualizar_becas(self):
        if not self.estudiantes:
            return
        # Solo aprobados pueden tener beca
        aprobados = [e for e in self.estudiantes if e.es_aprobado()]
        if not aprobados:
            for e in self.estudiantes:
                e.tiene_beca = False
            return
        # Ordenar aprobados por promedio descendente
        ordenados = sorted(aprobados, key=lambda e: e.calcular_promedio(), reverse=True)
        top_20 = max(1, len(ordenados)//5)
        for i, e in enumerate(ordenados):
            e.tiene_beca = i < top_20
        # Los no aprobados no tienen beca
        for e in self.estudiantes:
            if not e.es_aprobado():
                e.tiene_beca = False

    def editar_estudiante(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Editar", "Seleccione un estudiante para editar.", parent=self)
            return
        idx = self.tree.index(selected[0])
        estudiante = self.estudiantes[idx]
        win = tb.Toplevel(self)
        win.title("Editar Estudiante")
        win.geometry("420x420+{}+{}".format(self.winfo_x()+300, self.winfo_y()+120))
        win.resizable(False, False)
        win.grab_set()
        win.attributes('-topmost', True)
        win.after(10, lambda: win.focus_force())
        win.configure(borderwidth=2, relief="ridge")

        tb.Label(win, text="Nombre:").pack(pady=5)
        entry_nombre = tb.Entry(win)
        entry_nombre.insert(0, estudiante.nombre)
        entry_nombre.pack()
        tb.Label(win, text="Edad:").pack(pady=5)
        entry_edad = tb.Entry(win)
        entry_edad.insert(0, str(estudiante.edad))
        entry_edad.pack()
        tb.Label(win, text="Carrera:").pack(pady=5)
        carrera_var = tb.StringVar(value=estudiante.carrera)
        combo_carrera = tb.Combobox(win, textvariable=carrera_var, values=self.carreras, state="readonly")
        combo_carrera.pack()
        tb.Label(win, text="Notas (separadas por '|'):").pack(pady=5)
        entry_notas = tb.Entry(win)
        entry_notas.insert(0, " | ".join(f"{n:05.2f}" for n in estudiante.notas))
        entry_notas.pack()

        def guardar():
            try:
                nombre = entry_nombre.get()
                edad = int(entry_edad.get())
                carrera = carrera_var.get()
                notas_strs = [n.strip() for n in entry_notas.get().split("|") if n.strip()]
                if len(notas_strs) != 3:
                    raise ValueError("Por favor, ingrese exactamente 3 notas, separadas por '|'. Ejemplo: 15|18|20")
                notas = []
                for n in notas_strs:
                    try:
                        notas.append(float(n))
                    except ValueError:
                        raise ValueError("Por favor, ingrese solo valores numéricos para las notas, separados por '|'. Ejemplo: 15|18|20")
                estudiante.nombre = nombre
                estudiante.edad = edad
                estudiante.carrera = carrera
                estudiante.notas = notas
                self._actualizar_becas()
                messagebox.showinfo("Éxito", f"Estudiante {nombre} editado.", parent=win)
                win.destroy()
                self.mostrar_estudiantes()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        tb.Button(win, text="Guardar Cambios", bootstyle=SUCCESS, command=guardar).pack(pady=15)

    def eliminar_estudiante(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Eliminar", "Seleccione un estudiante para eliminar.", parent=self)
            return
        idx = self.tree.index(selected[0])
        estudiante = self.estudiantes[idx]
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar a {estudiante.nombre}?", parent=self)
        if confirm:
            del self.estudiantes[idx]
            self._actualizar_becas()
            self.mostrar_estudiantes()
            messagebox.showinfo("Eliminado", f"Estudiante {estudiante.nombre} eliminado.", parent=self)

    def aplicar_filtros(self):
        lista = self.estudiantes
        # Filtrar por carrera
        carrera = self.filtro_carrera.get()
        if carrera != "Todas":
            lista = [e for e in lista if e.carrera == carrera]
        # Filtrar por estado
        estado = self.filtro_estado.get()
        if estado == "Aprobado":
            lista = [e for e in lista if e.es_aprobado()]
        elif estado == "Desaprobado":
            lista = [e for e in lista if not e.es_aprobado()]
        # Filtrar por beca
        beca = self.filtro_beca.get()
        if beca == "Con beca":
            lista = [e for e in lista if e.tiene_beca]
        elif beca == "Sin beca":
            lista = [e for e in lista if not e.tiene_beca]
        self._actualizar_tabla(lista)

    def limpiar_filtros(self):
        self.filtro_carrera.set("Todas")
        self.filtro_estado.set("Todos")
        self.filtro_beca.set("Todos")
        self.mostrar_estudiantes()

    def ordenar_por_columna(self, columna):
        col_idx = list(self.tree["columns"]).index(columna)
        lista = self.tree.get_children()
        datos = [self.tree.item(i)["values"] for i in lista]
        if self.orden_columna == columna:
            self.orden_ascendente = not self.orden_ascendente
        else:
            self.orden_ascendente = True
        self.orden_columna = columna
        def parse_value(val):
            try:
                return float(val)
            except:
                return str(val)
        datos.sort(key=lambda x: parse_value(x[col_idx]), reverse=not self.orden_ascendente)
        for i, item in enumerate(lista):
            self.tree.item(item, values=datos[i])

if __name__ == "__main__":
    app = SistemaAcademicoApp()
    app.mainloop() 