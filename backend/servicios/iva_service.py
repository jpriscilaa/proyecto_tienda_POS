from backend.bddTienda import get_connection
from backend.modelo.Iva import Iva

def crear_tabla_iva():
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

def agregar_iva(iva):
    print("conectando a la base de datos")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Iva (iva_id, nombre, porcentaje) VALUES (?, ?, ?)",
                   (iva.iva_id, iva.nombre, iva.porcentaje))
    print("inserta")
    conn.commit()
    conn.close()

def listar_ivas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT iva_id, nombre, porcentaje FROM Iva")
    ivas = [Iva(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    return ivas