import sqlite3
from backend import Constantes
from backend.bddTienda import get_connection
import uuid

class Cliente:
    def __init__(self, id=None, nombre="", apellido="",  documento="", telefono="",direccion=""):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.telefono = telefono
        self.direccion = direccion

    

    # --- Métodos CRUD ---

    
    def guardar(self):
        try:
            conexion = sqlite3.connect(Constantes.RUTA_BD)
            cursor = conexion.cursor()

            if Cliente.existe(self.id):
                cursor.execute(Constantes.UPDATE_CLIENTE, (self.nombre, self.apellido, self.documento,self.telefono,self.direccion,self.id))
            else:
                cursor.execute(Constantes.INSERT_CLIENTE, (self.id, self.nombre,self.apellido,self.documento,self.telefono,self.direccion))

            conexion.commit()
            conexion.close()
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: PRODUCTO.N_REFERENCIA" in str(error):
                print("Ya existe un producto con esa referencia o codigo de barras.")
                return False 
            elif "FOREIGN KEY constraint failed" in str(error):
                print("Error con la CATEGORIA o el IVA seleccionado no existen.")
                return False
        except Exception:
            print("Ha dado algún error en el insert del producto")
            return False


    def eliminar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM CLIENTE WHERE CLIENTE_ID = ?", (self.id))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(cliente_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM CLIENTE WHERE CLIENTE_ID = ?", (cliente_id))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Cliente(*fila)
        else:
            return None

    @staticmethod
    def obtener_todos():
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM CLIENTE")
        filas = cursor.fetchall()
        conexion.close()

        return [Cliente(*fila) for fila in filas]

    @staticmethod
    def existe(cliente_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM CLIENTE WHERE CLIENTE_ID = ?", (cliente_id,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    @classmethod
    def borrar_por_id(cls, id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(Constantes.DELETE_CLIENTE, (id))
        conexion.commit()
        conexion.close()