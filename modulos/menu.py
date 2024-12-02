import pygame
import random
import modulos.colores as col
import modulos.funciones as mf
import modulos.constantes as mc



def menu_principal(pantalla:pygame.Surface, lista_pokemon:list[dict], lista_puntuaciones:list) -> None:
    """el menu principal del juego, donde se selecciona que va a hacer el jugador.

    Args:
        pantalla (pygame.Surface): la pantalla donde pegarlo.
        lista_pokemon (list[dict]): la lista con todos los pokemones.
        lista_puntuaciones (list): la lista de puntuaciones.
    """
    menu = True
    fuente = pygame.font.Font(mc.RUTA_FUENTE, 45)
    fondo = pygame.image.load(mc.FONDO_MENU_PRINCIPAL)
    titulo = "Pokemon"

    while menu:
        lista_eventos = pygame.event.get()

        pantalla.blit(fondo, (0, 0))
        titulo_juego = fuente.render(titulo, True, (255,255,255))
        pantalla.blit(titulo_juego,(270, 30))

        boton_jugar = mf.crear_boton(270, 130, 250, 100, col.ROJO, col.NEGRO, pantalla, fuente, "Jugar")
        boton_ranking = mf.crear_boton(270, 250, 250, 100, col.ROJO, col.NEGRO, pantalla, fuente, "Ranking")
        boton_salir = mf.crear_boton(270, 370, 250, 100, col.ROJO, col.NEGRO, pantalla, fuente, "Salir")

        for evento in lista_eventos:

            if evento.type == pygame.QUIT:
                menu = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = evento.pos

                jugar = boton_jugar.collidepoint(posicion_mouse)
                ranking = boton_ranking.collidepoint(posicion_mouse)
                salir = boton_salir.collidepoint(posicion_mouse)

                if jugar:
                    facil = menu_dificultad(pantalla)
                    pokemones_filtrados = menu_generacion(pantalla, lista_pokemon)

                    if len(pokemones_filtrados) != 0:
                        menu_partida(pantalla, pokemones_filtrados, facil, lista_puntuaciones)

                elif ranking:
                    menu_ranking(pantalla, lista_puntuaciones)

                elif salir:
                    menu = False

        pygame.display.update()

    pygame.quit()



