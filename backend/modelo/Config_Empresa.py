
from backend.bddTienda import get_connection
import sqlite3
class Config_Empresa:
    def __init__(self, empresa_id, nombre, direccion, telefono, moneda):
        self.empresa_id = empresa_id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.moneda = moneda

    def __str__(self):
        return f"{self.nombre} - {self.direccion} ({self.moneda})"

    # --- Métodos CRUD ---

    def crear_tabla_config_empresa():
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS config_empresa (
                empresa_id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                moneda TEXT
            )
        """)
            con.commit()
        except sqlite3.Error as e:
            print(f"Error creando tabla config_empresa: {e}")
        finally:
            con.close()


    def guardar_config_empresa(config: "Config_Empresa"):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO config_empresa (
            empresa_id, nombre, direccion, telefono, moneda
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        config.empresa_id,
        config.nombre,
        config.direccion,
        config.telefono,
        config.moneda
    ))
        con.commit()
        con.close()


    def obtener_config_empresa():
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM config_empresa LIMIT 1")
        fila = cur.fetchone()
        con.close()
        if fila:
            return Config_Empresa(
            empresa_id=fila[0],
            nombre=fila[1],
            direccion=fila[2],
            telefono=fila[3],
            moneda=fila[5]
        )
        return None


    def borrar_config_empresa():
        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM config_empresa")
        con.commit()
        con.close()