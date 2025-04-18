# Base para programa en Python con interfaz Tkinter

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import statistics
from collections import defaultdict

# ========================
# Carga de datos JSON
# ========================
def cargar_datos(path):
    with open(path, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# ========================
# Funciones de visualización
# ========================
def mostrar_grafico_estudiante(data, estudiante, tipo, tema_id=None):
    plt.clf()
    if tipo == 'general':
        x = list(estudiante['evaluaciones'].keys())
        y = [info['nota'] for info in estudiante['evaluaciones'].values()]
        plt.plot(x, y, marker='o')
        plt.title(f"Evolución general de {estudiante['nombre']}")
    elif tipo == 'parciales':
        parciales = {eid: info['nota'] for eid, info in estudiante['evaluaciones'].items() if eid.startswith('P')}
        plt.bar(parciales.keys(), parciales.values())
        plt.title(f"Parciales - {estudiante['nombre']}")
    elif tipo == 'otros':
        otros = {eid: info['nota'] for eid, info in estudiante['evaluaciones'].items() if not eid.startswith('P')}
        plt.bar(otros.keys(), otros.values())
        plt.title(f"Evaluaciones no parciales - {estudiante['nombre']}")
    elif tipo == 'tema' and tema_id:
        subtemas = [s['id'] for t in data['curso']['temas'] if t['id'] == tema_id for s in t['subtemas']]
        tema_notas = {}
        for eval_info in estudiante['evaluaciones'].values():
            for sid, nota in eval_info['subtemas'].items():
                if sid in subtemas:
                    tema_notas[sid] = nota
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
        notas_finales = [e['nota_final'] for e in data['estudiantes']]
        nombres = [e['nombre'] for e in data['estudiantes']]
        plt.bar(nombres, notas_finales)
        plt.title("Rendimiento general del curso")
        plt.xlabel("Estudiantes")
        plt.ylabel("Nota Final")
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
        stats = f"Promedio: {round(statistics.mean(notas_finales),1)}\n"
        stats += f"Moda: {statistics.mode(notas_finales)}\n"
        stats += f"Máximo: {max(notas_finales)}\n"
        stats += f"Mínimo: {min(notas_finales)}"
        messagebox.showinfo("Estadísticas", stats)

    elif tipo == 'subtemas':
        subtema_notas = defaultdict(list)
        for estudiante in data['estudiantes']:
            for eval_info in estudiante['evaluaciones'].values():
                for sid, nota in eval_info['subtemas'].items():
                    subtema_notas[sid].append(nota)
        subtema_promedios = {k: round(sum(v)/len(v),1) for k, v in subtema_notas.items() if v}
        sorted_items = sorted(subtema_promedios.items(), key=lambda x: x[1], reverse=True)
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
    data = cargar_datos('curso_estudiantes.json')

    root = tk.Tk()
    root.title("Análisis de Rendimiento Académico")
    root.geometry("600x400")

    modo = tk.StringVar(value='estudiante')

    def mostrar_panel_estudiante():
        for widget in frame.winfo_children(): widget.destroy()

        tk.Label(frame, text="Estudiante:").pack()
        estudiantes_ids = [e['id'] for e in data['estudiantes']]
        selected_id = tk.StringVar()
        estudiante_dropdown = ttk.Combobox(frame, textvariable=selected_id, values=estudiantes_ids)
        estudiante_dropdown.pack()

        tk.Label(frame, text="Tipo de gráfica:").pack()
        opciones = ["general", "parciales", "otros"] + [f"tema:{t['id']}" for t in data['curso']['temas']]
        selected_option = tk.StringVar()
        grafica_dropdown = ttk.Combobox(frame, textvariable=selected_option, values=opciones)
        grafica_dropdown.pack()

        def graficar_est():
            est_id = selected_id.get()
            opt = selected_option.get()
            estudiante = next((e for e in data['estudiantes'] if e['id'] == est_id), None)
            if not estudiante:
                messagebox.showerror("Error", "Estudiante no encontrado")
                return
            if opt.startswith('tema:'):
                mostrar_grafico_estudiante(data, estudiante, 'tema', tema_id=opt.split(':')[1])
            else:
                mostrar_grafico_estudiante(data, estudiante, opt)

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

if __name__ == '__main__':
    lanzar_interfaz()
