from backend.bddTienda import get_connection

class Categoria:
    def __init__(self, categoria_id, nombre):
        self.categoria_id = categoria_id
        self.nombre = nombre

    def __str__(self):
        return self.nombre
    
    
def crear_tabla_categoria():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categoria (
            categoria_id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def listar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT categoria_id, nombre FROM Categoria")
    categorias = [Categoria(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return categorias

def crear_categoria(id, nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Categoria (categoria_id, nombre) VALUES (?, ?)", (id, nombre))
    conn.commit()
    conn.close()


def borrar_categoria(categoria_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Categoria WHERE categoria_id = ?", (categoria_id,))
    conn.commit()
    conn.close()