def menu_partida(pantalla:pygame.Surface, lista_pokemon:list[dict], facil:bool, lista_puntuaciones:list) -> None:
    """menu donde se juega a adivinar el pokemon.

    Args:
        pantalla (pygame.Surface): la pantalla donde pegarlo.
        lista_pokemon (list[dict]): la lista con los pokemones de la partida.
        facil (bool): true juega en facil, false en normal.
        lista_puntuaciones (list): la lista de puntuaciones.
    """
    partida = True
    contador = 0
    pokemon_anterior = 0
    txt = ""
    fuente = pygame.font.Font(mc.RUTA_FUENTE, 45)
    fuente_stats = pygame.font.Font(mc.RUTA_FUENTE, 20)
    random.shuffle(lista_pokemon)
    tiempos = []
    mejor_tiempo = 0
    tiempo_anterior = 0
    color_texto = col.NEGRO
    sonido_correcto = pygame.mixer.Sound(mc.RUTA_RESPUESTA_CORRECTA_SONIDO)
    sonido_incorrecto = pygame.mixer.Sound(mc.RUTA_RESPUESTA_INCORRECTA_SONIDO)

    TIMEOVER = pygame.USEREVENT + 1
    PROXIMO_POKEMON = pygame.USEREVENT + 2
    FIN_PARTIDA = pygame.USEREVENT + 3
    mostrar = False
    
    opacidad_silueta = 255
    nombre_pokemon = lista_pokemon[contador]["nombre"]
    pokemon = pygame.image.load(lista_pokemon[contador]["ruta_imagen"])
    pokemon = pygame.transform.scale(pokemon, (350, 350))
    pokemon_silueta = pygame.image.load(lista_pokemon[contador]["ruta_silueta"])
    pokemon_silueta = pygame.transform.scale(pokemon_silueta, (350, 350))

    tiempo_inicial = pygame.time.get_ticks()
    while partida:
        lista_eventos = pygame.event.get()
        
        #cronometro
        if mostrar == False:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = mc.TIEMPO_ADIVINANZA - ((tiempo_actual - tiempo_inicial) / 1000)
            tiempo_transcurrido = round(tiempo_transcurrido, 2)

            #se acaba el tiempo
            if tiempo_transcurrido <= 0:
                event_timeover = pygame.event.Event(TIMEOVER)
                pygame.event.post(event_timeover)
                tiempo_transcurrido = 0.0


        pantalla.fill(col.ROJO_CLARO)
        pygame.draw.rect(pantalla, col.BLANCO, (200, 75, 400, 375), border_radius=10)

        #tiempo restante
        texto_tiempo = str(tiempo_transcurrido)
        mf.pegar_texto(pantalla, fuente_stats, col.NEGRO, (600, 0), f"restante: {tiempo_transcurrido}")

        #racha
        mf.pegar_texto(pantalla, fuente_stats, col.NEGRO, (10, 0), f"racha: {contador}")

        #mejor tiempo
        mf.pegar_texto(pantalla, fuente_stats, col.NEGRO, (290, 20), f"mejor tiempo: {mejor_tiempo}")

        #tiempo anterior
        mf.pegar_texto(pantalla, fuente_stats, col.NEGRO, (600, 40), f"anterior: {tiempo_anterior}")

        #tiempo promedio
        tiempo_promedio = mf.calcular_promedio(tiempos)
        mf.pegar_texto(pantalla, fuente_stats, col.NEGRO, (10, 40), f"promedio: {tiempo_promedio}")

        #pegar pokemon y silueta en la pantalla
        pantalla.blit(pokemon, (230, 75))
        if facil == False:
            pantalla.blit(pokemon_silueta, (230, 75))
            opacidad_silueta = mf.disminuir_opacidad(mostrar, opacidad_silueta, pokemon_silueta)

        #textbox
        mf.crear_boton(175, 450, 450, 100, (0,125,255), color_texto, pantalla, fuente, txt)

        mf.mostrar_nombre_idiomas(lista_pokemon[pokemon_anterior], pantalla, fuente_stats, mostrar)

        #acierta el pokemon
        if txt == nombre_pokemon.lower() and mostrar == False:
            contador += 1
            pokemon_anterior = contador - 1
            mostrar = True
            color_texto = col.VERDE
            sonido_correcto.play()
            tiempo_adivinar = mc.TIEMPO_ADIVINANZA - tiempo_transcurrido
            tiempo_adivinar = round(tiempo_adivinar, 2)
            tiempos.append(tiempo_adivinar)
            mejor_tiempo = min(tiempos)
            tiempo_anterior = tiempos[contador-1]
            pygame.time.set_timer(PROXIMO_POKEMON, 3000, 1)

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                partida = False

            elif evento.type == pygame.KEYDOWN and mostrar == False:
                codigo_ascii = evento.key
                txt = mf.comprobar_tecla(txt, codigo_ascii)

            elif evento.type == PROXIMO_POKEMON:

                if contador == 10:
                    pygame.time.set_timer(FIN_PARTIDA, 3000, 1)
                else:
                    mostrar = False
                    tiempo_inicial = pygame.time.get_ticks()
                    txt = ""
                    color_texto = col.NEGRO
                    opacidad_silueta = 255

                    nombre_pokemon = lista_pokemon[contador]["nombre"]
                    pokemon = pygame.image.load(lista_pokemon[contador]["ruta_imagen"])
                    pokemon = pygame.transform.scale(pokemon, (350, 350))
                    pokemon_silueta = pygame.image.load(lista_pokemon[contador]["ruta_silueta"])
                    pokemon_silueta = pygame.transform.scale(pokemon_silueta, (350, 350))

            elif evento.type == TIMEOVER:
                pokemon_anterior = contador
                mostrar = True
                color_texto = col.ROJO
                txt = lista_pokemon[contador]["nombre"]
                sonido_incorrecto.play()
                pygame.time.set_timer(FIN_PARTIDA, 3000, 1)

            elif evento.type == FIN_PARTIDA:

                if contador < 10:
                    tiempos.append(mc.TIEMPO_ADIVINANZA)
                    
                tiempo_total = mf.calcular_tiempo(tiempos)
                nombre = menu_fin_partida(pantalla, fuente, contador, tiempo_total)
                puntuacion = mf.crear_puntuacion(nombre, facil, contador, tiempo_total)
                lista_puntuaciones.append(puntuacion)
                mf.crear_csv("datos\\puntuacion.csv", lista_puntuaciones)
                partida = False
            
    
        pygame.display.update()



