import sqlite3
import uuid
from backend import Constantes

class Categoria:
    def __init__(self, categoria_id=None, nombre=""):
        self.categoria_id = categoria_id or str(uuid.uuid4())
        self.nombre = nombre.upper()

    def guardar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()

        if Categoria.existe(self.categoria_id):
            cursor.execute(Constantes.UPDATE_CATEGORIA, (self.nombre, self.categoria_id))
        else:
            cursor.execute(Constantes.INSERT_CATEGORIA, (self.categoria_id, self.nombre))

        conexion.commit()
        conexion.close()

    def eliminar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM CATEGORIA WHERE CATEGORIA_ID = ?", (self.categoria_id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(categoria_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM CATEGORIA WHERE CATEGORIA_ID = ?", (categoria_id,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Categoria(*fila)
        else:
            return None

    @staticmethod
    def obtener_todos():
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM CATEGORIA")
        filas = cursor.fetchall()
        conexion.close()

        return [Categoria(*fila) for fila in filas]

    @staticmethod
    def existe(categoria_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM CATEGORIA WHERE CATEGORIA_ID = ?", (categoria_id,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    @classmethod
    def borrar_por_id(cls, id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(Constantes.DELETE_CATEGORIA, (id,))
        conexion.commit()
        conexion.close()