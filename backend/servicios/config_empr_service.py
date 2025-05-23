from backend.bddTienda import get_connection
from backend.modelo.Config_Empresa import Config_Empresa

def inicializar_config_empresa():
    Config_Empresa.crear_tabla()

def guardar_datos_empresa(config_empresa):
    Config_Empresa.guardar(config_empresa)
