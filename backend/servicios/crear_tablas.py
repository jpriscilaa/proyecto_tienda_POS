import sqlite3
from backend.modelo.Categoria import Categoria

def inicializar_tablas():
    """
    Inicializa las tablas de la base de datos.
    """
    Categoria.crear_tabla()