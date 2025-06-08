import os
from backend import Constantes
import sqlite3
import logging
log=logging.getLogger(__name__)

def ruta_ejecucion():
    return os.getcwd()

def crearSQLITE():
    #Crear la carpeta conf si no existe, el exist ok es como decir, quieres que exista si o si no?
    ruta_config=os.path.join(ruta_ejecucion(), Constantes.RUTA_CARPETA_CONF)
    os.makedirs(ruta_config, exist_ok=True)

    #Crear la ruta de la bd agregando la carpeta conf y bd, uso os.path para que funciona bien en todos los sistemas operativos
    rutaSQLITE=os.path.join(ruta_ejecucion(), Constantes.RUTA_BD)
    log.info("---------------------")
    log.info("La ruta de la BD es: " + rutaSQLITE)
    log.info("---------------------")
    if not os.path.exists(rutaSQLITE):
        conexion=sqlite3.connect(rutaSQLITE)
        cursor=conexion.cursor()

        crearTabla(cursor)

        conexion.commit()
        conexion.close()
        log.info(f"Base de datos '{rutaSQLITE}' creada con éxito.")
        return True
    else:
        log.info(f"La base de datos '{rutaSQLITE}' ya existe.")
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
        cursor.execute(Constantes.CREATE_TABLA_USUARIO)

if __name__ == "__main__":
     pass
     