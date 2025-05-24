from backend.bddTienda import get_connection

class Cliente:
    def __init__(self, id, nombre, documento, telefono):
        self.id = id
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} (Doc: {self.documento}, Tel: {self.telefono})"

    # --- Métodos CRUD ---

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla Cliente si no existe"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Cliente (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    documento TEXT UNIQUE,
                    telefono TEXT
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Error al crear tabla Cliente: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def guardar(self):
        """Guarda o actualiza el cliente en la base de datos"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO Cliente 
                (id, nombre, documento, telefono)
                VALUES (?, ?, ?, ?)
            ''', (self.id, self.nombre, self.documento, self.telefono))
            conn.commit()
        except Exception as e:
            print(f"Error al guardar cliente: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @classmethod
    def obtener_por_id(cls, id):
        """Obtiene un cliente por su ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, documento, telefono FROM Cliente WHERE id = ?",
                (id,)
            )
            fila = cursor.fetchone()
            return cls(*fila) if fila else None
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @classmethod
    def obtener_por_documento(cls, documento):
        """Obtiene un cliente por su número de documento"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, documento, telefono FROM Cliente WHERE documento = ?",
                (documento,)
            )
            fila = cursor.fetchone()
            return cls(*fila) if fila else None
        except Exception as e:
            print(f"Error al obtener cliente por documento: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @classmethod
    def listar_todos(cls):
        """Obtiene todos los clientes"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, documento, telefono FROM Cliente")
            return [cls(*fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error al listar clientes: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @classmethod
    def eliminar(cls, id):
        """Elimina un cliente por su ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Cliente WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # --- Métodos adicionales útiles ---
    @classmethod
    def existe_documento(cls, documento):
        """Verifica si ya existe un cliente con el documento dado"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM Cliente WHERE documento = ?",
                (documento,)
            )
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error al verificar documento: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def actualizar_telefono(self, nuevo_telefono):
        """Actualiza solo el teléfono del cliente"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Cliente SET telefono = ? WHERE id = ?",
                (nuevo_telefono, self.id)
            )
            conn.commit()
            self.telefono = nuevo_telefono
            return True
        except Exception as e:
            print(f"Error al actualizar teléfono: {e}")
            return False
        finally:
            if conn:
                conn.close()