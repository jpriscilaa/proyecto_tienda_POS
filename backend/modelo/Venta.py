from backend.modelo.Cliente import Cliente
from backend.modelo.Usuario import Usuario
from backend.modelo.Venta_line import VentaLine
from backend.bddTienda import get_connection


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
    @staticmethod
    def crear_tabla():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Venta (
                id TEXT PRIMARY KEY,
                cliente_id TEXT,
                vendedor_id TEXT,
                fecha TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()

        # Guardamos la venta principal
        cursor.execute('''
            REPLACE INTO Venta (id, cliente_id, vendedor_id, fecha)
            VALUES (?, ?, ?, ?)
        ''', (
            self.id,
            self.cliente.id,
            self.vendedor.id,
            self.fecha
        ))

        # Guardamos las líneas de venta
        for linea in self.lineas:
            linea.guardar()

        conn.commit()
        conn.close()