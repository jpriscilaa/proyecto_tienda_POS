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
