from backend.bddTienda import get_connection
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva

class Producto:
    def __init__(self, id, n_referencia, nombre, precio, categoria: Categoria, iva: Iva):
        self.id = id
        self.n_referencia = n_referencia
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.iva = iva

    def __str__(self):
        return f"{self.nombre} - {self.precio}€ ({self.categoria}) - IVA: {self.iva}"

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla Producto con sus relaciones"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Producto (
                    id TEXT PRIMARY KEY,
                    n_referencia TEXT UNIQUE,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL CHECK(precio >= 0),
                    categoria_id TEXT NOT NULL,
                    iva_id TEXT NOT NULL,
                    FOREIGN KEY (categoria_id) REFERENCES Categoria(categoria_id),
                    FOREIGN KEY (iva_id) REFERENCES Iva(iva_id)
                )
            ''')
            conn.commit()
            print("Tabla Producto creada")
            return True
        except Exception as e:
            print(f"Error al crear tabla Producto: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def guardar(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO Producto (id, n_referencia, nombre, precio, categoria_id, iva_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.id,
                self.n_referencia,
                self.nombre,
                self.precio,
                self.categoria.categoria_id,
                self.iva.iva_id
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al guardar producto: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def obtener(cls, id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, n_referencia, nombre, precio, categoria_id, iva_id
                FROM Producto WHERE id = ?
            ''', (id,))
            row = cursor.fetchone()
            if row:
                cat = Categoria.obtener(row[4])
                iva = Iva.obtener(row[5])
                return Producto(row[0], row[1], row[2], row[3], cat, iva)
            return None
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def listar(cls):
        conn = get_connection()
        productos = []
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, n_referencia, nombre, precio, categoria_id, iva_id FROM Producto
            ''')
            rows = cursor.fetchall()
            for row in rows:
                cat = Categoria.obtener(row[4])
                iva = Iva.obtener(row[5])
                producto = Producto(row[0], row[1], row[2], row[3], cat, iva)
                productos.append(producto)
            return productos
        except Exception as e:
            print(f"Error al listar productos: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def borrar(cls, id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Producto WHERE id = ?', (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al borrar producto: {e}")
            return False
        finally:
            conn.close()
    @classmethod
    def buscar_por_referencia(cls, n_referencia):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, n_referencia, nombre, precio, categoria_id, iva_id
                FROM Producto WHERE n_referencia = ?
            ''', (n_referencia,))
            row = cursor.fetchone()
            if row:
                cat = Categoria.obtener(row[4])
                iva = Iva.obtener(row[5])
                return Producto(row[0], row[1], row[2], row[3], cat, iva)
            return None
        except Exception as e:
            print(f"Error al buscar por referencia: {e}")
            return None
        finally:
            conn.close()
    
    @classmethod
    def obtener_por_categoria(cls, categoria_id):
        conn = get_connection()
        productos = []
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, n_referencia, nombre, precio, categoria_id, iva_id
                FROM Producto WHERE categoria_id = ?
            ''', (categoria_id,))
            rows = cursor.fetchall()
            for row in rows:
                cat = Categoria.obtener(row[4])
                iva = Iva.obtener(row[5])
                productos.append(Producto(row[0], row[1], row[2], row[3], cat, iva))
            return productos
        except Exception as e:
            print(f"Error al obtener productos por categoría: {e}")
            return []
        finally:
            conn.close()    