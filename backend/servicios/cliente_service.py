# backend/service/cliente_service.py

from backend.modelo.Cliente import Cliente

def inicializar_cliente():
    Cliente.crear_tabla()

def guardar_cliente(cliente: Cliente):
    cliente.guardar()
def actualizar_cliente(cliente: Cliente):
    return cliente.actualizar()

def guardar_cliente_unico(cliente: Cliente):
    if Cliente.existe_documento(cliente.documento):
        raise ValueError("Ya existe un cliente con ese documento.")
    cliente.guardar()

def listar_clientes():
    return Cliente.listar_todos()

def obtener_cliente_por_id(id):
    return Cliente.obtener_por_id(id)

def obtener_cliente_por_documento(documento):
    return Cliente.obtener_por_documento(documento)

def eliminar_cliente(id):
    return Cliente.eliminar(id)

def actualizar_telefono_cliente(cliente: Cliente, nuevo_telefono: str):
    return cliente.actualizar_telefono(nuevo_telefono)

def existe_cliente_con_documento(documento):
    return Cliente.existe_documento(documento)
