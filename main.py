import flet as ft
from app.router import route_app
from backend.servicios import config_app
from app.iniciar_app import iniciar_app

def main(page: ft.Page):
    route_app(page)

def comprobarConfiguracion():
    if config_app.crearSQLITE() == False:
        if existeEmpresa():
            print("Si la salida del metodo es true significa que los datos de la empresa existen por ende podemos iniciar la app")
            return True
    else: 
        print("Si crearSQLITE devuelve true es porque justo ahora se acaba de crear la BD y por tanto no hay ningun dato en la tabla EMPRESA habrá que rellenarlo" \
        "eso significa que toca abrir la ventana de inicio donde poner la info de la empresa y ajustes de la app")

def existeEmpresa():
    print("Aqui pongo la logica para validar si existen datos de la empresa en BD o está corrupta")

    return True

if __name__ == "__main__":
    if comprobarConfiguracion():
        #ft.app(target=main)
        print("Iniciamos APP")
    else: print("Ha fallado la iniciación de la APP")