def menu_dificultad(pantalla:pygame.Surface) -> bool:
    """menu donde se selecciona la dificultad de la partida.

    Args:
        pantalla (pygame.Surface): la pantalla donde se pega.

    Returns:
        bool: true facil, false normal.
    """
    menu = True
    facil = False
    fuente = pygame.font.Font(mc.RUTA_FUENTE, 32)

    while menu:

        lista_eventos = pygame.event.get()

        pygame.draw.rect(pantalla, col.AZUL_CLARO, (305, 100, 180, 200), border_radius=20)
        boton_facil = mf.crear_boton(315, 110, 160, 80, col.ROJO, col.NEGRO, pantalla, fuente, "facil")
        boton_normal = mf. crear_boton(315, 210, 160, 80, col.ROJO,col.NEGRO, pantalla, fuente, "normal")

        for evento in lista_eventos:

            if evento.type == pygame.QUIT:
                menu = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = evento.pos
                
                if boton_facil.collidepoint(posicion_mouse):
                    facil = True
                    menu = False
                elif boton_normal.collidepoint(posicion_mouse):
                    menu = False


        pygame.display.update()

    return facil



def menu_generacion(pantalla:pygame.Surface, lista_pokemon:list[dict]) -> list[dict]:
    """menu donde se selecciona la generacion de pokemon que aparecera en la partida.

    Args:
        pantalla (pygame.Surface): la pantalla donde se pega.
        lista_pokemon (list[dict]): la lista con todos los pokemones.

    Returns:
        list[dict]: la lista con los pokemones correspondientes a la generacion seleccionada. 
    """
    menu = True
    fuente = pygame.font.Font(mc.RUTA_FUENTE, 32)
    pokemones_filtrados = []
    generacion = ""

    while menu:
        lista_eventos = pygame.event.get()

        pygame.draw.rect(pantalla, col.AZUL_CLARO, (220, 100, 300, 400), border_radius=20)
        boton_primera_gen = mf.crear_boton(230, 110, 80, 80, col.ROJO, col.NEGRO, pantalla, fuente, "1")
        boton_segunda_gen = mf.crear_boton(330, 110, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "2")
        boton_tercera_gen = mf.crear_boton(430, 110, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "3")
        boton_cuarta_gen = mf.crear_boton(230, 210, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "4")
        boton_quinta_gen = mf.crear_boton(330, 210, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "5")
        boton_sexta_gen = mf.crear_boton(430, 210, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "6")
        boton_septima_gen = mf.crear_boton(230, 310, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "7")
        boton_octava_gen = mf.crear_boton(330, 310, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "8")
        boton_novena_gen = mf.crear_boton(430, 310, 80, 80, col.ROJO,col.NEGRO, pantalla, fuente, "9")
        boton_todas_gen = mf.crear_boton(230, 410, 280, 80, col.ROJO,col.NEGRO, pantalla, fuente, "todas")

        for evento in lista_eventos:

            if evento.type == pygame.QUIT:
                menu = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = evento.pos

                if boton_primera_gen.collidepoint(posicion_mouse):
                    generacion = "primera"
                elif boton_segunda_gen.collidepoint(posicion_mouse):
                    generacion = "segunda"
                elif boton_tercera_gen.collidepoint(posicion_mouse):
                    generacion = "tercera"
                elif boton_cuarta_gen.collidepoint(posicion_mouse):
                    generacion = "cuarta"
                elif boton_quinta_gen.collidepoint(posicion_mouse):
                    generacion = "quinta"
                elif boton_sexta_gen.collidepoint(posicion_mouse):
                    generacion = "sexta"
                elif boton_septima_gen.collidepoint(posicion_mouse):
                    generacion = "septima"
                elif boton_octava_gen.collidepoint(posicion_mouse):
                    generacion = "octava"
                elif boton_novena_gen.collidepoint(posicion_mouse):
                    generacion = "novena"
                elif boton_todas_gen.collidepoint(posicion_mouse):
                    pokemones_filtrados = lista_pokemon
                    menu = False

                if generacion != "":
                    pokemones_filtrados = list(filter(lambda x:x["generacion"] == generacion, lista_pokemon))
                    menu = False


        pygame.display.update()


    return pokemones_filtrados



