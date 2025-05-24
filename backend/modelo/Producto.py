from backend.bddTienda import get_connection
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva

class Producto:
    def __init__(self, id, nombre, precio, categoria: Categoria, iva: Iva):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.iva = iva

    def __str__(self):
        return f"{self.nombre} - {self.precio}€ ({self.categoria}) - IVA: {self.iva}"

    # --- CRUD ---

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla Producto con sus relaciones"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Producto (
                    id TEXT PRIMARY KEY,
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
        """Guarda o actualiza el producto en la base de datos"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO Producto
                (id, nombre, precio, categoria_id, iva_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                self.id,
                self.nombre,
                self.precio,
                self.categoria.categoria_id,
                self.iva.iva_id
            ))
            conn.commit()
            print(f"Producto {self.nombre} guardado correctamente")
            return True
        except Exception as e:
            print(f"Error al guardar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @classmethod
    def obtener_por_id(cls, producto_id):
        """Obtiene un producto por su ID con todas sus relaciones"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Consulta con JOIN para obtener datos relacionados
            cursor.execute('''
                SELECT 
                    p.id, p.nombre, p.precio, 
                    p.categoria_id, c.nombre as categoria_nombre,
                    p.iva_id, i.nombre as iva_nombre, i.porcentaje as iva_porcentaje
                FROM Producto p
                LEFT JOIN Categoria c ON p.categoria_id = c.categoria_id
                LEFT JOIN Iva i ON p.iva_id = i.iva_id
                WHERE p.id = ?
            ''', (producto_id,))
            
            row = cursor.fetchone()
            if row:
                categoria = Categoria(row[3], row[4])
                iva = Iva(row[5], row[6], row[7])
                return cls(row[0], row[1], row[2], categoria, iva)
            return None
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @classmethod
    def listar_todos(cls):
        """Obtiene todos los productos con sus relaciones"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Consulta con JOIN para obtener datos relacionados
            cursor.execute('''
                SELECT 
                    p.id, p.nombre, p.precio, 
                    p.categoria_id, c.nombre as categoria_nombre,
                    p.iva_id, i.nombre as iva_nombre, i.porcentaje as iva_porcentaje
                FROM Producto p
                LEFT JOIN Categoria c ON p.categoria_id = c.categoria_id
                LEFT JOIN Iva i ON p.iva_id = i.iva_id
            ''')
            
            productos = []
            for row in cursor.fetchall():
                categoria = Categoria(row[3], row[4])
                iva = Iva(row[5], row[6], row[7])
                producto = cls(row[0], row[1], row[2], categoria, iva)
                productos.append(producto)
            
            return productos
        except Exception as e:
            print(f"Error al listar productos: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @classmethod
    def eliminar(cls, producto_id):
        """Elimina un producto por su ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Producto WHERE id = ?",
                (producto_id,)
            )
            conn.commit()
            print(f"Producto {producto_id} eliminado correctamente")
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # --- Métodos adicionales útiles ---

    @classmethod
    def obtener_por_categoria(cls, categoria_id):
        """Obtiene todos los productos de una categoría específica"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.nombre, p.precio, 
                       p.categoria_id, c.nombre as categoria_nombre,
                       p.iva_id, i.nombre as iva_nombre, i.porcentaje
                FROM Producto p
                LEFT JOIN Categoria c ON p.categoria_id = c.categoria_id
                LEFT JOIN Iva i ON p.iva_id = i.iva_id
                WHERE p.categoria_id = ?
            ''', (categoria_id,))
            
            productos = []
            for row in cursor.fetchall():
                categoria = Categoria(row[3], row[4])
                iva = Iva(row[5], row[6], row[7])
                productos.append(cls(row[0], row[1], row[2], categoria, iva))
            
            return productos
        except Exception as e:
            print(f"Error al obtener productos por categoría: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def calcular_precio_con_iva(self):
        """Calcula el precio del producto con IVA incluido"""
        return self.precio * (1 + (self.iva.porcentaje / 100))