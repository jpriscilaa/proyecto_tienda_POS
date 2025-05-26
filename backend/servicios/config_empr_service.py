# backend/service/config_empresa_service.py

from backend.modelo.Config_Empresa import Config_Empresa

def inicializar_config_empresa():
    Config_Empresa.crear_tabla()

def guardar_config_empresa(config: Config_Empresa):
    config.guardar()

def obtener_config_empresa(empresa_id="empresa_001"):
    return Config_Empresa.obtener(empresa_id)

def existe_config_empresa(empresa_id="empresa_001"):
    return Config_Empresa.existe_empresa(empresa_id)

def eliminar_config_empresa(empresa_id="empresa_001"):
    return Config_Empresa.eliminar(empresa_id)

def actualizar_moneda_empresa(empresa_id, nueva_moneda):
    return Config_Empresa.actualizar_moneda(empresa_id, nueva_moneda)
