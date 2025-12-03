import pygame
from Constantes import *  
from Funciones import *   

pygame.init()

boton_volver = crear_boton_volver("VOLVER", "Texturas\Boton_Respuesta.jpg", 1, 1)

pantalla_ajustes = pygame.transform.scale(pygame.image.load("Texturas/Fondo_Pantallas.png"),PANTALLA)


def mostrar_ajustes(pantalla, eventos, datos_juego):
    ventana = "ajustes" 
    pantalla.blit(pantalla_ajustes, (0,0))

    administrar_barra(datos_juego, pantalla)

    dibujar_botones([boton_volver], pantalla, "superficie", "rectangulo", 0)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                return "menu"

    pygame.display.flip()
    return ventana

