from backend.modelo.Venta import Venta
import uuid

class venta_Service:

    @staticmethod
    def crear_tabla():
        """Crea la tabla Venta"""
        Venta.crear_tabla()

    @staticmethod
    def guardar(venta: Venta):
        """Guarda una venta"""
        venta.guardar()

    @staticmethod
    def eliminar(id):
        """Elimina una venta y sus líneas"""
        Venta.borrar(id)

    @staticmethod
    def obtener(id):
        """Obtiene una venta por su ID"""
        return Venta.obtener_por_id(id)

    @staticmethod
    def listar():
        """Lista todas las ventas"""
        return Venta.listar_todas()

    @staticmethod
    def crear_venta(cliente, vendedor, lineas, fecha):
        """
        Crea una venta nueva con UUID y guarda.
        Las líneas deben estar preparadas (con cantidades, precios).
        """
        venta_id = str(uuid.uuid4())
        # Asignar IDs únicos a las líneas de venta (venta_id.1, venta_id.2...)
        for i, linea in enumerate(lineas):
            linea.linea_id = f"{venta_id}.{i+1}"
        venta = Venta(venta_id, cliente, vendedor, lineas, fecha)
        venta.guardar()
        return venta
