# backend/service/iva_service.py

from backend.modelo.Iva import Iva

def inicializar_iva():
    return Iva.crear_tabla()

def crear_iva(iva: Iva):
    return iva.guardar()

def obtener_iva(iva_id):
    return Iva.obtener_por_id(iva_id)

def actualizar_iva(iva: Iva):
    return iva.actualizar()

def eliminar_iva(iva_id):
    return Iva.borrar_por_id(iva_id)

def listar_ivas():
    return Iva.listar_todos()
