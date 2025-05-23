from backend.bddTienda import get_connection

class Iva:
    def __init__(self, iva_id, nombre, porcentaje):
        self.iva_id = iva_id
        self.nombre = nombre
        self.porcentaje = porcentaje

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"
def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Iva (iva_id, nombre, porcentaje) VALUES (?, ?, ?)",
            (self.iva_id, self.nombre, self.porcentaje)
        )
        conn.commit()
        conn.close()

@classmethod
def crear_tabla(cls):
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
        conn.close()

@classmethod
def listar_todos(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT iva_id, nombre, porcentaje FROM Iva")
        filas = cursor.fetchall()
        conn.close()
        return [cls(f[0], f[1], f[2]) for f in filas]

@classmethod
def borrar_por_id(cls, iva_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Iva WHERE iva_id = ?", (iva_id,))
        conn.commit()
        conn.close()