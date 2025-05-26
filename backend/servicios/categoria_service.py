# backend/service/categoria_service.py

from backend.modelo.Categoria import Categoria

def inicializar_categoria():
    Categoria.crear_tabla()

def guardar_categoria(categoria: Categoria):
    categoria.guardar()

def listar_categorias():
    return Categoria.listar_todas()

def obtener_categoria_por_id(categoria_id):
    return Categoria.obtener_por_id(categoria_id)

def actualizar_categoria(categoria: Categoria):
    return categoria.actualizar()

def borrar_categoria(categoria_id):
    return Categoria.borrar_por_id(categoria_id)
