from backend.bddTienda import get_connection

class Usuario:
    def __init__(self, id, nombre_usuario, contrasena, rol):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self):
        return f"Usuario: {self.nombre_usuario} - Rol: {self.rol}"

    # 1. CREAR TABLA (Create Table)
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
            conn.close()

    # 2. GUARDAR USUARIO (Create)
    def guardar(self):
        """Guarda un nuevo usuario en la base de datos"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Usuario (id, nombre_usuario, contrasena, rol)
                VALUES (?, ?, ?, ?)
            ''', (self.id, self.nombre_usuario, self.contrasena, self.rol))
            conn.commit()
            print(f"Usuario {self.nombre_usuario} guardado correctamente")
        except Exception as e:
            print(f"Error al guardar usuario: {e}")
        finally:
            conn.close()

    # 3. OBTENER USUARIO POR ID (Read)
    @staticmethod
    def obtener_por_id(id_usuario):
        """Busca un usuario por su ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id_usuario,))
            usuario = cursor.fetchone()
            if usuario:
                return Usuario(*usuario)
            return None
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
        finally:
            conn.close()

    # 4. ACTUALIZAR USUARIO (Update)
    def actualizar(self):
        """Actualiza los datos del usuario"""
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
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
        finally:
            conn.close()

    # 5. ELIMINAR USUARIO (Delete)
    @staticmethod
    def eliminar(id_usuario):
        """Elimina un usuario por su ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuario WHERE id = ?", (id_usuario,))
            conn.commit()
            print(f"Usuario {id_usuario} eliminado correctamente")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
        finally:
            conn.close()

    # 6. LISTAR TODOS LOS USUARIOS
    @staticmethod
    def listar_todos():
        """Obtiene todos los usuarios registrados"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario")
            usuarios = [Usuario(*fila) for fila in cursor.fetchall()]
            return usuarios
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            conn.close()