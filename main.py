import pygame
import modulos.funciones as mod
import modulos.menu as men
import modulos.constantes as mc

lista_pokemon = []
lista_puntuaciones = []

#inicializar pygame
pygame.init()
pygame.mixer.init()

#musica de fondo
pygame.mixer.music.load(mc.RUTA_MUSICA_FONDO)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

#configuracion inicial de la ventana
ventana = pygame.display.set_mode(mc.RESOLUCION_VENTANA)
pygame.display.set_caption(mc.TITULO_VENTANA)
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

#cargar pokemones
lista_pokemon = mod.leer_json("datos\\pokemon.json", "pokemon")
mod.leer_csv("datos\\puntuacion.csv", lista_puntuaciones)

#bucle principal del juego
men.menu_principal(ventana, lista_pokemon, lista_puntuaciones)