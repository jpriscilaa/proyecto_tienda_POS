import sqlite3
import uuid
from backend import Constantes

class Iva:
    def __init__(self, iva_id=None, nombre="", porcentaje=""):
        self.iva_id=iva_id or str(uuid.uuid4())
        self.nombre=nombre
        self.porcentaje=porcentaje  # puede ser string o float; tú eliges

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

    def guardar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()

        if Iva.existe(self.iva_id):
            cursor.execute(Constantes.UPDATE_IVA, (self.nombre, self.porcentaje, self.iva_id))
        else:
            cursor.execute(Constantes.INSERT_IVA, (self.iva_id, self.nombre, self.porcentaje))

        conexion.commit()
        conexion.close()

    def eliminar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM IVA WHERE IVA_ID=?", (self.iva_id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(iva_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM IVA WHERE IVA_ID=?", (iva_id,))
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            return Iva(*fila)
        else:
            return None
        
    @staticmethod
    def buscar_por_nombre(nombre):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM IVA WHERE NOMBRE=?", [nombre])
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            return Iva(*fila)
        else:
            return None

    @staticmethod
    def obtener_todos():
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM IVA")
        filas=cursor.fetchall()
        conexion.close()

        return [Iva(*fila) for fila in filas]

    @staticmethod
    def existe(iva_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT 1 FROM IVA WHERE IVA_ID=?", (iva_id,))
        resultado=cursor.fetchone()
        conexion.close()
        return resultado is not None

    @classmethod
    def borrar_por_id(cls, id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM IVA WHERE IVA_ID=?", (id,))
        conexion.commit()
        conexion.close()
