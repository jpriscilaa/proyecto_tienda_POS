# from backend.modelo.Config_Empresa import (
#     crear_tabla_config_empresa,
#     guardar_config_empresa,
#     obtener_config_empresa,
#     borrar_config_empresa,
# )
# from backend.modelo.Iva import obtener_iva_por_id
# from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Config_Empresa import Config_Empresa
import logging

def crearEmpresa(empresa: Config_Empresa):
    empresa.guardar()
    print("recibimos empresa e imprimos")
    pass

def existeEmpresa():
    logging.info("Aqui pongo la logica para validar si existen datos de la empresa en BD o está corrupta")
    #obtener clase config empresa
    empresa=Config_Empresa.obtener_config_empresa()
    if empresa and empresa.empresa_id:
        logging.info("Existe empresa")
        return True
    else:
        logging.info("Ha fallado, no existe empresa")
        return False

# def inicializar_config_empresa():
#     crear_tabla_config_empresa()


# def guardar_config(empresa_id, nombre, direccion, telefono, iva_id, moneda):
#     iva = obtener_iva_por_id(iva_id)
#     config = Config_Empresa(
#         empresa_id=empresa_id,
#         nombre=nombre,
#         direccion=direccion,
#         telefono=telefono,
#         iva=iva,
#         moneda=moneda
#     )
#     guardar_config_empresa(config)


# def obtener_config():
#     return obtener_config_empresa()


# def borrar_config():
#     borrar_config_empresa()