import sqlite3
from backend import Constantes
from backend.bddTienda import get_connection
import uuid

class Cliente:
    def __init__(self, cliente_id=None, cliente_nombre="", cliente_apellido="",  cliente_documento="", cliente_telefono="", cliente_direccion=""):
        self.id=cliente_id or str(uuid.uuid4())
        self.nombre=cliente_nombre
        self.apellido=cliente_apellido
        self.documento=cliente_documento
        self.telefono=cliente_telefono
        self.direccion=cliente_direccion

    # --- Métodos CRUD ---
    def guardar(self):
        try:
            conexion=sqlite3.connect(Constantes.RUTA_BD)
            cursor=conexion.cursor()

            if Cliente.existe(self.id):
                print("Aplicamos update")
                cursor.execute(Constantes.UPDATE_CLIENTE, (
                    self.nombre, self.apellido, self.documento,
                    self.telefono, self.direccion, self.id
                ))
            else:
                print("Aplicamos insert")
                cursor.execute(Constantes.INSERT_CLIENTE, (
                    self.id, self.nombre, self.apellido,
                    self.documento, self.telefono, self.direccion
                ))

            conexion.commit()
            conexion.close()
            return True  
        
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: CLIENTE.DOCUMENTO" in str(error):
                print("Ya existe un cliente con ese documento.")
            else:
                print("Error de integridad:", error)
            return False
        except Exception as e:
            print("Ha ocurrido un error al guardar el cliente:", e)
            return False


    def eliminar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM CLIENTE WHERE CLIENTE_ID=?", (self.id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(cliente_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM CLIENTE WHERE CLIENTE_ID=?", (cliente_id,))
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            return Cliente(*fila)
        else:
            return None

    @staticmethod
    def obtener_todos():
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM CLIENTE")
        filas=cursor.fetchall()
        conexion.close()

        return [Cliente(*fila) for fila in filas]

    @staticmethod
    def existe(cliente_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT 1 FROM CLIENTE WHERE CLIENTE_ID=?", (cliente_id,))
        resultado=cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    @classmethod
    def borrar_por_id(cls, id,):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute(Constantes.DELETE_CLIENTE(id,))
        conexion.commit()
        conexion.close()