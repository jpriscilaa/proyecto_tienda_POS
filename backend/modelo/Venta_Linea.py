import sqlite3
import uuid
import json
from backend import Constantes
from backend.modelo.Producto import Producto
from backend.modelo.Venta import Venta

class Venta_Linea:
    def __init__(self, venta: Venta, producto: Producto, cantidad, precio_unitario, iva, total_linea, id=None):
        self.id = id or str(uuid.uuid4())
        self.venta = venta
        self.producto = producto
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
        self.iva = float(iva)
        self.total_linea = float(total_linea)

    def guardar(self):
        try:
            conexion = sqlite3.connect(Constantes.RUTA_BD)
            cursor = conexion.cursor()

            if Venta_Linea.existe(self.id):
                cursor.execute("""
                    UPDATE LINEA_VENTA SET VENTA_ID = ?, PRODUCTO_ID = ?, CANTIDAD = ?, 
                    PRECIO_UNITARIO = ?, IVA = ?, TOTAL_LINEA = ? WHERE LINEA_ID = ?
                """, (self.venta.id, self.producto.id, self.cantidad, self.precio_unitario, self.iva, self.total_linea, self.id))
            else:
                cursor.execute("""
                    INSERT INTO LINEA_VENTA (LINEA_ID, VENTA_ID, PRODUCTO_ID, CANTIDAD, PRECIO_UNITARIO, IVA, TOTAL_LINEA)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.id, self.venta.id, self.producto.id, self.cantidad, self.precio_unitario, self.iva, self.total_linea))

            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            print("Error al guardar la línea de venta:", str(e))
            return False

    def eliminar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM LINEA_VENTA WHERE LINEA_ID = ?", (self.id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(linea_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT LINEA_ID, VENTA_ID, PRODUCTO_ID, CANTIDAD, PRECIO_UNITARIO, IVA, TOTAL_LINEA
            FROM LINEA_VENTA WHERE LINEA_ID = ?
        """, (linea_id,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            venta = Venta.buscar_por_id(fila[1])
            producto = Producto.buscar_por_id(fila[2])
            return Venta_Linea(venta, producto, fila[3], fila[4], fila[5], fila[6], id=fila[0])
        return None

    @staticmethod
    def existe(linea_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM LINEA_VENTA WHERE LINEA_ID = ?", (linea_id,))
        existe = cursor.fetchone()
        conexion.close()
        return existe is not None
    
    @staticmethod
    def obtener_por_venta(venta_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT LINEA_ID, VENTA_ID, PRODUCTO_ID, CANTIDAD, PRECIO_UNITARIO, IVA, TOTAL_LINEA
            FROM LINEA_VENTA
            WHERE VENTA_ID = ?
        """, (venta_id,))
        filas = cursor.fetchall()
        conexion.close()

        lineas = []
        for fila in filas:
            venta = Venta.buscar_por_id(fila[1])
            producto = Producto.buscar_por_id(fila[2])
            linea = LineaVenta(
                venta=venta,
                producto=producto,
                cantidad=fila[3],
                precio_unitario=fila[4],
                iva=fila[5],
                total_linea=fila[6],
                id=fila[0]
            )
            lineas.append(linea)
        return lineas

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "venta_id": self.venta.id,
            "producto": self.producto.nombre if self.producto else None,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "iva": self.iva,
            "total_linea": self.total_linea
        })