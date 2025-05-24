from backend.bddTienda import get_connection
from backend.modelo.Producto import Producto

class VentaLine:
    def __init__(self, linea_id, producto: Producto, cantidad, precio_stamp):
        self.linea_id = linea_id
        self.producto = producto
        self.cantidad = cantidad
        self.precio_stamp = precio_stamp

    def subtotal(self):
        """Calcula el total de esta línea de venta"""
        return self.cantidad * self.precio_stamp

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} - {self.subtotal()}€"

    # 1. CREAR TABLA (Create Table)
    @staticmethod
    def crear_tabla():
        """Crea la tabla si no existe"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS VentaLine (
                    linea_id TEXT PRIMARY KEY,
                    producto_id TEXT,
                    cantidad INTEGER CHECK(cantidad > 0),
                    precio_stamp REAL CHECK(precio_stamp >= 0),
                    FOREIGN KEY (producto_id) REFERENCES Producto(id)
                )
            ''')
            conn.commit()
            print("Tabla VentaLine creada correctamente")
        except Exception as e:
            print(f"Error al crear tabla: {e}")
        finally:
            conn.close()

    # 2. GUARDAR LÍNEA DE VENTA (Create)
    def guardar(self):
        """Guarda la línea de venta en la base de datos"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO VentaLine 
                (linea_id, producto_id, cantidad, precio_stamp)
                VALUES (?, ?, ?, ?)
            ''', (
                self.linea_id,
                self.producto.id,
                self.cantidad,
                self.precio_stamp
            ))
            conn.commit()
            print(f"Línea de venta {self.linea_id} guardada")
        except Exception as e:
            print(f"Error al guardar línea: {e}")
        finally:
            conn.close()

    # 3. OBTENER LÍNEA POR ID (Read)
    @staticmethod
    def obtener_por_id(linea_id):
        """Busca una línea de venta por su ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Usamos JOIN para traer los datos del producto
            cursor.execute('''
                SELECT vl.linea_id, vl.producto_id, vl.cantidad, vl.precio_stamp,
                       p.nombre, p.precio, p.categoria_id, p.iva_id
                FROM VentaLine vl
                JOIN Producto p ON vl.producto_id = p.id
                WHERE vl.linea_id = ?
            ''', (linea_id,))
            
            datos = cursor.fetchone()
            if datos:
                # Creamos el objeto Producto
                producto = Producto(
                    id=datos[1],
                    nombre=datos[4],
                    precio=datos[5],
                    categoria=None,  # Podrías completar esto si lo necesitas
                    iva=None       # Lo mismo aquí
                )
                return VentaLine(datos[0], producto, datos[2], datos[3])
            return None
        except Exception as e:
            print(f"Error al buscar línea: {e}")
            return None
        finally:
            conn.close()

    # 4. ACTUALIZAR LÍNEA (Update)
    def actualizar(self):
        """Actualiza los datos de la línea de venta"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE VentaLine 
                SET producto_id = ?, cantidad = ?, precio_stamp = ?
                WHERE linea_id = ?
            ''', (
                self.producto.id,
                self.cantidad,
                self.precio_stamp,
                self.linea_id
            ))
            conn.commit()
            print(f"Línea {self.linea_id} actualizada")
        except Exception as e:
            print(f"Error al actualizar: {e}")
        finally:
            conn.close()

    # 5. ELIMINAR LÍNEA (Delete)
    @staticmethod
    def eliminar(linea_id):
        """Elimina una línea de venta"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM VentaLine WHERE linea_id = ?",
                (linea_id,)
            )
            conn.commit()
            print(f"Línea {linea_id} eliminada")
        except Exception as e:
            print(f"Error al eliminar: {e}")
        finally:
            conn.close()

    # 6. LISTAR TODAS LAS LÍNEAS
    @staticmethod
    def listar_todas():
        """Obtiene todas las líneas de venta"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Consulta con JOIN para obtener datos del producto
            cursor.execute('''
                SELECT vl.linea_id, vl.producto_id, vl.cantidad, vl.precio_stamp,
                       p.nombre, p.precio
                FROM VentaLine vl
                JOIN Producto p ON vl.producto_id = p.id
            ''')
            
            lineas = []
            for datos in cursor.fetchall():
                producto = Producto(
                    id=datos[1],
                    nombre=datos[4],
                    precio=datos[5],
                    categoria=None,
                    iva=None
                )
                lineas.append(VentaLine(datos[0], producto, datos[2], datos[3]))
            
            return lineas
        except Exception as e:
            print(f"Error al listar líneas: {e}")
            return []
        finally:
            conn.close()