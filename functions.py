import re
import json as js
from DML import *
def draw_text(font, text, color, screen, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    screen.blit(textobj, textrect)

def guarda_score(lista_score, score):
    try:
        createTable()
    except Exception as error:
        print(error)

    diccionario = {}
    nombre = input("Ingrese su nombre (solo 3 letras o números): ")
    while not re.match(r'^[a-zA-Z0-9]{3}$', nombre):
        print("El nombre debe tener exactamente 3 letras o números.")
        nombre = input("Ingrese su nombre (solo 3 letras o números): ")
    diccionario['nombre'] = nombre
    diccionario['puntaje'] = score
    instruccion = "INSERT INTO jugadores (nombre, puntaje) VALUES (?,?)"
    parametro = f'{nombre}, {score}'                                   
    insertRow(instruccion, parametro)
    if lista_score:
        lista_score.append(diccionario)
        lista_ordenada = ordenar_burbujeo(lista_score)
        with open("Data/Highscore.json","w") as archivo:
            js.dump(lista_ordenada,archivo,indent = 2,separators=(", "," : "))
    else:
        lista_score.append(diccionario)
        lista_ordenada = ordenar_burbujeo(lista_score)
        with open("Data/Highscore.json","w") as archivo:
            js.dump(lista_ordenada,archivo,indent = 2,separators=(", "," : "))

def load_score():
    try:
        with open("Data/Highscore.json","r") as archivo:
            puntuaciones = js.load(archivo)  
    except FileNotFoundError:
        return False
    return puntuaciones

def ordenar_burbujeo(lista_numeros: list[int]):
    if not lista_numeros:
        print('La lista esta vacia')
    else:
        lista_copia = lista_numeros.copy()
        # Arranca nuestro algoritmo
        for indice_1 in range(len(lista_copia) - 1):
            for indice_2 in range(indice_1 + 1, len(lista_copia)):
                if lista_copia[indice_1].get("puntaje") < lista_copia[indice_2].get("puntaje"):
                    lista_copia[indice_1], lista_copia[indice_2] =\
                    lista_copia[indice_2], lista_copia[indice_1]
        return lista_copia