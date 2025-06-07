import sqlite3
import uuid
import json
from backend import Constantes
from backend.modelo.Cliente import Cliente

class Venta:
    def __init__(self, id= None, fecha= "", pago="", cliente = "", total = ""):
        self.id = id or str(uuid.uuid4())
        self.cliente = cliente
        self.total = float(total)

    def guardar(self):
        try:
            conexion = sqlite3.connect(Constantes.RUTA_BD)
            cursor = conexion.cursor()

            if Venta.existe(self.id):
                cursor.execute(
                    "UPDATE VENTA SET CLIENTE_ID = ?, TOTAL = ?, CANTIDAD_PRODUCTOS = ? WHERE VENTA_ID = ?",
                    (self.cliente.cliente_id, self.total, self.cantidad_productos, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO VENTA (VENTA_ID, CLIENTE_ID, TOTAL, CANTIDAD_PRODUCTOS) VALUES (?, ?, ?, ?)",
                    (self.id, self.cliente.cliente_id, self.total, self.cantidad_productos)
                )

            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            print("Error al guardar la venta:", str(e))
            return False

    def eliminar(self):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM VENTA WHERE VENTA_ID = ?", (self.id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(venta_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT VENTA_ID, CLIENTE_ID, TOTAL, CANTIDAD_PRODUCTOS FROM VENTA WHERE VENTA_ID = ?", (venta_id,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            cliente = Cliente.buscar_por_id(fila[1])
            return Venta(cliente=cliente, total=fila[2], cantidad_productos=fila[3], id=fila[0])
        return None

    @staticmethod
    def existe(venta_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM VENTA WHERE VENTA_ID = ?", (venta_id,))
        existe = cursor.fetchone()
        conexion.close()
        return existe is not None

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "cliente": self.cliente.nombre if self.cliente else None,
            "total": self.total,
            "cantidad_productos": self.cantidad_productos
        })