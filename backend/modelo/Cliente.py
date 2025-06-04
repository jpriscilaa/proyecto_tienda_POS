import sqlite3
from backend import Constantes
from backend.bddTienda import get_connection
import uuid

class Cliente:
    def __init__(self, id=None, nombre="", apellido="",  documento="", telefono=""):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre.upper()
        self.apellido = apellido.upper()
        self.documento = documento.upper()
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} (Doc: {self.documento}, Tel: {self.telefono})"

    # --- Métodos CRUD ---

    
    def guardar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()

        if Cliente.existe(self.id):
            cursor.execute(Constantes.UPDATE_CLIENTE, (self.nombre, self.apellido, self.documento,self.id))
        else:
            cursor.execute(Constantes.INSERT_CLIENTE, (self.id, self.nombre))

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