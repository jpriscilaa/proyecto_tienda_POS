import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.modelo.Producto import Producto

from backend.bddTienda import get_connection
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva
from backend.servicios.categoria_service import listar_categorias
from backend.servicios.producto_service import  crear_producto, listar_productos
crear_producto(Producto("0","12345","coca",1.50,Categoria("1","bebidas"),Iva("1","general",21)))
productos = listar_productos()
print(productos[0])


