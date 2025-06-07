
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