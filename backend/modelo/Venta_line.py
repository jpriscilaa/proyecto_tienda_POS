from backend.bddTienda import get_connection

from backend.modelo.Producto import Producto

class VentaLine:
    def __init__(self, linea_id, producto: Producto, cantidad, precio_stamp):
        self.linea_id = linea_id
        self.producto = producto
        self.cantidad = cantidad
        self.precio_stamp = precio_stamp

    def subtotal(self):
        return self.cantidad * self.precio_stamp

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} - {self.subtotal()}€"
    @staticmethod
    def crear_tabla():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS VentaLine (
                linea_id TEXT PRIMARY KEY,
                producto_id TEXT,
                cantidad INTEGER,
                precio_stamp REAL
            )
        ''')
        conn.commit()
        conn.close()

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            REPLACE INTO VentaLine (linea_id, producto_id, cantidad, precio_stamp)
            VALUES (?, ?, ?, ?)
        ''', (
            self.linea_id,
            self.producto.id,
            self.cantidad,
            self.precio_stamp
        ))
        conn.commit()
        conn.close()

