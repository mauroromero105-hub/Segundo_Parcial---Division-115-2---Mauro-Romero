import pygame
import os
from Constantes import *
from Funciones import *
from Manejo_Archivos_Funciones import*

pygame.init()

# lista_ranking = leer_json("ranking.json") 

pantalla_rankings = pygame.transform.scale(pygame.image.load("Texturas/Fondo_Pantallas.png"),PANTALLA)
boton_volver = crear_boton_volver("VOLVER", "Texturas\Boton_Respuesta.jpg", 1, 1)
cuadro_top = crear_elemento_juego("Texturas\Pared_Blanca.png", 400,600,195, 1)

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:

    ventana = "rankings"
    pantalla.blit(pantalla_rankings,(0,0))
    pantalla.blit(cuadro_top["superficie"], cuadro_top["rectangulo"])
    dibujar_botones([boton_volver], pantalla_rankings, "superficie", "rectangulo", 0)
    mostrar_texto(pantalla, "TOP 10", (310, 0), FUENTE_ARIAL_55, COLOR_NEGRO)

    # y_inicial = 160
    # espacio_jugadores = 40

    # for i in range(len(lista_ranking)):
    #     jugador = lista_ranking[i]
    #     texto = f"{i+1}. {jugador['nombre']}  -  {jugador['puntuacion']} pts"
    #     mostrar_texto(pantalla,texto,(180, y_inicial + i * espacio_jugadores),FUENTE_ARIAL_40,COLOR_NEGRO)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                ventana = "menu"
    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    return ventana

