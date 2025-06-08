import sqlite3
import uuid
from backend import Constantes
import logging
logger=logging.getLogger(__name__)

class Config_Empresa:
    def __init__(self, empresa_id=None, nombre="", direccion="", telefono="", moneda=""):
        self.empresa_id=empresa_id or str(uuid.uuid4())
        self.nombre=nombre.upper()
        self.direccion=direccion.upper()
        self.telefono=telefono.upper()
        self.moneda=moneda.upper()

    def guardar(self):  
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()

        if Config_Empresa.existe(self.empresa_id):
            cursor.execute(Constantes.UPDATE_CONFIG_EMPRESA, (self.nombre, self.direccion, self.telefono, self.moneda, self.empresa_id))
        else:
            cursor.execute(Constantes.INSERT_CONFIG_EMPRESA, (self.empresa_id, self.nombre, self.direccion, self.telefono, self.moneda))

        conexion.commit()
        conexion.close()

    def eliminar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM CONFIG_EMPRESA WHERE EMPRESA_ID=?", (self.empresa_id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(empresa_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM CONFIG_EMPRESA WHERE EMPRESA_ID=?", (empresa_id,))
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            return Config_Empresa(*fila)
        else:
            return None

    @staticmethod
    def existe(empresa_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT 1 FROM CONFIG_EMPRESA WHERE EMPRESA_ID=?", (empresa_id,))
        resultado=cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    @staticmethod
    def obtener_config_empresa():
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM CONFIG_EMPRESA LIMIT 1")
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            return Config_Empresa(*fila)
        else:
            return None
