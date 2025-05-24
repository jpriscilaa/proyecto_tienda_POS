from backend.bddTienda import get_connection
from backend.modelo.Cliente import Cliente
from backend.modelo.Usuario import Usuario
from backend.modelo.Venta_line import VentaLine

class Venta:
    def __init__(self, id, cliente: Cliente, vendedor: Usuario, lineas: list[VentaLine], fecha):
        self.id = id
        self.cliente = cliente
        self.vendedor = vendedor
        self.lineas = lineas
        self.fecha = fecha
        self.total = self.calcular_total()

    def calcular_total(self):
        return sum(linea.subtotal() for linea in self.lineas)

    def __str__(self):
        return f"Venta nº{self.id} - Total: {self.total}€ - Cliente: {self.cliente.nombre}"

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Venta (id, cliente_id, vendedor_id, fecha, total)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.cliente.id, self.vendedor.id, self.fecha, self.total))
        conn.commit()

        # Guardar las líneas
        for linea in self.lineas:
            linea.guardar()
        conn.close()

    @staticmethod
    def crear_tabla():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Venta (
                id TEXT PRIMARY KEY,
                cliente_id TEXT NOT NULL,
                vendedor_id TEXT NOT NULL,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES Cliente(id),
                FOREIGN KEY (vendedor_id) REFERENCES Usuario(id)
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def borrar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Venta WHERE id = ?", (id,))
        conn.commit()
        conn.close()