import os
from backend import Constantes
import sqlite3

ruta_ejecucion = os.getcwd()
print("---------------------")
print("La ruta de la APP es: " + ruta_ejecucion)
print("---------------------")

def crearSQLITE():
    #Crear la carpeta conf si no existe
    os.makedirs(Constantes.RUTA_CARPETA_CONF, exist_ok=True)

    #Crear la ruta de la bd agregando la carpeta conf y bd
    rutaSQLITE = ruta_ejecucion + Constantes.RUTA_BD
    print("---------------------")
    print("La ruta de la BD es: " + rutaSQLITE)
    print("---------------------")
    if not os.path.exists(rutaSQLITE):
        conexion = sqlite3.connect(rutaSQLITE)
        cursor = conexion.cursor()

        crearTabla(cursor)

        conexion.commit()
        conexion.close()
        print(f"Base de datos '{rutaSQLITE}' creada con éxito.")
        return True
    else:
        print(f"La base de datos '{rutaSQLITE}' ya existe.")
        return False

def crearTabla(cursor):
        #Cramos las tablas necesarias
        cursor.execute(Constantes.CREATE_TABLA_CATEGORIA)
        cursor.execute(Constantes.CREATE_TABLA_CLIENTE)
        cursor.execute(Constantes.CREATE_TABLA_CONFIGURACION_APP)
        cursor.execute(Constantes.CREATE_TABLA_IVA)
        cursor.execute(Constantes.CREATE_TABLA_PRODUCTO)
        cursor.execute(Constantes.CREATE_TABLA_VENTA)
        cursor.execute(Constantes.CREATE_TABLA_VENTA_LINEA)