import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.bddTienda import get_connection
from backend.modelo.Categoria import Categoria

from backend.servicios.categoria_service import crear_tabla_categoria, agregar_categoria, listar_categorias
from backend.servicios.producto_service import crear_tabla_producto, crear_producto, listar_productos


productos = listar_productos()
print(productos[0])


