from backend.bddTienda import get_connection

class Iva:
    def __init__(self, iva_id, nombre, porcentaje):
        self.iva_id = iva_id
        self.nombre = nombre
        self.porcentaje = porcentaje

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

    # CREATE (Guardar)
    def guardar(self):
        """Guarda un nuevo tipo de IVA en la base de datos"""
        
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Iva (iva_id, nombre, porcentaje) VALUES (?, ?, ?)",
                (self.iva_id, self.nombre, self.porcentaje)
            )
            conn.commit()
            print(f"IVA {self.nombre} guardado correctamente")
            return True
        except Exception as e:
            print(f"Error al guardar IVA: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # READ (Obtener)
    @classmethod
    def obtener_por_id(cls, iva_id):
        """Obtiene un tipo de IVA por su ID"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT iva_id, nombre, porcentaje FROM Iva WHERE iva_id = ?",
                (iva_id,)
            )
            fila = cursor.fetchone()
            if fila:
                return cls(fila[0], fila[1], fila[2])
            return None
        except Exception as e:
            print(f"Error al obtener IVA: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # UPDATE (Actualizar)
    def actualizar(self):
        """Actualiza los datos del IVA en la base de datos"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Iva SET nombre = ?, porcentaje = ? WHERE iva_id = ?",
                (self.nombre, self.porcentaje, self.iva_id)
            )
            conn.commit()
            print(f"IVA {self.iva_id} actualizado correctamente")
            return True
        except Exception as e:
            print(f"Error al actualizar IVA: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # DELETE (Eliminar)
    @classmethod
    def borrar_por_id(cls, iva_id):
        """Elimina un tipo de IVA por su ID"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Iva WHERE iva_id = ?",
                (iva_id,)
            )
            conn.commit()
            print(f"IVA {iva_id} eliminado correctamente")
            return True
        except Exception as e:
            print(f"Error al eliminar IVA: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # LISTAR TODOS
    @classmethod
    def listar_todos(cls):
        """Obtiene todos los tipos de IVA"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT iva_id, nombre, porcentaje FROM Iva")
            filas = cursor.fetchall()
            return [cls(fila[0], fila[1], fila[2]) for fila in filas]
        except Exception as e:
            print(f"Error al listar IVAs: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # CREAR TABLA
    @classmethod
    def crear_tabla(cls):
        """Crea la tabla Iva si no existe"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Iva (
                    iva_id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    porcentaje REAL NOT NULL
                )
            ''')
            conn.commit()
            print("Tabla Iva creada/verificada correctamente")
            return True
        except Exception as e:
            print(f"Error al crear tabla Iva: {e}")
            return False
        finally:
            if conn:
                conn.close()