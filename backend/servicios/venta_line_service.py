from backend.bddTienda import get_connection
def crear_tabla_venta_line():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VentaLine (
            linea_id TEXT PRIMARY KEY,
            producto_id TEXT,
            cantidad INTEGER,
            precio_stamp REAL,
            FOREIGN KEY (producto_id) REFERENCES Producto(id)
        )
    ''')
    conn.commit()
    conn.close()

def agregar_venta_line(linea):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO VentaLine (linea_id, producto_id, cantidad, precio_stamp) VALUES (?, ?, ?, ?)",
                   (linea.linea_id, linea.producto_id.id, linea.cantidad, linea.precio_stamp))
    conn.commit()
    conn.close()

def listar_venta_lines():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT linea_id, producto_id, cantidad, precio_stamp FROM VentaLine")
    lineas = cursor.fetchall()
    conn.close()
    return lineas