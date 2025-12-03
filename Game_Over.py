import pygame
import os
from Constantes import *
from Funciones import *
from Manejo_Archivos_Funciones import*

# ranking_file = "ranking.json"

pygame.init()

pantalla_game_over = pygame.transform.scale(pygame.image.load("Texturas/Fondo_game_over.png"),PANTALLA)

boton_continuar = crear_boton_continuar("CONTINUAR", 300, 380, 200, 60,(80,255,80),(160,160,160),FUENTE_ARIAL_30,320,390,activo=False, )

def mostrar_game_over(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict) -> str:
    datos_juego["bandera_texto"] = not datos_juego["bandera_texto"]
    
    ventana = "game_over"
    cuadro_nombre = crear_elemento_juego("Texturas/Figura_blanca.jpg", 300, 50, 250, 320)
    cuadro_game_over = crear_elemento_juego("Texturas/Boton_inicio.jpg", 600, 350, 100, 150)    

    pantalla.blit(pantalla_game_over,(0,0))
    pantalla.blit(cuadro_game_over["superficie"], cuadro_game_over["rectangulo"])

    for evento in cola_eventos:
        manejar_texto_nombre(evento, datos_juego)

    mostrar_texto(pantalla, f"GAME OVER", (290, 200), FUENTE_ARIAL_40, COLOR_NEGRO)
    mostrar_texto(pantalla, f"PUNTUACIÓN FINAL: {datos_juego.get('puntuacion')}", (220, 260), FUENTE_ARIAL_40, COLOR_NEGRO)

    nombre = datos_juego.get("nombre", "")
    if len(nombre) > 0:
        texto = f"{nombre}|" if datos_juego["bandera_texto"] else nombre
        mostrar_texto(cuadro_nombre["superficie"], texto, (10,10), FUENTE_ARIAL_30, COLOR_NEGRO)
    else:
        mostrar_texto(cuadro_nombre["superficie"], "Ingrese su nombre", (10,10), FUENTE_ARIAL_25, "#2E2D2D")

    pantalla.blit(cuadro_nombre["superficie"], cuadro_nombre["rectangulo"])

    if nombre_es_valido(nombre):
        boton_continuar["activo"] = True
    else:
        boton_continuar["activo"] = False

    dibujar_boton_continuar(pantalla, boton_continuar)

    if boton_clickeado_continuar(cola_eventos, boton_continuar) and boton_continuar["activo"]:
        # guardar_puntaje_json(ranking_file, nombre, datos_juego["puntuacion"])
        ventana = "menu"

    return ventana

