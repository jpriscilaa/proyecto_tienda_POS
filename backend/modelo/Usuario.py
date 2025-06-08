import sqlite3
import uuid
from backend import Constantes
from backend.bddTienda import get_connection
import logging
log=logging.getLogger(__name__)

class Usuario:
    def __init__(self, id_usuario=None, nombre_usuario="",trabajador="", apellido="", ntelefono="", contrasena="", rol=""):
        self.id=id_usuario or str(uuid.uuid4())  
        self.nombre_usuario=nombre_usuario
        self.trabajador=trabajador
        self.apellido=apellido
        self.ntelefono=ntelefono
        self.contrasena=contrasena
        self.rol=rol

    def __str__(self):
        return f"Usuario: {self.nombre_usuario} - Rol: {self.rol}"

    
    # --- GUARDAR USUARIO ---
    def guardar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        if Usuario.existe(self.id):
            cursor.execute(Constantes.UPDATE_USUARIO, (self.nombre_usuario, self.trabajador,self.apellido,self.ntelefono,self.contrasena, self.rol,self.id))
        else:
            cursor.execute(Constantes.INSERT_USUARIO, (self.id,self.nombre_usuario, self.trabajador,self.apellido,self.ntelefono,self.contrasena, self.rol))

        conexion.commit()
        conexion.close()

    def eliminar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM USUARIO WHERE USUARIO_ID=?", (self.id,))
        conexion.commit()
        conexion.close()

    # --- Buscar por ID ---
    @staticmethod
    def buscar_por_id(id_usuario):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT USUARIO_ID, NOMBRE, TRABAJADOR_NOMBRE, APELLIDO,NTELEFONO, CONTRASENA, ROL WHERE USUARIO_ID=?", (id_usuario,))
        fila=cursor.fetchone()
        conexion.close()
        if fila:
            return Usuario(*fila)
        return None

    # --- Obtener todos ---
    @staticmethod
    def obtener_todos():
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM USUARIO")
        filas=cursor.fetchall()
        conexion.close()
        return [Usuario(*fila) for fila in filas]

    # --- Verificar existencia por ID ---
    @staticmethod
    def existe(id_usuario):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT 1 FROM USUARIO WHERE USUARIO_ID=?", (id_usuario,))
        resultado=cursor.fetchone()
        conexion.close()
        return resultado is not None

    # --- Borrar por ID (class method con constante SQL) ---
    @classmethod
    def borrar_por_id(cls, id_usuario):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute(Constantes.DELETE_USUARIO, (id_usuario,))
        conexion.commit()
        conexion.close()
    
    @classmethod
    def obtener_por_nombre_usuario(cls, nombre_usuario):
    
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM USUARIO WHERE NOMBRE=?", (nombre_usuario,))
        fila=cursor.fetchone()
        if fila:
            return cls(*fila)  
        return None
 
            
