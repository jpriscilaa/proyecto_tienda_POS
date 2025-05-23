from backend.bddTienda import get_connection

class Usuario:
    def __init__(self, id, nombre_usuario, contrasena, rol):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self):
        return f"{self.nombre_usuario} ({self.rol})"
    @staticmethod
    def crear_tabla():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                id TEXT PRIMARY KEY,
                nombre_usuario TEXT,
                contrasena TEXT,
                    rol TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            REPLACE INTO Usuario (id, nombre_usuario, contrasena, rol)
            VALUES (?, ?, ?, ?)
        ''', (self.id, self.nombre_usuario, self.contrasena, self.rol))
        conn.commit()
        conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_usuario, contrasena, rol FROM Usuario")
        usuarios = [Usuario(*row) for row in cursor.fetchall()]
        conn.close()
        return usuarios