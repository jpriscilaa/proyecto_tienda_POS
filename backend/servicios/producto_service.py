from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva
from backend.modelo.Producto import Producto

def inicializar_producto():
    return Producto.crear_tabla()

def crear_producto(id, n_referencia, nombre, precio, categoria_id, iva_id):
    categoria = Categoria.obtener_por_id(categoria_id)
    iva = Iva.obtener_iva_por_id(iva_id)
    
    if not categoria or not iva:
        raise Exception("Categoría o IVA no encontrados")

    producto = Producto(id, n_referencia, nombre, precio, categoria, iva)
    return producto.guardar()

def obtener_producto(producto_id: str):
    return Producto.obtener(producto_id)

def actualizar_producto(producto: Producto):
    return producto.guardar()

def eliminar_producto(producto_id: str):
    return Producto.borrar(producto_id)

def listar_productos():
    return Producto.listar()

def productos_por_categoria(categoria_id: str):
    return Producto.obtener_por_categoria(categoria_id)
