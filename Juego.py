import pygame
from Constantes import *
from Funciones import *
from os import*
from Manejo_Archivos_Funciones import*

pygame.init()

csv_preguntas = cargar_preguntas("Preguntas.csv")    

pantalla_juego = pygame.transform.scale(pygame.image.load("Texturas/Fondo_Pantallas.png"),PANTALLA)

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    ventana = "jugar"

    if actualizar_tiempo_pregunta(datos_juego):
        pasar_pregunta(datos_juego, csv_preguntas)

    cuadro_pregunta = crear_elemento_juego("Texturas/Cuadro_madera.jpg",ANCHO_PREGUNTA, ALTO_PREGUNTA, 125, 110)
    cuadro_respuestas = crear_lista_respuestas("Texturas/Boton_Respuesta.jpg",270, 300, 4)
    cuadro_puntuacion = crear_elemento_juego("Texturas/Boton_Respuesta.jpg",180, 100, 620, 1)

    pregunta_actual = obtener_pregunta_actual(datos_juego, csv_preguntas)
    
    boton_volver = crear_boton_volver("VOLVER", "Texturas/Boton_Respuesta.jpg", 1, 1)
    boton_bomba = crear_elemento_juego("Texturas/Bomba.png", 40, 40, 20, 260)
    boton_x2 = crear_elemento_juego("Texturas/icono_x2.png", 40, 40, 20, 300)
    boton_doble = crear_elemento_juego("Texturas/logo_dos_intentos.png", 40, 40, 20, 340)
    boton_pasar = crear_elemento_juego("Texturas/Cambio_Pregunta.png", 40, 40, 20, 380)


    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                return "menu"

            if boton_bomba["rectangulo"].collidepoint(evento.pos):
                activar_bomba(datos_juego, pregunta_actual)

            if boton_doble["rectangulo"].collidepoint(evento.pos):
                activar_doble_chance(datos_juego)

            if boton_x2["rectangulo"].collidepoint(evento.pos):
                activar_x2(datos_juego)

            if boton_pasar["rectangulo"].collidepoint(evento.pos):
                activar_pasar(datos_juego, csv_preguntas)
                pregunta_actual = obtener_pregunta_actual(datos_juego, csv_preguntas)

            responder_pregunta_pygame(cuadro_respuestas,evento.pos,SONIDO_CLICK,datos_juego,csv_preguntas,pregunta_actual)

            pregunta_actual = obtener_pregunta_actual(datos_juego, csv_preguntas)

    if datos_juego["cantidad_vidas"] <= 0:
        return "game_over"

    pantalla.blit(pantalla_juego, (0, 0))

    mostrar_datos_juego_pygame(pantalla, datos_juego, cuadro_puntuacion)

    mostrar_pregunta_pygame(pregunta_actual,pantalla,cuadro_pregunta,cuadro_respuestas,datos_juego)

    pantalla.blit(boton_bomba["superficie"], boton_bomba["rectangulo"])
    pantalla.blit(boton_x2["superficie"], boton_x2["rectangulo"])
    pantalla.blit(boton_doble["superficie"], boton_doble["rectangulo"])
    pantalla.blit(boton_pasar["superficie"], boton_pasar["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    return ventana
