import sqlite3
import uuid
import json
from datetime import datetime
from backend import Constantes
from backend.modelo.Cliente import Cliente
import logging
log=logging.getLogger(__name__)

class Venta:
    def __init__(self, fecha, pago, cantidad_prod, total, id=None, cliente: Cliente=None):
        self.id = id or str(uuid.uuid4())
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.pago = pago
        self.cliente = cliente
        self.cantidad_prod = cantidad_prod
        self.total = float(str(total).replace(",", ".")) if total else 0.0

    def guardar(self):
        try:
            conexion = sqlite3.connect(Constantes.RUTA_BD)
            cursor = conexion.cursor()
            cliente_id = self.cliente.id if self.cliente else None
            if Venta.existe(self.id):
                cursor.execute(Constantes.UPDATE_VENTA, (
                    self.fecha, self.pago, cliente_id, self.cantidad_prod, self.total, self.id
                ))
            else:
                cursor.execute(Constantes.INSERT_VENTA, (
                    self.id, self.fecha, self.pago, cliente_id, self.cantidad_prod, self.total
                ))

            conexion.commit()
            conexion.close()
            return True
        except sqlite3.IntegrityError as error:
            log.info("Error de integridad en venta:", error)
            return False
        except Exception as e:
            log.info("Ha ocurrido un error al guardar la venta:", e)
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
        cursor.execute("SELECT * FROM VENTA WHERE VENTA_ID = ?", (venta_id,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            cliente = Cliente.buscar_por_id(fila[3])  
            return Venta(
                id=fila[0],
                fecha=fila[1],
                pago=fila[2],
                cliente=cliente,
                cantidad_prod=fila[4],
                total=fila[5]
            )
        else:
            return None

    @staticmethod
    def obtener_todos():
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM VENTA")
        filas = cursor.fetchall()
        conexion.close()

        ventas = []
        for fila in filas:
            cliente = Cliente.buscar_por_id(fila[3])
            venta = Venta(
                id=fila[0],
                fecha=fila[1],
                pago=fila[2],
                cliente=cliente,
                cantidad_prod=fila[4],
                total=fila[5]

            )
            ventas.append(venta)
        return ventas

    @staticmethod
    def existe(venta_id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM VENTA WHERE VENTA_ID = ?", (venta_id,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None

    @classmethod
    def borrar_por_id(cls, id):
        conexion = sqlite3.connect(Constantes.RUTA_BD)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM VENTA WHERE VENTA_ID = ?", (id,))
        conexion.commit()
        conexion.close()

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "fecha": self.fecha,
            "pago": self.pago,
            "cliente": f"{self.cliente.nombre} {self.cliente.apellido}" if self.cliente else None,
            "cantidad_prod": self.cantidad_prod,
            "total": self.total
        })
