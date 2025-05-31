import sqlite3
import uuid
from backend import Constantes
from backend.bddTienda import get_connection

class Usuario:
    def __init__(self, id_usuario = None, nombre_usuario="", contrasena="", rol=""):
        self.id = id_usuario or str(uuid.uuid4())  
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self):
        return f"Usuario: {self.nombre_usuario} - Rol: {self.rol}"

    # --- CREAR TABLA ---
    @staticmethod
    def crear_tabla():
        """Crea la tabla de usuarios si no existe"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Usuario (
                    id TEXT PRIMARY KEY,
                    nombre_usuario TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("Tabla Usuario creada correctamente")
        except Exception as e:
            print(f"Error al crear tabla: {e}")
        finally:
            if conn:
                conn.close()

    # --- GUARDAR USUARIO ---
    def guardar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute(
        "INSERT INTO USUARIO (USUARIO_ID, NOMBRE, CONTRASENA, ROL) VALUES (?, ?, ?, ?)",
        (self.id, self.nombre_usuario, self.contrasena, self.rol)
    )
        conexion.commit()
        conexion.close()

    # --- OBTENER USUARIO POR ID ---
    @classmethod
    def obtener_por_id(cls, id_usuario):
        """Busca un usuario por su ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id_usuario,))
            usuario = cursor.fetchone()
            if usuario:
                return cls(*usuario)
            return None
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # --- OBTENER USUARIO POR NOMBRE DE USUARIO ---
    @classmethod
    def obtener_por_nombre_usuario(cls, nombre_usuario):
        """Busca un usuario por su nombre de usuario (para login)"""
        try:
            conexion = sqlite3.connect(Constantes.RUTA_BD)
            cursor = conexion.cursor()

            cursor.execute("SELECT USUARIO_ID, NOMBRE, CONTRASENA, ROL FROM USUARIO WHERE NOMBRE = ?", (nombre_usuario,))
            fila = cursor.fetchone()
            if fila:
                return cls(*fila)  # esto equivale a: Usuario(id, nombre_usuario, contrasena, rol)
            return None
        except Exception as e:
            print(f"Error al buscar usuario por nombre: {e}")
            return None
        finally:
            if conexion:
                conexion.close()

    # --- ACTUALIZAR USUARIO ---
    def actualizar(self):
        """Actualiza los datos del usuario existente"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Usuario 
                SET nombre_usuario = ?, contrasena = ?, rol = ?
                WHERE id = ?
            ''', (self.nombre_usuario, self.contrasena, self.rol, self.id))
            conn.commit()
            print(f"Usuario {self.id} actualizado correctamente")
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # --- ELIMINAR USUARIO ---
    @staticmethod
    def eliminar(id_usuario):
        """Elimina un usuario por su ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuario WHERE id = ?", (id_usuario,))
            conn.commit()
            print(f"Usuario {id_usuario} eliminado correctamente")
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # --- LISTAR TODOS LOS USUARIOS ---
    @classmethod
    def listar_todos(cls):
        """Obtiene todos los usuarios registrados"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario")
            usuarios = [cls(*fila) for fila in cursor.fetchall()]
            return usuarios
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            if conn:
                conn.close()


    @staticmethod
    def existe(id_usuario):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM USUARIO WHERE USUARIO_ID  = ?", (id_usuario,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None