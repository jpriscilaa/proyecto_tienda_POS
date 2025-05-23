import sqlite3

database_name = 'backend/bddGestionTienda.db'

def get_connection():
    return sqlite3.connect(database_name)

def create_table():
    conexion = get_connection()
    query = conexion.cursor()
    print("Creando tabla Categoria...")

    query.execute('''
    CREATE TABLE "Categoria" (
        "categoria_id" TEXT NOT NULL UNIQUE,
        "nombre" TEXT NOT NULL,
        PRIMARY KEY("categoria_id")
    )
    ''')
    
    conexion.commit()
    conexion.close()
    print("Tabla Categoria creada correctamente.")


def main():
    create_table()

if __name__ == "__main__":
    main()
