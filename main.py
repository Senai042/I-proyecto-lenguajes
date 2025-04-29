"""Sistema de Análisis de Rendimiento Académico

Este proyecto analiza el rendimiento de estudiantes en un curso a través de procesamiento 
en OCaml y visualización en Python. Realizado y desarrollado por los estudiantes:

-Isaí José Navarro Serrano
-Marco Antonio Quirós Cabezas"""

# Librerías empleadas.
import subprocess
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Función para lectura y creación de los archivos JSON
def generar_resultados():
    # Ejecuta y automatiza los pasos necesarios para compilar y ejecutar el programa OCaml,
    # haciendo innecesario un build y run manual.
    try:
        # Compila el proyecto OCaml utilizando dune mediante la biblioteca subprocess.
        print("Compilando OCaml 🔨 🔨 🔨 ")
        subprocess.run(["dune", "build"], cwd="ocaml", check=True)
        print("Completado")

        # Ejecuta el ejecutable generado de OCaml (calculos.exe) para crear un archivo JSON con los resultados.
        ruta_ocaml = os.path.join("ocaml", "_build", "default", "calculos.exe")
        if not os.path.exists(ruta_ocaml):
            raise FileNotFoundError(f"No se encontró el ejecutable OCaml en {ruta_ocaml}")
        subprocess.run([ruta_ocaml], check=True)
        print("OCaml ejecutado correctamente.")
    except Exception as e:
        # Maneja cualquier error que ocurra durante la compilación o ejecución de OCaml.
        print(f"Error al ejecutar OCaml: {e}")

