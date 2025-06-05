import flet as ft
import logging
from backend.servicios import config_app
from app.iniciar_app import iniciar_app
from app.login_view import login_view
from backend.modelo.Config_Empresa import Config_Empresa
from backend import Constantes

def main(page: ft.Page):
    page.window.center=True
    page.window_icon = "POS.ico"
    page.title=Constantes.NOMBRE_APP
    page.clean()

    #valido si todo está bien antes de inciar app
    if config_app.crearSQLITE() == False:
        if existeEmpresa():
            print("Si la salida del metodo es true significa que los datos de la empresa existen por ende podemos iniciar la app")
            print("LANZAR LOGIN_VIEW")
            page.clean()
            page.add((login_view(page)))
    else: 
        print("Si crearSQLITE devuelve true es porque justo ahora se acaba de crear la BD y por tanto no hay ningun dato en la tabla EMPRESA habrá que rellenarlo" \
        "eso significa que toca abrir la ventana de inicio donde poner la info de la empresa y ajustes de la app")
        print("LANZAR INICIAR_APP")
        page.clean()
        page.add(iniciar_app(page))

def existeEmpresa():
    print("Aqui pongo la logica para validar si existen datos de la empresa en BD o está corrupta")
    #obtener clase config empresa
    empresa=Config_Empresa.obtener_config_empresa()
    if empresa.empresa_id:
        print("Existe empresa")
        return True
    else:
        print("Ha fallado, no existe empresa")
        return False

if __name__ == "__main__":

    #Configurar logging global
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        filename=Constantes.RUTA_LOG,   #Donde guardar los logs
        filemode='a'    #a significa que agrega linea al log, w seria para crear de 0
    )

    #mostrar en consola además del archivo
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    ft.app(target=main, assets_dir="assets")
