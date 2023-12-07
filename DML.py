import sqlite3 as ora

def create_database():
    """Crea la base de datos de highscore players"""
    connection = ora.connect("data/Meme_Game.db")
    connection.commit()
    connection.close()

def createTable():
    """Crea la tabla jugadores de highscore players"""
    try:
        create_database()
    except FileExistsError as error:
        print(error)
    connection = ora.connect("data/Meme_Game.db")
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT NULL,
        nombre TEXT,
        puntaje INT
        );'''
    )
    connection.commit()
    connection.close()

def insertRow(instruccion, parametro):
    """Inserta datos a la base de datos

    Args:
        instruccion (_type_): Debemos indicar una instruccion
        parametro (_type_): debemos indicar uno o varios parametros
    """
    connection = ora.connect("data/Meme_Game.db")
    cursor = connection.cursor()
    cursor.execute(instruccion, parametro.split(','))
    connection.commit()
    connection.close()

def readRows():
    """Imprime los datos de la base de datos"""
    connection = ora.connect("data/Meme_Game.db")
    cursor = connection.cursor()
    instruccion = "SELECT * FROM jugadores order by puntaje desc;"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    connection.commit()
    connection.close()
    print(datos)