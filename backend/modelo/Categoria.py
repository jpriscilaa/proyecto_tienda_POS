from backend.bddTienda import get_connection

class Categoria:
    def __init__(self, categoria_id, nombre):
        self.categoria_id = categoria_id
        self.nombre = nombre

    def __str__(self):
        return self.nombre
    
    
def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Categoria (categoria_id, nombre) VALUES (?, ?)",
            (self.categoria_id, self.nombre)
        )
        conn.commit()
        conn.close()

@classmethod
def crear_tabla(cls):
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

    # ✅ Método de clase para obtener todas las categorías como objetos Categoria
@classmethod
def listar_todas(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT categoria_id, nombre FROM Categoria")
        filas = cursor.fetchall()
        conn.close()

        # Creamos objetos Categoria con cls
        categorias = []
        for fila in filas:
            categoria = cls(fila[0], fila[1])  # cls = Categoria
            categorias.append(categoria)

        return categorias

    # ✅ Método de clase para borrar una categoría
@classmethod
def borrar_por_id(cls, categoria_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categoria WHERE categoria_id = ?", (categoria_id,))
        conn.commit()
        conn.close()