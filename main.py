# pip install pygame in terminal
import pygame
import random
import math
from pygame import mixer    # para trabajar con sonidos
import cv2


# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni (2).png")
pygame.display.set_icon(icono)

# Fondo
fondo = pygame.image.load("tierra.jpg")

# Agregar música
mixer.music.load("stranger-things-124008.mp3")
mixer.music.set_volume(0.08)    # numero del 0 al 1 para gestionar el volumen
mixer.music.play(-1)    # -1 para que se repita una vez termine

# Variables del Jugador
img_jugador = pygame.image.load("ovni (2).png")
jugador_x = 368   # le restamos a 400 la mitad del ancho del icono del jugador = 64/2)
jugador_y = 520   # 600 - 64 aprox
jugador_x_cambio = 0

# Variables del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10

# Para crear multiples enemigos lo ideal seria seguir los principios de clases y herencias
# creando instancias de una clase 'enemigo'
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("nave-espacial.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(3)
    enemigo_y_cambio.append(50)

# Variables de la Bala
img_bala = pygame.image.load("bala (1).png")
bala_x = 368
bala_y = 520
bala_x_cambio = 0
bala_y_cambio = 8
bala_visible = False

# Variable Puntaje
puntaje = 0
fuente = pygame.font.Font('HIGHSENS.otf', 32)   # fuente que viene incorporada gratuitamente con pygame
texto_x = 20
texto_y = 20


# Texto final de juego
fuente_final = pygame.font.Font('HIGHSENS.otf', 50)


# Función del Jugador
# agregamos parámetros a la funcion(x, y) para poder actualizarlos cuando se mueva
def jugador(x, y):
    # blit() es un metodo que significa algo como 'arrojar'
    pantalla.blit(img_jugador, (x, y))


# Función del Enemigo
# agregamos parámetros a la funcion(x, y) para poder actualizarlos cuando se mueva
def enemigo(x, y, ene):
    # blit() es un metodo que significa algo como 'arrojar' (en pantalla)
    pantalla.blit(img_enemigo[ene], (x, y))


# Función disparar bala
def disparar_bala(x, y):
    # global nos permite convertir la variable en una variable con scope global
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))   # le sumamos pixeles para que aparezca en el medio de la nave


# Función detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))  # funcion matematica de la distancia
    if distancia < 25:
        return True
    else:
        return False


# Función mostrar puntaje
def mostrar_puntaje(x, y):
    # render significaria renderizar o mostrar en pantalla
    texto = fuente.render(f"Score: {puntaje}", True, (0, 0, 0))
    pantalla.blit(texto, (x, y))


def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (0, 0, 0))
    pantalla.blit(mi_fuente_final, (300, 200))


# LOOP DEL JUEGO
se_ejecuta = True
while se_ejecuta:

    # Color pantalla --> RGB wheel
    # Colocamos la pantalla arriba del codigo porque no queremos que la pantalla aparezca encima de los personajes
    # pantalla.fill((96, 18, 185))
    pantalla.blit(fondo, (0, 0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -4.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 4.5
            if evento.key == pygame.K_SPACE:
                # Cargamos aquí el sonido de la bala
                sonido_bala = mixer.Sound("silencer-effects.mp3")
                sonido_bala.set_volume(0.25)
                sonido_bala.play()  # lo hemos guardado en una variable para poder ejecutarlo (.play())
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicación Jugador
    jugador_x += jugador_x_cambio

    # Mantener dentro de bordes al Jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:  # 800 - 64 pixels
        jugador_x = 736

    # En el loop for que creamos a continuacion tenemos que añadir [e] en cada una de las variables de 'enemigo'
    # porque hemos creado una lista de enemigos en vez de instancias de una clase
    # 'mantener dentro de bordes al enemigo', 'colision', y la llamada a enemigo: 'enemigo(enemigo_x[e], enemigo_y[e], e)'
    # siguiendo el orden estarian mas abajo del codigo, pero necesitamos que entren en el loop for
    # porque todos ellos contienen variables de enemigo, que necesitan contar ahora con su indice correspondiente dentro del loop

    # Modificar ubicación Enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 456 and (350 < enemigo_x[e] < 450):
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000     # como la pantalla tiene 600 de alto, nos aseguramos que no se vea
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro de bordes al Enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -3
            enemigo_y[e] += enemigo_y_cambio[e]

    # Colisión
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("jab-jab.mp3")
            sonido_colision.set_volume(0.04)
            sonido_colision.play()
            bala_y = 520
            bala_visible = False
            puntaje += 100
            print(puntaje)
            # Para hacer si tocamos el enemigo desaparezca y aparezca uno de nuevo, lo ideal seria hacer una funcion
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= 0:
        bala_y = 520
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()