def menu_fin_partida(pantalla:pygame.surface, fuente:pygame.font, racha:int, tiempo:float) -> str:
    """el menu de final de partida.

    Args:
        pantalla (pygame.surface): la pantalla donde se pega.
        fuente (pygame.font): la fuente del texto.
        racha (int): la racha de la partida.
        tiempo (float): el tiempo total de partida.

    Returns:
        str: el nombre del jugador de esta partida.
    """

    nombre = ""
    ingresar = True

    if racha == 10:
        ruta_fondo = mc.FONDO_GANO
        color_txt = col.NEGRO
    else:
        ruta_fondo = mc.FONDO_PERDIO
        color_txt = col.BLANCO

    fondo = pygame.image.load(ruta_fondo)

    while ingresar:

        lista_eventos = pygame.event.get()
        pantalla.blit(fondo, (0, 0))

        mf. pegar_texto(pantalla, fuente, color_txt, (150, 50), f"racha: {racha}")
        mf.pegar_texto(pantalla, fuente, color_txt, (150, 100), f"tiempo total: {tiempo}")
        mf.pegar_texto(pantalla, fuente, color_txt, (150, 400), "ingrese un nombre")
        mf.crear_boton(175, 480, 450, 100, col.AZUL_CLARO, col.NEGRO, pantalla, fuente, nombre)

        for evento in lista_eventos:

            if evento.type == pygame.QUIT:
                ingresar = False

            elif evento.type == pygame.KEYDOWN:
                codigo_ascii = evento.key

                nombre = mf.comprobar_tecla(nombre, codigo_ascii)

                if evento.key == pygame.K_RETURN and nombre != "":
                    ingresar = False



        pygame.display.update()

    return nombre



def menu_ranking(pantalla:pygame.Surface, lista_puntuacion:list) -> None:
    """menu donde se muestran las mejores puntuaciones.

    Args:
        pantalla (pygame.Surface): la pantalla donde se pega.
        lista_puntuacion (list): la lista de puntuaciones.
    """
    ranking = True
    texto_ranking = ""
    fuente = pygame.font.Font(mc.RUTA_FUENTE, 24)

    lista_puntuacion = mf.buscar_puntos_maximos(lista_puntuacion)
    mf.bubble_sort_ascendente(lista_puntuacion, 3)

    while ranking:

        lista_eventos = pygame.event.get()

        pantalla.fill(col.ROJO_CLARO)

        aumento_y = 34
        aumento_x = 200
        y = 90

        mf.pegar_texto(pantalla, fuente, col.NEGRO, (340, 30), "ranking")

        boton_volver = mf.crear_boton(310, 510, 150, 75, col.ROJO, col.NEGRO, pantalla, fuente, "volver")



        for i in range(len(lista_puntuacion)):

            if i == 11:
                break

            texto_ranking = ""
            y += aumento_y
            x = 75
            
            if i > 0:
                mf.pegar_texto(pantalla, fuente, col.NEGRO, (30, y), f"{i}")

            for j in range(len(lista_puntuacion[i])):

                texto_ranking = f"{lista_puntuacion[i][j]}"
                mf.pegar_texto(pantalla, fuente, col.NEGRO, (x, y), texto_ranking)
                x += aumento_x
        

        for evento in lista_eventos:

            if evento.type == pygame.QUIT:
                ranking = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = evento.pos

                if boton_volver.collidepoint(posicion_mouse):
                    ranking = False


        pygame.display.update()