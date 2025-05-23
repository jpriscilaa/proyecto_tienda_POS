from backend.bddTienda import get_connection
def crear_tabla_venta():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Venta (
            id TEXT PRIMARY KEY,
            cliente_id TEXT,
            vendedor_id TEXT,
            fecha TEXT,
            total REAL,
            FOREIGN KEY (cliente_id) REFERENCES Cliente(id),
            FOREIGN KEY (vendedor_id) REFERENCES Usuario(id)
        )
    ''')
    conn.commit()
    conn.close()

def agregar_venta(venta):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Venta (id, cliente_id, vendedor_id, fecha, total) VALUES (?, ?, ?, ?, ?)",
                   (venta.id, venta.cliente.id, venta.vendedor.id, venta.fecha, venta.total))
    conn.commit()
    conn.close()

def listar_ventas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente_id, vendedor_id, fecha, total FROM Venta")
    ventas = cursor.fetchall()
    conn.close()
    return ventas