# Función para cargar los datos de un archivo JSON
def cargar_datos(path):
    # Verifica si el archivo existe
    if not os.path.exists(path):
        messagebox.showerror("Error", f"No se encontró el archivo {path}")
        exit(1)
    # Abre y carga el contenido JSON
    with open(path, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# Función para  gráficos individuales de un estudiante
def mostrar_grafico_estudiante(estudiante, tipo, tema_id=None):
    plt.clf()  # Limpia la figura actual
    
    if tipo == 'general':
        # Grafica la evolución de las notas del estudiante en general
        x = list(estudiante['notas_evaluaciones'].keys())
        y = [nota for nota in estudiante['notas_evaluaciones'].values()]
        plt.plot(x, y, marker='o')
        plt.title(f"Evolución general de {estudiante['nombre']}")
    
    elif tipo == 'parciales':
        # Grafica solamente las evaluaciones que son parciales
        parciales = {eid: nota for eid, nota in estudiante['notas_evaluaciones'].items() if eid.startswith('P')}
        plt.bar(parciales.keys(), parciales.values())
        plt.title(f"Parciales - {estudiante['nombre']}")
    
    elif tipo == 'otros':
        # Grafica evaluaciones que no son parciales
        otros = {eid: nota for eid, nota in estudiante['notas_evaluaciones'].items() if not eid.startswith('P')}
        plt.bar(otros.keys(), otros.values())
        plt.title(f"Evaluaciones no parciales - {estudiante['nombre']}")
    
    elif tipo == 'tema' and tema_id:
        # Grafica el rendimiento del estudiante en un tema específico
        tema_notas = {
            sid: nota for sid, nota in estudiante['porcentaje_conocimiento'].items()
            if sid.startswith(tema_id + ".")
        }
        if not tema_notas:
            messagebox.showwarning("Tema vacío", f"No hay subtemas registrados para el tema {tema_id}")
            return
        plt.bar(tema_notas.keys(), tema_notas.values())
        plt.title(f"Rendimiento en tema {tema_id} - {estudiante['nombre']}")

    # Configuraciones generales del gráfico
    plt.xlabel("Evaluaciones/Subtemas")
    plt.ylabel("Nota")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Función para gráficos generales del curso
def mostrar_grafico_general(data, tipo):
    if tipo == 'notas':
        # Grafica la nota final de todos los estudiantes
        nombres = [e['nombre'] for e in data['resultados']]
        notas = [e['nota_final'] for e in data['resultados']]
        plt.bar(nombres, notas)
        plt.title("Rendimiento general del curso")
        plt.xlabel("Estudiantes")
        plt.ylabel("Nota Final")
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

        # Muestra estadísticas básicas del curso en ventanas emergentes
        stats = data['estadisticas']
        resumen = (
            f"Promedio: {round(stats['nota_promedio'], 1)}\n"
            f"Moda: {stats['nota_moda']}\n"
            f"Máximo: {stats['nota_max']}\n"
            f"Mínimo: {stats['nota_min']}"
        )
        messagebox.showinfo("Estadísticas", resumen)

        # Muestra subtemas críticos
        criticos = data['estadisticas'].get('subtemas_criticos', {})
        detalle = "\n".join([f"{k}: {v}" for k, v in criticos.items()])
        messagebox.showinfo("Subtemas Críticos", f"Subtemas con menor promedio:\n{detalle}")

    elif tipo == 'subtemas':
        # Grafica el promedio de cada subtema
        subtemas = data['estadisticas']['promedio_por_subtema']
        sorted_items = sorted(subtemas.items(), key=lambda x: x[1], reverse=True)
        x, y = zip(*sorted_items)
        plt.figure(figsize=(10, 5))
        plt.bar(x, y)
        plt.title("Promedio por subtema")
        plt.xlabel("Subtemas")
        plt.ylabel("Nota Promedio")
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

#Interfaz con Tkinder
def lanzar_interfaz():
    # Inicializa los datos necesarios ejecutando OCaml y cargando el JSON
    generar_resultados()
    data = cargar_datos("./resultados.json")
    estudiantes = data['resultados']

    # Crea la ventana principal
    root = tk.Tk()
    root.title("Análisis de Rendimiento Académico")
    root.geometry("600x400")

    # Variable para definir el modo de análisis (por estudiante o curso)
    modo = tk.StringVar(value='estudiante')

    # Mostrar el panel de selección de estudiante
    def mostrar_panel_estudiante():
        # Limpia el frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Selector de estudiante
        tk.Label(frame, text="Estudiante:").pack()
        estudiantes_ids = [e['id'] for e in estudiantes]
        selected_id = tk.StringVar()
        estudiante_dropdown = ttk.Combobox(frame, textvariable=selected_id, values=estudiantes_ids)
        estudiante_dropdown.pack()

        # Selector de tipo de gráfico
        tk.Label(frame, text="Tipo de gráfica:").pack()
        opciones = ["general", "parciales", "otros"] + [f"tema:{i}" for i in ["2", "3", "4", "5", "6", "7"]]
        selected_option = tk.StringVar()
        grafica_dropdown = ttk.Combobox(frame, textvariable=selected_option, values=opciones)
        grafica_dropdown.pack()

        # información del estudiante seleccionado
        def graficar_est():
            # Obtiene el ID del estudiante seleccionado en el menú desplegable
            est_id = selected_id.get()
            # Obtiene la opción de gráfico seleccionada (general, parciales, otros o tema específico)
            opt = selected_option.get()
            # Busca el estudiante correspondiente en la lista de estudiantes
            estudiante = next((e for e in estudiantes if e['id'] == est_id), None)

            # Si no se encuentra el estudiante, muestra un mensaje de error y termina
            if not estudiante:
                messagebox.showerror("Error", "Estudiante no encontrado")
                return
            # Dependiendo de la opción seleccionada, muestra el gráfico correspondiente
            if opt.startswith('tema:'):
                # Si la opción es un tema específico, extrae el ID del tema y muestra el gráfico de subtemas
                mostrar_grafico_estudiante(estudiante, 'tema', tema_id=opt.split(':')[1])
            else:
                # Si la opción es general, parciales u otros, muestra el gráfico correspondiente
                mostrar_grafico_estudiante(estudiante, opt)
            # Solo si el tipo de gráfico seleccionado fue 'general', muestra la tendencia del estudiante
            if opt == 'general':
                tendencia = estudiante.get('tendencia', 'desconocida')
                messagebox.showinfo("Tendencia", f"Tendencia de {estudiante['nombre']}: {tendencia}")
        tk.Button(frame, text="Graficar Estudiante", command=graficar_est).pack(pady=10)

    # Función para mostrar el panel de análisis general del curso
    def mostrar_panel_curso():
        # Limpia el frame antes de actualizar
        for widget in frame.winfo_children():
            widget.destroy()

        # Selector de tipo de gráfico general
        tk.Label(frame, text="Tipo de gráfica general:").pack()
        opciones = ["notas", "subtemas"]
        selected_option = tk.StringVar()
        grafica_dropdown = ttk.Combobox(frame, textvariable=selected_option, values=opciones)
        grafica_dropdown.pack()

        # Función para graficar los datos generales del curso
        def graficar():
            opt = selected_option.get()
            mostrar_grafico_general(data, opt)

        tk.Button(frame, text="Graficar Curso", command=graficar).pack(pady=10)

    # Función para actualizar el panel según el modo seleccionado
    def actualizar_panel():
        if modo.get() == 'estudiante':
            mostrar_panel_estudiante()
        else:
            mostrar_panel_curso()

    # Creación de selector para el tipo de análisis
    selector_frame = tk.Frame(root)
    selector_frame.pack(pady=10)
    tk.Label(selector_frame, text="Seleccione el tipo de análisis:").pack()
    ttk.Radiobutton(selector_frame, text="Estudiante", variable=modo, value='estudiante', command=actualizar_panel).pack(side='left')
    ttk.Radiobutton(selector_frame, text="Curso", variable=modo, value='curso', command=actualizar_panel).pack(side='left')

    # Frame principal donde se carga dinámicamente el contenido
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Inicializa el primer panel
    actualizar_panel()

    # Inicia el loop de eventos de Tkinter
    root.mainloop()

# Ejecuta la interfaz al correr el script
lanzar_interfaz()
