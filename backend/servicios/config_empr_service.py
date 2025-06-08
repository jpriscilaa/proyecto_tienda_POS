from backend.modelo.Config_Empresa import Config_Empresa
from backend import Constantes
from backend.servicios import config_app
import shutil
import os
import logging
log=logging.getLogger(__name__)

def crearEmpresa(empresa: Config_Empresa):
    empresa.guardar()
    log.info("recibimos empresa y guardamos empresa")

def borrar_conf():
    #Crear la carpeta conf si no existe, el exist ok es como decir, quieres que exista si o si no?
    ruta_config=os.path.join(config_app.ruta_ejecucion(), Constantes.RUTA_CARPETA_CONF)
    if os.path.exists(ruta_config) and os.path.isdir(ruta_config):
        shutil.rmtree(ruta_config) #borramos la carpeta para evitar corrupcion de datos

def existeEmpresa():
    logging.info("Aqui pongo la logica para validar si existen datos de la empresa en BD o está corrupta")
    #obtener clase config empresa
    empresa=Config_Empresa.obtener_config_empresa()
    if empresa and empresa.nombre:
        logging.info("Existe empresa")
        return True
    else:
        logging.info("Ha fallado, no existe empresa")
        borrar_conf()
        return False