import json
import os

def cargar_preguntas(nombre_archivo: str):
    preguntas = []

    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            if lineas:
                lineas = lineas[1:]

            for linea in lineas:
                fila = linea.strip().split(',')
                if len(fila) < 6:
                    print("Fila inválida (ignorada):", fila)
                    continue

                preguntas.append({
                    "pregunta": fila[0],
                    "opcion_A": fila[1],
                    "opcion_B": fila[2],
                    "opcion_C": fila[3],
                    "opcion_D": fila[4],
                    "opcion_correcta": fila[5]
                })

    return preguntas

# def guardar_puntaje_json(nombre_archivo: str, nombre_jugador: str, puntuacion: int):

#     if os.path.exists(nombre_archivo):
#         with open(nombre_archivo, "r", encoding="utf-8") as archivo:
#             jugadores = json.load(archivo)
#     else:
#         jugadores = []

#     if len(jugadores) >= 10 and puntuacion <= min(jugador['puntuacion'] for jugador in jugadores):
#         return

#     jugadores.append({"nombre": nombre_jugador, "puntuacion": puntuacion})

#     jugadores.sort(key=lambda x: x['puntuacion'], reverse=True)

#     jugadores = jugadores[:10]

#     with open(nombre_archivo, "w", encoding="utf-8") as archivo:
#         json.dump(jugadores, archivo, indent=4)

# def leer_json(nombre_archivo:str):
#     if not os.path.exists(nombre_archivo):
#         return False

#     try:
#         with open(nombre_archivo,"r",encoding="utf-8") as archivo:
#             return json.load(archivo)
#     except (json.JSONDecodeError, ValueError):
#         return False


# def crear_archivo_json(nombre_archivo: str):
#     directorio = os.path.dirname(nombre_archivo)
    
#     if not os.path.exists(directorio):
#         os.makedirs(directorio)

#     with open(nombre_archivo, "w", encoding="utf-8") as archivo:
#         json.dump([], archivo) 

# nombre_archivo = "C:/Users/mauro/OneDrive/Documentos/Visual Studios Code/Python UTN/Programación 1/Segundo Parcial/Datos.json"
# crear_archivo_json(nombre_archivo)

# def guardar_datos_json(nombre_archivo: str, datos: dict):
#     """Guarda datos en un archivo JSON."""
#     if os.path.exists(nombre_archivo):
#         with open(nombre_archivo, "r", encoding="utf-8") as archivo:
#             try:
#                 contenido = json.load(archivo)
#             except json.JSONDecodeError:
#                 contenido = [] 
#     else:
#         contenido = []

#     contenido.append(datos)

#     with open(nombre_archivo, "w", encoding="utf-8") as archivo:
#         json.dump(contenido, archivo, indent=4)

# def leer_datos_json(nombre_archivo: str):
#     """Lee datos desde un archivo JSON y los devuelve como una lista."""
#     if os.path.exists(nombre_archivo):
#         with open(nombre_archivo, "r", encoding="utf-8") as archivo:
#             try:
#                 return json.load(archivo)
#             except json.JSONDecodeError:
#                 return [] 
#     return [] 

# nombre_archivo = "C:/Users/mauro/OneDrive/Documentos/Visual Studios Code/Python UTN/Programación 1/Segundo Parcial/Datos.json"

# crear_archivo_json(nombre_archivo)

# guardar_datos_json(nombre_archivo, {"nombre": "Juan", "puntaje": 150})
# guardar_datos_json(nombre_archivo, {"nombre": "María", "puntaje": 200})

# datos_cargados = leer_datos_json(nombre_archivo)
# print(datos_cargados)
# import os
# print(os.getcwd())
