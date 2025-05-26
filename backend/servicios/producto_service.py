from backend.modelo.Producto import Producto

def inicializar_producto():
    return Producto.crear_tabla()

def crear_producto(producto: Producto):
    return producto.guardar()

def obtener_producto(producto_id: str):
    return Producto.obtener_por_id(producto_id)

def actualizar_producto(producto: Producto):
    return producto.actualizar()  # Asegúrate que exista este método

def eliminar_producto(producto_id: str):
    return Producto.eliminar(producto_id)

def listar_productos():
    return Producto.listar_todos()

def productos_por_categoria(categoria_id: str):
    return Producto.obtener_por_categoria(categoria_id)
