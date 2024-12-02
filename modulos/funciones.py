import json
import pygame
import modulos.colores as col
import modulos.constantes as mc


def leer_json(path:str, clave:str) -> list[dict]:
    """lee los datos de un json y los guarda en una lista.

    Args:
        path (str): ruta del archivo.
        clave (str): la clave a sacar dej json.

    Returns:
        list[dict]: los datos solicitados.
    """

    with open(path, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
        
    return datos[clave]



def crear_csv(path:str, lista:list) -> None:
    """crea un archivo csv donde guarda los datos enviados.

    Args:
        path (str): ruta del archivo.
        lista (list): los datos a guardar.
    """

    with open(path, "w", encoding="utf-8", newline="") as csv:
        csv.write("nombre,dificultad,puntos,tiempo\n")

        linea = []

        for i in range(1, len(lista)):

            for j in range(len(lista[i])):
                linea.append(str(lista[i][j]))

            linea = ",".join(linea)

            if len(lista)-1 != i:
                linea = linea + "\n"
            
            csv.write(linea)
            linea = []



def leer_csv(path:str, lista:list) -> None:
    """lee un archivo csv, convierte los datos y los guarda en una lista.

    Args:
        path (str): ruta del archivo.
        lista (list): lista donde cargar los datos leidos.
    """

    with open(path, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    
    lineas[0] = lineas[0].strip("\n")
    linea = lineas[0].split(",")
    lista.append(linea)
    
    for i in range(1, len(lineas)):
        linea = lineas[i].split(",")

        linea[2] = int(linea[2])
        linea[3] = linea[3].strip("\n")
        linea[3] = float(linea[3])

        
        lista.append(linea)



def comprobar_limite_caracteres(txt:str, max_caracteres:int) -> bool:
    """comprueba que la cadena enviada no se exceda del maximo de caracteres enviado.

    Args:
        txt (str): texto a comprobar.
        max_caracteres (int): el maximo de caracteres que puede tener el texto.

    Returns:
        bool: true si supera el maximo, false en caso contrario.
    """
    caracteres = len(txt)
    supera_maximo = False

    if caracteres > max_caracteres:
        supera_maximo = True

    return supera_maximo



def comprobar_tecla(txt:str, codigo_ascii:int) -> str:
    """comprueba que el codigo ascii enviado este en los parametros y si es asi lo suma a la cadena enviada.

    Args:
        txt (str): el texto al que se le agrega el caracter.
        codigo_ascii (int): el codigo del caracter ingresado.

    Returns:
        str: la cadena mas el nuevo caracter.
    """
    supera_maximo = comprobar_limite_caracteres(txt, 12)

    if codigo_ascii == 8: #backspace
        txt = txt[:len(txt)-1]

    if supera_maximo == False:
        if codigo_ascii == 32: #space
            txt += " "
        elif codigo_ascii >= 97 and codigo_ascii <= 122: #abecedario sin ñ
            txt += pygame.key.name(codigo_ascii)
        elif codigo_ascii >= 48 and codigo_ascii <= 57: #numeros
            txt += pygame.key.name(codigo_ascii)
    
    return txt



def crear_boton(x:int, y:int, ancho_boton:int, alto_boton:int, color:tuple,color_texto:tuple, 
                pantalla:pygame.Surface,fuente:pygame.font, texto:str) -> pygame.Surface:
    """crea un boton.

    Args:
        x (int): la posicion en x del boton.
        y (int): la posicion en y del boton.
        ancho_boton (int): el tamaño del ancho del boton.
        alto_boton (int): el tamaño del alto del boton.
        color (tuple): el color del boton.
        color_texto (tuple): el color del texto del boton.
        pantalla (pygame.Surface): la pantalla donde va a estar el boton.
        fuente (pygame.font): la fuente del texto.
        texto (str): el texto del boton.

    Returns:
        pygame.Surface: el boton creado.
    """

    boton = pygame.draw.rect(pantalla, color, (x, y, ancho_boton, alto_boton), border_radius=20)
    texto_boton = fuente.render(texto, True, color_texto)
    posicion_texto = texto_boton.get_rect(center=(x + ancho_boton // 2, y + alto_boton // 2))
    pantalla.blit(texto_boton, posicion_texto)

    return boton



def disminuir_opacidad(cambiar:bool, opacidad:int, pokemon_silueta:pygame.Surface) -> int:
    """disminuye la opacidad de la imagen enviada.

    Args:
        cambiar (bool): true para disminuir la opacidad, false para no hacer nada.
        opacidad (int): la opacidad del surface.
        pokemon_silueta (pygame.Surface): la imagen a reducir la opacidad.

    Returns:
        int: la nueva opacidad.
    """
    if cambiar and opacidad != 0:
        opacidad -= 5
        pokemon_silueta.set_alpha(opacidad)

    return opacidad



def pegar_texto(pantalla:pygame.surface, fuente:pygame.font, color:tuple, posicion:tuple, texto:str) -> None:
    """pega el texto enviado en la pantalla.

    Args:
        pantalla (pygame.surface): la pantalla donde se pega el texto.
        fuente (pygame.font): la fuente del texto.
        color (tuple): el color del texto.
        posicion (tuple): la posicion del texto.
        texto (str): el texto.
    """

    texto = fuente.render(texto, True, color)
    pantalla.blit(texto, posicion)



def calcular_promedio(lista:list) -> float:
    """calcula el promedio de la lista enviada.

    Args:
        lista (list): la lista a calcular el promedio.

    Returns:
        float: el promedio de toda la lista.
    """
    suma_total = 0
    promedio = 0
    
    if len(lista) != 0:
        for i in lista:
            suma_total += i

        promedio = suma_total / len(lista)
        promedio = round(promedio, 2)

    return promedio



def crear_puntuacion(nombre:str, facil:bool, puntos:int, tiempo:list) -> list:
    """crea una lista de puntuacion.

    Args:
        nombre (str): el nombre del jugador.
        facil (bool): la dificultad en que jugo, true = facil, false = normal.
        puntos (int): los puntos que consiguio.
        tiempo (list): el tiempo total de partida.

    Returns:
        list: la lista con la puntuacion.
    """
    dificultad = covertir_facil_dificil(facil)

    lista_puntuacion = [nombre, dificultad, puntos, tiempo]

    return lista_puntuacion

def covertir_facil_dificil(facil:bool) -> str:
    """convierte un booleano en facil o dificil.

    Args:
        facil (bool): true = facil, false = normal.

    Returns:
        str: una cadena que diga facil o normal.
    """
    retorno = "normal"

    if facil:
        retorno = "facil"

    return retorno



def calcular_tiempo(lista:list) -> float:
    """suma todos los tiempos de la lista enviada.

    Args:
        lista (list): lista con los tiempos.

    Returns:
        float: el tiempo total.
    """
    tiempo = 0

    for i in lista:
        tiempo += i

    return round(tiempo, 2)



def mostrar_nombre_idiomas(pokemon:dict, pantalla:pygame.Surface, fuente:pygame.font, mostrar:bool) -> None:
    """pega los nombres en otros idiomas del pokemon.

    Args:
        pokemon (dict): el diccionario con el pokemon
        pantalla (pygame.Surface): la pantalla donde pegar el texto.
        fuente (pygame.font): la fuente del texto.
        mostrar (bool): si debe imprimirse o no.
    """

    if mostrar:

        bandera_alemania = pygame.image.load(mc.BANDERA_ALEMANIA)
        bandera_francia = pygame.image.load(mc.BANDERA_FRANCIA)
        bandera_italia = pygame.image.load(mc.BANDERA_ITALIA)

        pantalla.blit(bandera_alemania, (60, 560))
        pegar_texto(pantalla, fuente, col.NEGRO, (100, 565), pokemon["nombre_aleman"])

        pantalla.blit(bandera_francia, (310, 560))
        pegar_texto(pantalla, fuente, col.NEGRO, (350, 565), pokemon["nombre_frances"])

        pantalla.blit(bandera_italia, (560, 560))
        pegar_texto(pantalla, fuente, col.NEGRO, (600, 565), pokemon["nombre_italiano"])



def buscar_puntos_maximos(lista_puntuaciones:list) -> list:
    """devuelve una lista con todos los jugadores que alcanzaron la puntuacion maxima.

    Args:
        lista_puntuaciones (list): la lista con todas las puntuaciones.

    Returns:
        list: la lista con los jugadoras que alcanzaron el maximo de puntos.
    """

    lista_puntos_maximos = []
    maximo_puntos = buscar_maximo_puntuacion(lista_puntuaciones)
    lista_puntos_maximos.append(lista_puntuaciones[0])

    for i in range(1, len(lista_puntuaciones)):

        if lista_puntuaciones[i][2] == maximo_puntos:
            lista_puntos_maximos.append(lista_puntuaciones[i])

    return lista_puntos_maximos



def buscar_maximo_puntuacion(lista_puntuaciones:list) -> int:
    """busca el maximo de puntos en la lista de puntuaciones.

    Args:
        lista_puntuaciones (list): la lista de puntuaciones.

    Returns:
        int: el puntaje maximo.
    """
    maximo = 0

    if len(lista_puntuaciones) != 0:
        for i in range(1, len(lista_puntuaciones)):
            if i == 0:
                maximo = lista_puntuaciones[i][2]
            else:
                if lista_puntuaciones[i][2] > maximo:
                    maximo = lista_puntuaciones[i][2]

    return maximo



def bubble_sort_ascendente(lista:list, indice:int) -> None:
    """ordena la matriz de manera descendente.

    Args:
        lista (list): la matriz a ordenar.
        indice (int): la columna por la cual ordenar.
    """

    if len(lista) == 0:
        return

    for j in range(1, len(lista)):
        intercambio = False    
        for i in range(1, len(lista)-1-j):
            if lista[i][indice] > lista[i+1][indice]:
                lista[i], lista[i+1] = lista[i+1], lista[i]
                intercambio = True
        if intercambio == False:
            break
    