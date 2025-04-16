import json
import matplotlib.pyplot as plt

def cargar_datos(path):# Carga de datos JSON

    with open(path, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def mostrar_estudiantes(data):# Mostrar información básica de estudiantes

    print("\nEstudiantes registrados:")

    for estudiante in data['estudiantes']:
        print(f"- {estudiante['nombre']} ({estudiante['id']})")

def mostrar_curso(data):# Mostrar información básica de cursos

    curso = data['curso']

    print(f"\nCurso: {curso['nombre']} ({curso['codigo']})")
    print("Temas:")

    for tema in curso['temas']:
        print(f"  {tema['id']} - {tema['nombre']}")

def guardar_datos(path, data):#Actualizar datos json

    with open(path, 'w', encoding='utf-8') as archivo:
        json.dump(data, archivo, indent=2, ensure_ascii=False)

def agregar_estudiante(data):#generar un nuevo estudiante

    nuevo = {
        "id": input("ID del estudiante: "),
        "nombre": input("Nombre: "),
        "codigo_curso": data['curso']['codigo'],
    }

    print("Ingrese las notas por subtema para cada evaluación:")

    evaluaciones = crear_estructura_evaluaciones(data)
    nuevo["evaluaciones"] = evaluaciones
    nuevo["nota_final"] = calcular_nota_final(data, evaluaciones)
    data['estudiantes'].append(nuevo)

    print("Estudiante agregado exitosamente.")

def eliminar_estudiante(data): #eliminar algun estudiante.

    id_est = input("ID del estudiante a eliminar: ")
    data['estudiantes'] = [e for e in data['estudiantes'] if e['id'] != id_est]

    print("Estudiante eliminado si existía.")

def crear_estructura_evaluaciones(data):

    evaluaciones = {}
    for eval_def in data['evaluaciones']:
        subtemas_dict = {}
        for sub in eval_def['subtemas']:
            try:
                nota = float(input(f"  Nota para subtema {sub}: "))
            except ValueError:
                nota = 0.0
            subtemas_dict[sub] = nota
        promedio = sum(subtemas_dict.values()) / len(subtemas_dict) if subtemas_dict else 0.0
        evaluaciones[eval_def['id']] = {
            "nota": round(promedio, 1),
            "subtemas": subtemas_dict
        }
    return evaluaciones

def calcular_nota_final(data, evaluaciones):

    total = 0.0
    for eval_def in data['evaluaciones']:
        eid = eval_def['id']
        peso = eval_def['peso']
        nota = evaluaciones[eid]['nota'] if eid in evaluaciones else 0.0
        total += peso * nota
    return round(total, 1)



# Gráfico de evalución por estudiante
def grafico_estudiante(data):
    
    id_est = input("ID del estudiante para graficar: ")
    estudiante = next((e for e in data['estudiantes'] if e['id'] == id_est), None)
    if not estudiante:
        print("Estudiante no encontrado.")
        return

    x = []
    y = []
    for eval_id, info in estudiante['evaluaciones'].items():
        x.append(eval_id)
        y.append(info['nota'])

    plt.plot(x, y, marker='o')
    plt.title(f"Notas de {estudiante['nombre']}")
    plt.xlabel("Evaluaciones")
    plt.ylabel("Nota")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.show()

#Menu
def menu():
    path = 'curso_estudiantes.json'
    data = cargar_datos(path)

    while True:
        print("\n--- MENÚ ---")
        print("1. Mostrar estudiantes")
        print("2. Mostrar información del curso")
        print("3. Agregar estudiante")
        print("4. Eliminar estudiante")
        print("5. Guardar datos")
        print("6. Gráfico de estudiante")
        print("7. Salir")

        op = input("Seleccione una opción: ")
        if op == '1':
            mostrar_estudiantes(data)
        elif op == '2':
            mostrar_curso(data)
        elif op == '3':
            agregar_estudiante(data)
        elif op == '4':
            eliminar_estudiante(data)
        elif op == '5':
            guardar_datos(path, data)
        elif op == '6':
            grafico_estudiante(data)
        elif op == '7':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


menu()
