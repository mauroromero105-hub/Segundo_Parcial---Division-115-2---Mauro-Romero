import random
import os
from Constantes import *
import pygame

#GENERAL
def mostrar_texto(superficie, texto, posicion, fuente, color=pygame.Color('black')):
    lineas = [linea.split(' ') for linea in texto.splitlines()]

    ancho_espacio = fuente.size(' ')[0]

    ancho_maximo, alto_maximo = superficie.get_size()

    x_inicial, y = posicion
    x = x_inicial

    for linea in lineas:
        for palabra in linea:
            superficie_palabra = fuente.render(palabra, True, color)
            ancho_palabra, alto_palabra = superficie_palabra.get_size()

            if x + ancho_palabra >= ancho_maximo:
                x = x_inicial
                y += alto_palabra

            superficie.blit(superficie_palabra, (x, y))

            x += ancho_palabra + ancho_espacio

        x = x_inicial
        y += alto_palabra

def crear_datos_juego() -> dict:
    datos_juego = {
        #estadistica
        "nombre": "",
        "indice": 0,
        "puntuacion": 0,
        "cantidad_vidas": CANTIDAD_VIDAS,

        #tiempo
        "tiempo_restante": TIEMPO_TOTAL,
        "tiempo_inicio_pregunta": pygame.time.get_ticks(),

        #acciones
        "correctas_seguidas": 0,
        "respuestas_ocultas": [],
        "doble_chance_en_uso": False,
        "doble_chance_fallo": False,
        "x2_activado": False,

        #comodines
        "bomba_disponible": True,
        "x2_disponible": True,
        "pasar_disponible": True,
        "doble_chance_disponible": True,

        #Volumen
        "volumen_musica": 0.5,
        "bandera_texto": True,
        "ultimo_borrado": 0
    }
    return datos_juego

def verificar_indice(datos_juego:dict,lista_preguntas:list) -> None:
    if datos_juego["indice"] == len(lista_preguntas):
        datos_juego["indice"] = 0
        mezclar_lista(lista_preguntas)

def mezclar_lista(lista_preguntas:dict) -> bool:
    if type(lista_preguntas) == list and len(lista_preguntas):
        retorno = True
        random.shuffle(lista_preguntas)
    else:
        retorno = False
    return retorno

def crear_elemento_juego(textura:str, ancho_elemento:int, alto_elemento:int, x:int, y:int) -> dict | None:
    if os.path.exists(textura):

        superficie = pygame.image.load(textura)
        superficie = pygame.transform.scale(superficie, (ancho_elemento, alto_elemento))

        rectangulo = superficie.get_rect(topleft=(x, y))

        return {
            "superficie": superficie,
            "rectangulo": rectangulo
        }
    else:
        return None

def dibujar_botones(lista_botones, pantalla, superficie, superficie_boton, indice):
    pantalla.blit(lista_botones[indice][superficie], lista_botones[indice][superficie_boton])

def dibujar_texto_en_cuadro(superficie, texto, rect, fuente, color=(0,0,0), margen=5):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba_linea = linea_actual + " " + palabra if linea_actual != "" else palabra
        ancho, alto = fuente.size(prueba_linea)
        if ancho + 2*margen > rect.width:
            lineas.append(linea_actual)
            linea_actual = palabra
        else:
            linea_actual = prueba_linea

    if linea_actual:
        lineas.append(linea_actual)

    # Dibuja las líneas centradas vertical y horizontalmente
    total_altura = len(lineas) * fuente.get_linesize()
    y_offset = rect.top + (rect.height - total_altura) // 2  # centra vertical

    for linea in lineas:
        ancho_linea, alto_linea = fuente.size(linea)
        x = rect.left + (rect.width - ancho_linea) // 2  # centra horizontal
        render = fuente.render(linea, True, color)
        superficie.blit(render, (x, y_offset))
        y_offset += fuente.get_linesize()

def crear_boton_volver(texto, textura, x, y):
    boton = crear_elemento_juego(textura,100, 40, x, y)
    dibujar_texto_en_cuadro(boton["superficie"], texto, boton["rectangulo"], FUENTE_INICIO, color= 'white')
    return boton

