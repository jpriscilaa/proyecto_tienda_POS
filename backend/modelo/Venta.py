from backend.bddTienda import get_connection
from backend.modelo.Cliente import Cliente
from backend.modelo.Usuario import Usuario
from backend.modelo.Venta_line import VentaLine
from backend.modelo.Producto import Producto  # Asegúrate de que Producto tiene un método para obtener por ID

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
            INSERT OR REPLACE INTO Venta (id, cliente_id, vendedor_id, fecha, total)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.cliente.id, self.vendedor.id, self.fecha, self.total))
        conn.commit()

        # Guardar líneas de venta
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

        # Elimina las líneas de la venta también
        cursor.execute("DELETE FROM VentaLine WHERE linea_id LIKE ?", (f"{id}%",))
        cursor.execute("DELETE FROM Venta WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Venta WHERE id = ?", (id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        # Obtener objetos relacionados
        cliente = Cliente.obtener_por_id(row[1])
        vendedor = Usuario.obtener_por_id(row[2])

        # Obtener líneas
        cursor.execute("SELECT * FROM VentaLine WHERE linea_id LIKE ?", (f"{id}%",))
        lineas_rows = cursor.fetchall()

        lineas = []
        for linea in lineas_rows:
            producto = Producto.obtener_por_id(linea[1])
            lineas.append(VentaLine(linea[0], producto, linea[2], linea[3]))

        venta = Venta(row[0], cliente, vendedor, lineas, row[3])
        conn.close()
        return venta

    @staticmethod
    def listar_todas():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Venta")
        ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        return [Venta.obtener_por_id(vid) for vid in ids]
