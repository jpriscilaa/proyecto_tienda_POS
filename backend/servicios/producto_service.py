from backend.bddTienda import get_connection
from backend.modelo.Producto import Producto

def crear_tabla_producto():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Productos (
        producto_id TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        categoria_id TEXT NOT NULL,
        iva_id TEXT NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES Categoria(categoria_id),
        FOREIGN KEY (iva_id) REFERENCES Iva(iva_id)
    )
''')

    conn.commit()
    conn.close()

def listar_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT producto_id, nombre, precio, categoria_id, iva_id FROM Productos")
    return cursor.fetchall()

def crear_producto(id, nombre, precio, categoria_id, iva_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Productos VALUES (?, ?, ?, ?, ?)",
        (id, nombre, precio, categoria_id, iva_id)
    )
    conn.commit()
    conn.close()

def actualizar_producto(id, nombre, precio, categoria_id, iva_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Productos SET 
            nombre = ?, 
            precio = ?, 
            categoria_id = ?, 
            iva_id = ?
        WHERE producto_id = ?
    """, (nombre, precio, categoria_id, iva_id, id))
    conn.commit()
    conn.close()
