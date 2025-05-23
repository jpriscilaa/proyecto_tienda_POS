from backend.modelo.Producto import Producto

class VentaLine:
    def __init__(self, linea_id, producto: Producto, cantidad, precio_stamp):
        self.linea_id = linea_id
        self.producto_id = producto
        self.cantidad = cantidad
        self.precio_stamp = precio_stamp

    def subtotal(self):
        return self.cantidad * self.precio_stamp

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} - {self.subtotal()}€"
