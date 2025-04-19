import subprocess
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# ========================
# Ejecutar OCaml y cargar JSON
# ========================
def generar_resultados():
    try:
        # Ajusta esta ruta según tu sistema y estructura
        ruta_ocaml = "_build/default/calculos.exe"
        if not os.path.exists(ruta_ocaml):
            raise FileNotFoundError(f"No se encontró el ejecutable OCaml en {ruta_ocaml}")
        subprocess.run([ruta_ocaml], check=True)
        print("✅ OCaml ejecutado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar OCaml: {e}")
        exit(1)

def cargar_datos(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", f"No se encontró el archivo {path}")
        exit(1)
    with open(path, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# ========================
# Funciones de visualización
# ========================
def mostrar_grafico_estudiante(estudiante, tipo, tema_id=None):
    plt.clf()
    if tipo == 'general':
        x = list(estudiante['notas_evaluaciones'].keys())
        y = [nota for nota in estudiante['notas_evaluaciones'].values()]
        plt.plot(x, y, marker='o')
        plt.title(f"Evolución general de {estudiante['nombre']}")
    elif tipo == 'parciales':
        parciales = {eid: nota for eid, nota in estudiante['notas_evaluaciones'].items() if eid.startswith('P')}
        plt.bar(parciales.keys(), parciales.values())
        plt.title(f"Parciales - {estudiante['nombre']}")
    elif tipo == 'otros':
        otros = {eid: nota for eid, nota in estudiante['notas_evaluaciones'].items() if not eid.startswith('P')}
        plt.bar(otros.keys(), otros.values())
        plt.title(f"Evaluaciones no parciales - {estudiante['nombre']}")
    elif tipo == 'tema' and tema_id:
        tema_notas = {
            sid: nota for sid, nota in estudiante['porcentaje_conocimiento'].items()
            if sid.startswith(tema_id + ".")
        }
        if not tema_notas:
            messagebox.showwarning("Tema vacío", f"No hay subtemas registrados para el tema {tema_id}")
            return
        plt.bar(tema_notas.keys(), tema_notas.values())
        plt.title(f"Rendimiento en tema {tema_id} - {estudiante['nombre']}")
    plt.xlabel("Evaluaciones/Subtemas")
    plt.ylabel("Nota")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def mostrar_grafico_general(data, tipo):
    if tipo == 'notas':
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

        stats = data['estadisticas']
        resumen = (
            f"Promedio: {round(stats['nota_promedio'], 1)}\n"
            f"Moda: {stats['nota_moda']}\n"
            f"Máximo: {stats['nota_max']}\n"
            f"Mínimo: {stats['nota_min']}"
        )
        messagebox.showinfo("Estadísticas", resumen)

    elif tipo == 'subtemas':
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

# ========================
# Interfaz principal con Tkinter
# ========================
def lanzar_interfaz():
    generar_resultados()
    data = cargar_datos("../resultados.json")
    estudiantes = data['resultados']

    root = tk.Tk()
    root.title("Análisis de Rendimiento Académico")
    root.geometry("600x400")

    modo = tk.StringVar(value='estudiante')

    def mostrar_panel_estudiante():
        for widget in frame.winfo_children(): widget.destroy()

        tk.Label(frame, text="Estudiante:").pack()
        estudiantes_ids = [e['id'] for e in estudiantes]
        selected_id = tk.StringVar()
        estudiante_dropdown = ttk.Combobox(frame, textvariable=selected_id, values=estudiantes_ids)
        estudiante_dropdown.pack()

        tk.Label(frame, text="Tipo de gráfica:").pack()
        opciones = ["general", "parciales", "otros"] + [f"tema:{i}" for i in ["2", "3", "4", "5", "6", "7"]]
        selected_option = tk.StringVar()
        grafica_dropdown = ttk.Combobox(frame, textvariable=selected_option, values=opciones)
        grafica_dropdown.pack()

        def graficar_est():
            est_id = selected_id.get()
            opt = selected_option.get()
            estudiante = next((e for e in estudiantes if e['id'] == est_id), None)
            if not estudiante:
                messagebox.showerror("Error", "Estudiante no encontrado")
                return
            if opt.startswith('tema:'):
                mostrar_grafico_estudiante(estudiante, 'tema', tema_id=opt.split(':')[1])
            else:
                mostrar_grafico_estudiante(estudiante, opt)

        tk.Button(frame, text="Graficar Estudiante", command=graficar_est).pack(pady=10)

    def mostrar_panel_curso():
        for widget in frame.winfo_children(): widget.destroy()

        tk.Label(frame, text="Tipo de gráfica general:").pack()
        opciones = ["notas", "subtemas"]
        selected_option = tk.StringVar()
        grafica_dropdown = ttk.Combobox(frame, textvariable=selected_option, values=opciones)
        grafica_dropdown.pack()

        def graficar():
            opt = selected_option.get()
            mostrar_grafico_general(data, opt)

        tk.Button(frame, text="Graficar Curso", command=graficar).pack(pady=10)

    def actualizar_panel():
        if modo.get() == 'estudiante':
            mostrar_panel_estudiante()
        else:
            mostrar_panel_curso()

    selector_frame = tk.Frame(root)
    selector_frame.pack(pady=10)
    tk.Label(selector_frame, text="Seleccione el tipo de análisis:").pack()
    ttk.Radiobutton(selector_frame, text="Estudiante", variable=modo, value='estudiante', command=actualizar_panel).pack(side='left')
    ttk.Radiobutton(selector_frame, text="Curso", variable=modo, value='curso', command=actualizar_panel).pack(side='left')

    frame = tk.Frame(root)
    frame.pack(pady=20)

    actualizar_panel()
    root.mainloop()

# ========================
# Punto de entrada principal
# ========================
if __name__ == "__main__":
    lanzar_interfaz()