def colocar_musica(musica:str,datos_juego:dict) -> bool:
    if os.path.exists(musica):
        retorno = True
        pygame.mixer.music.load("Sonidos\Musica del juego.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(datos_juego.get("volumen_musica"))
    else:
        retorno = False
        
    return retorno

#JUEGO

def crear_lista_respuestas(textura:str,x:int,y:int,cantidad_respuestas:int) -> list:
    lista_respuestas = []

    for i in range(cantidad_respuestas):
        cuadro_respuesta = crear_elemento_juego(textura,ANCHO_RESPUESTA,ALTO_RESPUESTA,x,y)
        lista_respuestas.append(cuadro_respuesta)
        y += 70
    
    return lista_respuestas

def crear_lista_botones(textura:str,x:int,y:int,cantidad_botones:int) -> list:
    lista_botones = []

    for i in range(cantidad_botones):
        boton = crear_elemento_juego(textura,ANCHO_BOTON,ALTO_BOTON,x,y)
        lista_botones.append(boton)
        y += 85
    
    return lista_botones

def obtener_pregunta_actual(datos_juego:dict,lista_preguntas:list) -> dict | None:
    if type(datos_juego) == dict and type(lista_preguntas) == list and len(lista_preguntas) > 0 and datos_juego.get("indice") != None:
        indice = datos_juego.get("indice")
        pregunta = lista_preguntas[indice]
    else:
        pregunta = None

    return pregunta    

def pasar_pregunta(datos_juego:dict,lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("indice") != None:
        retorno = True
        datos_juego["indice"] += 1
        verificar_indice(datos_juego,lista_preguntas)
    else:
        retorno = False 
        
    return retorno

def mostrar_datos_juego_pygame(pantalla:pygame.Surface,datos_juego:dict, cuadro_puntuacion):
    mostrar_texto(cuadro_puntuacion["superficie"],f"Tiempo restante: {datos_juego.get("tiempo_restante")} s",(10,10),FUENTE_INICIO, COLOR_BLANCO)
    mostrar_texto(cuadro_puntuacion["superficie"],f"Puntuación: {datos_juego.get("puntuacion")}",(10,35),FUENTE_INICIO, COLOR_BLANCO)
    mostrar_texto(cuadro_puntuacion["superficie"],f"Vidas: {datos_juego.get("cantidad_vidas")}",(10,60),FUENTE_INICIO, COLOR_BLANCO)
    pantalla.blit(cuadro_puntuacion["superficie"], cuadro_puntuacion["rectangulo"])

def verificar_respuesta(pregunta_actual:dict, datos_juego:dict, respuesta:int):

    if pregunta_actual is None:
        return False
    if respuesta < 1 or respuesta > 4:
        return False

    opciones = ["opcion_A", "opcion_B", "opcion_C", "opcion_D"]

    texto_elegido = pregunta_actual.get(opciones[respuesta - 1], "")
    texto_correcto = pregunta_actual.get("opcion_correcta", "")

    texto_elegido = str(texto_elegido).strip().casefold()
    texto_correcto = str(texto_correcto).strip().casefold()

    es_correcta = texto_elegido == texto_correcto and texto_correcto != ""

    if es_correcta:
        modificar_puntuacion(datos_juego, PUNTUACION_ACIERTO)

        if datos_juego["x2_activado"]:
            modificar_puntuacion(datos_juego, PUNTUACION_ACIERTO)
            datos_juego["x2_activado"] = False

        return True

    else:
        SONIDO_ERROR.play()
        modificar_puntuacion(datos_juego, PUNTUACION_ERROR)
        modificar_vida(datos_juego, VIDA_ERROR)
        return False

def responder_pregunta_pygame(lista_respuestas, pos_click, sonido,datos_juego, lista_preguntas, pregunta_actual):

    ocultas = datos_juego["respuestas_ocultas"]

    for i in range(len(lista_respuestas)):
        if i in ocultas:
            continue

        rect = lista_respuestas[i]["rectangulo"]

        if rect.collidepoint(pos_click):
            sonido.play()
            respuesta = i + 1

            es_correcta = verificar_respuesta(pregunta_actual,datos_juego,respuesta)

            if datos_juego["doble_chance_en_uso"] and not es_correcta:

                if not datos_juego["doble_chance_fallo"]:
                    datos_juego["doble_chance_fallo"] = True
                    datos_juego["respuestas_ocultas"].append(i)
                    return True

                else:
                    datos_juego["doble_chance_en_uso"] = False
                    datos_juego["doble_chance_fallo"] = False

            manejar_aciertos_consecutivos(datos_juego, es_correcta)

            datos_juego["respuestas_ocultas"] = []
            datos_juego["doble_chance_en_uso"] = False
            datos_juego["doble_chance_fallo"] = False

            pasar_pregunta(datos_juego, lista_preguntas)

            datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()

            return True

    return False

def mostrar_pregunta_pygame(pregunta_actual:dict, pantalla:pygame.Surface,cuadro_pregunta:dict, cuadro_respuestas:list, datos_juego:dict) -> bool:
    if type(pregunta_actual) != dict:
        return False
    mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual.get("pregunta"), (10,10), FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"], cuadro_pregunta["rectangulo"])

    opciones = ["opcion_A", "opcion_B", "opcion_C", "opcion_D"]

    for i in range(len(cuadro_respuestas)):
        if i in datos_juego["respuestas_ocultas"]:
            continue
        mostrar_texto(cuadro_respuestas[i]["superficie"],pregunta_actual.get(opciones[i], ""),(15,15),FUENTE_ARIAL_20,COLOR_BLANCO)
        pantalla.blit(cuadro_respuestas[i]["superficie"],cuadro_respuestas[i]["rectangulo"])

    return True

#COMODINES

def usar_x2(datos_juego:dict):
    if not datos_juego.get("x2_disponible"):
        return
    datos_juego["multiplicador_puntos"] = 2
    datos_juego["x2_disponible"] = False

def activar_bomba(datos_juego, pregunta_actual):
    if not datos_juego["bomba_disponible"]:
        return

    opciones = ["opcion_A", "opcion_B", "opcion_C", "opcion_D"]
    correcta = pregunta_actual["opcion_correcta"]

    incorrectas = []

    for i in range(4):
        if pregunta_actual[opciones[i]] != correcta:
            incorrectas.append(i)

    while len(incorrectas) > 2:
        incorrectas.pop(random.randint(0, len(incorrectas)-1))

    datos_juego["respuestas_ocultas"] = incorrectas

    datos_juego["bomba_disponible"] = False

def usar_doble_chance(datos_juego):
    if datos_juego.get("doble_chance_disponible"):
        datos_juego["doble_chance_en_uso"] = True
        datos_juego["doble_chance_fallo"] = False
        datos_juego["doble_chance_disponible"] = False

def usar_pasar(datos_juego:dict, lista_preguntas:list):
    if not datos_juego.get("pasar_disponible"):
        return

    pasar_pregunta(datos_juego, lista_preguntas)
    datos_juego["respuestas_ocultas"] = []
    datos_juego["doble_chance_en_uso"] = False
    datos_juego["doble_chance_fallo"] = False
    datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()
    datos_juego["pasar_disponible"] = False

def activar_doble_chance(datos_juego):
    if datos_juego["doble_chance_disponible"]:
        datos_juego["doble_chance_en_uso"] = True
        datos_juego["doble_chance_fallo"] = False
        datos_juego["doble_chance_disponible"] = False

def activar_x2(datos_juego):
    if datos_juego["x2_disponible"]:
        datos_juego["x2_activado"] = True
        datos_juego["x2_disponible"] = False

def activar_pasar(datos_juego, lista_preguntas):
    if datos_juego["pasar_disponible"]:
        pasar_pregunta(datos_juego, lista_preguntas)
        datos_juego["pasar_disponible"] = False
        datos_juego["respuestas_ocultas"] = []
        datos_juego["bomba_animando"] = False
        datos_juego["bomba_pendientes"] = []
        datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()


#ESTADISTICA

def reiniciar_estadisticas(datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        retorno = True
        datos_juego.update({
            "nombre": "",
            "tiempo_restante":TIEMPO_TOTAL,
            "puntuacion":0,
            "cantidad_vidas":CANTIDAD_VIDAS,
            "tiempo_inicio_pregunta": pygame.time.get_ticks(),
            "correctas_seguidas": 0,
            "respuestas_ocultas": [],
            "doble_chance_en_uso": False,
            "doble_chance_fallo": False,
            "x2_activado": False,
            "bomba_disponible": True,
            "x2_disponible": True,
            "pasar_disponible": True,
            "doble_chance_disponible": True,
        })
    else:
        retorno = False
    
    return retorno

def actualizar_tiempo(tiempo_inicio:float,tiempo_actual:float,datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        retorno = True
        tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)
        datos_juego["tiempo_restante"] = TIEMPO_TOTAL - tiempo_transcurrido
    else:
        retorno = False
        
    return retorno

def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False
        
    return retorno

def modificar_puntuacion(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += incremento
    else:
        retorno = False
        
    return retorno

def actualizar_tiempo_pregunta(datos_juego):
    tiempo_actual = pygame.time.get_ticks()
    transcurrido = (tiempo_actual - datos_juego["tiempo_inicio_pregunta"]) // 1000

    restante = TIEMPO_TOTAL - transcurrido
    if restante < 0:
        restante = 0

    datos_juego["tiempo_restante"] = restante

    if restante == 0:
        modificar_vida(datos_juego, VIDA_ERROR)
        datos_juego["correctas_seguidas"] = 0
        datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()
        return True

    return False

def manejar_aciertos_consecutivos(datos_juego, es_correcta):
    if es_correcta:
        datos_juego["correctas_seguidas"] += 1

        if datos_juego["correctas_seguidas"] == 5:
            modificar_vida(datos_juego, 1)
            datos_juego["correctas_seguidas"] = 0

    else:
        datos_juego["correctas_seguidas"] = 0


#AJUSTES

def barra_volumen(screen, x, y, ancho=200, alto=20, volumen_actual=0.5):
    pygame.draw.rect(screen, (180,180,180), (x, y, ancho, alto))

    relleno = int(ancho * volumen_actual)
    pygame.draw.rect(screen, (50,200,50), (x, y, relleno, alto))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:
        if x <= mouse[0] <= x + ancho and y <= mouse[1] <= y + alto:
            volumen_actual = (mouse[0] - x) / ancho
            volumen_actual = max(0, min(1, volumen_actual))
            pygame.mixer.music.set_volume(volumen_actual)

    return volumen_actual

def administrar_barra(datos_juego, pantalla):
    vol = datos_juego.get("volumen_musica", 0)
    vol = barra_volumen(pantalla, 150, 270, 500, 20, vol)
    datos_juego["volumen_musica"] = vol
    mostrar_texto(pantalla,"VOLUMEN", (290,200), FUENTE_ARIAL_50, color=COLOR_BLANCO)

#GAME_OVER

def manejar_texto_nombre(evento, datos_juego):
    nombre = datos_juego["nombre"]
    if evento.type == pygame.TEXTINPUT:
        if len(nombre) < 15:
            nombre += evento.text
    elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_BACKSPACE:
            nombre = nombre[:-1]
            datos_juego["ultimo_borrado"]
            
    datos_juego["nombre"] = nombre

def nombre_es_valido(nombre:str) -> bool:
    return 3 <= len(nombre) <= 15

def crear_boton_continuar(texto, x, y, ancho, alto, color_normal, color_inactivo, fuente, texto_x, texto_y, activo=True):
    rect = pygame.Rect(x, y, ancho, alto)

    return {
        "rect": rect,
        "texto": texto,
        "color_normal": color_normal,
        "color_inactivo": color_inactivo,
        "activo": activo,
        "fuente": fuente,
        "texto_x": texto_x, 
        "texto_y": texto_y
    }

def dibujar_boton_continuar(pantalla, boton):
    color = boton["color_normal"] if boton["activo"] else boton["color_inactivo"]
    pygame.draw.rect(pantalla, color, boton["rect"], border_radius=10)

    superficie_texto = boton["fuente"].render(boton["texto"], True, (0,0,0))
    pantalla.blit(superficie_texto, (boton["texto_x"], boton["texto_y"]))

def boton_clickeado_continuar(eventos, boton):
    if not boton["activo"]:
        return False

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton["rect"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                return True
    return False


