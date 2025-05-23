from backend.bddTienda import get_connection

from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva
class Producto:
    def __init__(self, id, nombre, precio, categoria: Categoria, iva: Iva):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.iva = iva

    def __str__(self):
        return f"{self.nombre} - {self.precio}€ - {self.categoria}"
    @staticmethod
    def crear_tabla():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Producto (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                precio REAL,
                categoria_id TEXT,
                iva_id TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            REPLACE INTO Producto (id, nombre, precio, categoria_id, iva_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.id,
            self.nombre,
            self.precio,
            self.categoria.categoria_id,
            self.iva.iva_id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, categoria_id, iva_id FROM Producto")
        productos = []

        for row in cursor.fetchall():
            producto_id, nombre, precio, categoria_id, iva_id = row

            # Creamos los objetos "relacionados"
            categoria = Categoria(categoria_id, "")  # puedes completar con nombre si lo necesitas
            iva = Iva(iva_id, 0)                     # lo mismo aquí

            producto = Producto(producto_id, nombre, precio, categoria, iva)
            productos.append(producto)

        conn.close()
        return productos