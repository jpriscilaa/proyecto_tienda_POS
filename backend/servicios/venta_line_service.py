from backend.modelo.Venta_line import VentaLine
import uuid

class ventaLine_Service:

    @staticmethod
    def crear_tabla():
        """Crea la tabla VentaLine si no existe"""
        return VentaLine.crear_tabla()

    @staticmethod
    def guardar(venta_line: VentaLine):
        """Guarda una línea de venta"""
        return venta_line.guardar()

    @staticmethod
    def actualizar(venta_line: VentaLine):
        """Actualiza una línea de venta existente"""
        return venta_line.actualizar()

    @staticmethod
    def obtener(linea_id):
        """Obtiene una línea de venta por su ID"""
        return VentaLine.obtener_por_id(linea_id)

    @staticmethod
    def eliminar(linea_id):
        """Elimina una línea de venta por su ID"""
        return VentaLine.eliminar(linea_id)

    @staticmethod
    def listar():
        """Lista todas las líneas de venta"""
        return VentaLine.listar_todas()

    @staticmethod
    def crear_linea(producto, cantidad, precio_stamp):
        """
        Crea una línea de venta con ID aleatorio y la guarda.
        Se espera un objeto Producto ya cargado.
        """
        linea_id = str(uuid.uuid4())
        linea = VentaLine(linea_id, producto, cantidad, precio_stamp)
        return linea.guardar()
