from backend.modelo.Config_Empresa import (
    crear_tabla_config_empresa,
    guardar_config_empresa,
    obtener_config_empresa,
    borrar_config_empresa,
)
from backend.modelo.Iva import obtener_iva_por_id
from backend.modelo.Config_Empresa import Config_Empresa


def inicializar_config_empresa():
    crear_tabla_config_empresa()


def guardar_config(empresa_id, nombre, direccion, telefono, iva_id, moneda):
    iva = obtener_iva_por_id(iva_id)
    config = Config_Empresa(
        empresa_id=empresa_id,
        nombre=nombre,
        direccion=direccion,
        telefono=telefono,
        iva=iva,
        moneda=moneda
    )
    guardar_config_empresa(config)


def obtener_config():
    return obtener_config_empresa()


def borrar_config():
    borrar_config_empresa()