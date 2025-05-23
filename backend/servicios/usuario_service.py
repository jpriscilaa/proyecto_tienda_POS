from backend.bddTienda import get_connection
def crear_tabla_usuario():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            id TEXT PRIMARY KEY,
            nombre_usuario TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def agregar_usuario(usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuario (id, nombre_usuario, contrasena, rol) VALUES (?, ?, ?, ?)",
                   (usuario.id, usuario.nombre_usuario, usuario.contrasena, usuario.rol))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_usuario, rol FROM Usuario")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios