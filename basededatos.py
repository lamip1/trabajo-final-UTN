import sqlite3


# En esta seccion importamos el modulo sqlite3 que permite trabajar con su base de datos.
# Es aqui donde tenemos las funciones principales sobre la base de datos, la creacion de la misma, como tambien tablas dentro de ella.
# El try nos permite capturar excepciones, es decir, si no se crea por alguna razon nos avisara con un mensaje de error.


# Creacion de la base de datos
def conexion_db():
    con = sqlite3.connect("composturatrabajos.db")
    return con


# Creacion de tabla
def tabla_db():
    con = conexion_db()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS clientes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             cliente varchar(20) NOT NULL,
             trabajo varchar(20) NOT NULL,
             precio INTEGER NOT NULL)
    """
    cursor.execute(sql)
    con.commit()


# Capturador de excepciones.
try:
    conexion_db()
    tabla_db()
except:
    print("Error o falla en db")
