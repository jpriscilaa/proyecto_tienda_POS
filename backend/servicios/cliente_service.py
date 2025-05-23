from backend.bddTienda import get_connection

def crear_tabla_cliente():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            documento TEXT,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()

def agregar_cliente(cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cliente (id, nombre, documento, telefono) VALUES (?, ?, ?, ?)", 
                   (cliente.id, cliente.nombre, cliente.documento, cliente.telefono))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, documento, telefono FROM Cliente")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def borrar_cliente(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cliente WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()