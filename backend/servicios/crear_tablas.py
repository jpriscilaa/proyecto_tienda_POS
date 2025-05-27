import sqlite3
from backend.modelo.Categoria import Categoria
from backend.modelo.Cliente import Cliente
from backend.modelo.Producto import Producto

def inicializar_tablas():
    """
    Inicializa las tablas de la base de datos.
    """
    Categoria.crear_tabla()
    Producto.crear_tabla()
    Cliente.crear_tabla()