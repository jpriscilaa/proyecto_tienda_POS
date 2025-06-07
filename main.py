import flet as ft
import logging
from backend.servicios import config_app
from app.iniciar_app import iniciar_app
from app.login_view import login_view
from backend.modelo.Config_Empresa import Config_Empresa
from backend import Constantes
from backend.servicios import config_empr_service
from app import ventana_alerta

def main(page: ft.Page):
    page.window.center=True
    page.window_icon="POS.ico"
    page.title=Constantes.NOMBRE_APP
    page.clean()

    #valido si todo está bien antes de inciar app
    if config_app.crearSQLITE() == False:
        if config_empr_service.existeEmpresa():
            logging.info("Si la salida del metodo es true significa que los datos de la empresa existen por ende podemos iniciar la app")
            logging.info("LANZAR LOGIN_VIEW")
            page.clean()
            page.add((login_view(page)))
        else:
            page.clean()
            page.add(iniciar_app(page))
            page.open(ventana_alerta.barra_error_mensaje("NO EXISTE DATOS DE EMPRES Y POR TANTO NO SE PUEDE ABRIR EL CRMV \nDEBE DE VOLVER A CREAR EMPRESA"))
            pass
    else: 
        logging.info("Si crearSQLITE devuelve true es porque justo ahora se acaba de crear la BD y por tanto no hay ningun dato en la tabla EMPRESA habrá que rellenarlo" \
        "eso significa que toca abrir la ventana de inicio donde poner la info de la empresa y ajustes de la app")
        logging.info("LANZAR INICIAR_APP")
        page.clean()
        page.add(iniciar_app(page))

if __name__ == "__main__":

    #Configurar logging global
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s (Archivo: %(filename)s | Línea: %(lineno)d)',
        datefmt='%d/%m/%Y %H:%M:%S',
        filename=Constantes.RUTA_LOG,   #Donde guardar los logs
        filemode='a'    #a significa que agrega linea al log, w seria para crear de 0
    )

    #Mostrar en consola además del archivo
    console=logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter=logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    #inicio de app
    ft.app(target=main, assets_dir="assets")
