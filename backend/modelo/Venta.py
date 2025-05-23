from backend.modelo.Cliente import Cliente
from backend.modelo.Usuario import Usuario
from backend.modelo.Venta_line import VentaLine

class Venta:
    def __init__(self, id, cliente: Cliente, vendedor: Usuario, lineas: list, fecha):
        self.id = id
        self.cliente = cliente
        self.vendedor = vendedor
        self.lineas: list[VentaLine] = lineas
        self.fecha = fecha
        self.total = self.calcular_total()
        

    def calcular_total(self):
        total = 0
        for linea in self.lineas:
            total += linea.subtotal()
            return total


    def __str__(self):
        return f"Venta nº{self.id} - Total: {self.total}€ - Cliente: {self.cliente.nombre}"
