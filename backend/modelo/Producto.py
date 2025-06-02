import sqlite3
import uuid
from backend import Constantes
from backend.bddTienda import get_connection
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva

class Producto:
    def __init__(self, id=None, n_referencia="", nombre="", precio="", categoria=None, iva=None):
        self.id = id or str(uuid.uuid4())
        self.n_referencia = n_referencia
        self.nombre = nombre.upper()
        try:
            self.precio = float(precio) if precio else 0.0
        except ValueError:
            self.precio = 0.0
        self.categoria = categoria
        self.iva = iva

    def __str__(self):
        return f"{self.nombre} - {self.precio}€ ({self.categoria}) - IVA: {self.iva}"

    def guardar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()

        if Producto .existe(self.id):
            cursor.execute(Constantes.UPDATE_PRODUCTO, (self.n_referencia, self.nombre, self.precio, self.categoria.categoria_id, self.iva.iva_id, self.id))
        else:
            cursor.execute(Constantes.INSERT_PRODUCTO, (self.id, self.n_referencia, self.nombre, self.precio, self.categoria.categoria_id, self.iva.iva_id))

        conexion.commit()
        conexion.close()

    def eliminar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM PRODUCTO WHERE PRODUCTO_ID = ?", (self.id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(producto_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PRODUCTO WHERE PRODUCTO_ID = ?", (producto_id,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Producto(*fila)
        else:
            return None

    @staticmethod
    def obtener_todos():
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PRODUCTO")
        filas = cursor.fetchall()
        conexion.close()

        return [Producto(*fila) for fila in filas]

    @staticmethod
    def existe(producto_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM PRODUCTO WHERE PRODUCTO_ID = ?", (producto_id,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    @classmethod
    def borrar_por_id(cls, id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM PRODUCTO WHERE PRODUCTO_ID = ?''', (id,))
        conexion.commit()
        conexion.close()