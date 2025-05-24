from backend.modelo.Iva import Iva
from backend.bddTienda import get_connection

class Config_Empresa:
    def __init__(self, empresa_id, nombre, direccion, telefono, iva: Iva, moneda):
        self.empresa_id = empresa_id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.iva = iva
        self.moneda = moneda

    def __str__(self):
        return f"{self.nombre} - {self.direccion} ({self.moneda})"

    # --- Métodos CRUD ---

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla Config_Empresa con sus relaciones"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Config_Empresa (
                    empresa_id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    iva_id TEXT NOT NULL,
                    moneda TEXT NOT NULL,
                    FOREIGN KEY (iva_id) REFERENCES Iva(iva_id)
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Error al crear tabla Config_Empresa: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def guardar(self):
        """Guarda o actualiza la configuración de la empresa"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO Config_Empresa
                (empresa_id, nombre, direccion, telefono, iva_id, moneda)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.empresa_id,
                self.nombre,
                self.direccion,
                self.telefono,
                self.iva.iva_id,
                self.moneda
            ))
            conn.commit()
        except Exception as e:
            print(f"Error al guardar configuración de empresa: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @classmethod
    def obtener(cls, empresa_id="empresa_001"):
        """Obtiene la configuración de la empresa por ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    ce.empresa_id, 
                    ce.nombre, 
                    ce.direccion, 
                    ce.telefono, 
                    ce.iva_id, 
                    ce.moneda,
                    i.nombre as iva_nombre,
                    i.valor as iva_valor
                FROM Config_Empresa ce
                JOIN Iva i ON ce.iva_id = i.iva_id
                WHERE ce.empresa_id = ?
            ''', (empresa_id,))
            
            row = cursor.fetchone()
            if row:
                iva_obj = Iva(row[4], row[6], row[7])  # iva_id, nombre, valor
                return cls(
                    empresa_id=row[0],
                    nombre=row[1],
                    direccion=row[2],
                    telefono=row[3],
                    iva=iva_obj,
                    moneda=row[5]
                )
            return None
        except Exception as e:
            print(f"Error al obtener configuración de empresa: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @classmethod
    def actualizar_moneda(cls, empresa_id, nueva_moneda):
        """Actualiza solo la moneda de la empresa"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Config_Empresa 
                SET moneda = ? 
                WHERE empresa_id = ?
            ''', (nueva_moneda, empresa_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar moneda: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @classmethod
    def eliminar(cls, empresa_id):
        """Elimina la configuración de la empresa"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM Config_Empresa 
                WHERE empresa_id = ?
            ''', (empresa_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar configuración de empresa: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # --- Métodos adicionales ---

    @classmethod
    def existe_empresa(cls, empresa_id="empresa_001"):
        """Verifica si existe la configuración de la empresa"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM Config_Empresa 
                WHERE empresa_id = ?
            ''', (empresa_id,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error al verificar empresa: {e}")
            return False
        finally:
            if conn:
                conn.close()