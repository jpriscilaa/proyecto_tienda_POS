from backend.modelo.Producto import Producto
from backend.modelo.Venta import Venta
from backend.modelo.Venta_Linea import Venta_Linea
from backend.modelo.Cliente import Cliente
from backend.modelo.Iva import Iva
from backend.modelo.Categoria import Categoria
from backend import Constantes
from app import ventana_alerta
import logging
from datetime import datetime

logger=logging.getLogger(__name__)

def crear_categoria():
    pass

def crear_iva():
    pass

def crear_cliente():
    cliente1=Cliente(
        cliente_nombre="Brian",
        cliente_apellido="Terr",
        cliente_direccion="s jorge",
        cliente_telefono="9999999"
    )
    cliente1.guardar()
    pass

def crear_venta():
    venta1=Venta(
        cliente=Cliente.buscar_por_id("d0f4f258-a653-4aec-b0ec-5bf5fe24da77"),
        fecha="01/01/2025",
        pago="TARJETA",
        total="100",
        cantidad_prod="10"
    )
    venta1.guardar()
    pass

def crear_venta_linea():
    pass

if __name__ == "__main__":
    # python -m tests.test_backend
    crear_venta()
    pass