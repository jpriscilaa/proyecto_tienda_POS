from backend.bddTienda import get_connection

class Categoria:
    def __init__(self, categoria_id, nombre):
        self.categoria_id = categoria_id
        self.nombre = nombre

    def __str__(self):
        return f"Categoría: {self.nombre} (ID: {self.categoria_id})"

    # --- CRUD ---

    # CREATE (Guardar categoría)
    def guardar(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
    "INSERT OR REPLACE INTO Categoria (categoria_id, nombre) VALUES (?, ?)",
    (self.categoria_id, self.nombre)
)

            
            conn.commit()
        except Exception as e:
            print(f"Error al guardar categoría: {e}")
            raise
        finally:
            if conn:
                conn.close()

    # READ (Obtener todas las categorías)
    @classmethod
    def listar_todas(cls):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria_id, nombre FROM Categoria")
            filas = cursor.fetchall()
            return [cls(fila[0], fila[1]) for fila in filas]  # Lista de objetos Categoria
        except Exception as e:
            print(f"Error al listar categorías: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # READ (Obtener categoría por ID)
    @classmethod
    def obtener_por_id(cls, categoria_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT categoria_id, nombre FROM Categoria WHERE categoria_id = ?",
                (categoria_id,)
            )
            fila = cursor.fetchone()
            return cls(fila[0], fila[1]) if fila else None
        except Exception as e:
            print(f"Error al obtener categoría: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # UPDATE (Actualizar categoría)
    def actualizar(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Categoria SET nombre = ? WHERE categoria_id = ?",
                (self.nombre, self.categoria_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar categoría: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # DELETE (Eliminar categoría)
    @classmethod
    def borrar_por_id(cls, categoria_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Categoria WHERE categoria_id = ?",
                (categoria_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al borrar categoría: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # --- Métodos auxiliares ---
    @classmethod
    def crear_tabla(cls):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Categoria (
                    categoria_id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Error al crear tabla: {e}")
        finally:
            if conn:
                conn.close()