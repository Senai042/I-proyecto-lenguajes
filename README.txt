
Sistema de Análisis de Rendimiento Académico

Este proyecto analiza el rendimiento de estudiantes en un curso a través de procesamiento en OCaml y visualización en Python.
Realizado y desarrollado por los estudiantes:

-Isaí José Navarro Serrano
-Marco Antonio Quirós Cabezas


==============================

Tecnologías Utilizadas
- OCaml + Dune (procesamiento funcional)
- Python 3 + Matplotlib + Tkinter (visualización gráfica)
- Yojson (manejo de archivos JSON en OCaml)

==============================

Estructura del Proyecto

proyecto/
├── ocaml/
│   ├── curso_estudiantes.json
│   ├── calculos.ml
│   ├── dune-project
│   ├── dune
├── main.py
├── resultados.json (se genera automáticamente)
├── README.md

==============================

Instalación 

En Ubuntu / WSL2:

# Instalación OCaml y Dune
sudo apt update
sudo apt install ocaml opam dune m4
opam init
opam install dune yojson

# Instalación Python y Matplotlib
sudo apt install python3 python3-pip
pip install matplotlib

==============================

Se puede ejecutar desde la raíz del proyecto:

python3 main.py

Este comando compilará OCaml, procesará los datos y lanzará la interfaz gráfica.
