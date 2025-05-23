from backend.bddTienda import get_connection

class Cliente:
    def __init__(self, id, nombre, documento, telefono):
        self.id = id
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre}"

    @staticmethod
    def crear_tabla():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cliente (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                documento TEXT,
                telefono TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            REPLACE INTO Cliente (id, nombre, documento, telefono)
            VALUES (?, ?, ?, ?)
        ''', (self.id, self.nombre, self.documento, self.telefono))
        conn.commit()
        conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, documento, telefono FROM Cliente")
        clientes = [Cliente(*row) for row in cursor.fetchall()]
        conn.close()
        return clientes