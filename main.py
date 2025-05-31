import flet as ft
from app.router import route_app
from backend.servicios import config_app
from app.iniciar_app import iniciar_app
from app.login_view import login_view


def main(page: ft.Page):   
    page.clean() 
    # Creo los dialogos necesarios para el login
    dlg_alerta = ft.AlertDialog(
        modal=True,
        title=ft.Text("Error de inicio de sesión"),
        content=ft.Text("Usuario o contraseña incorrectos"),
        actions=[ft.TextButton("OK", on_click=lambda e: cerrar_dialogo())],
        actions_alignment=ft.MainAxisAlignment.END
    )
    def mostrar_dialogo():
        print("Mostrando dialogo de alerta")
        page.dialog = dlg_alerta
        dlg_alerta.open = True
        page.update()
        print("Dialogo mostrado")

    def cerrar_dialogo():
        dlg_alerta.open = False
        page.update()

    #----------------------------------------------------------------------

    # page.add(iniciar_app(page))

    if config_app.crearSQLITE() == False:
        if existeEmpresa():
            print("Si la salida del metodo es true significa que los datos de la empresa existen por ende podemos iniciar la app")
            print("LANZAR LOGIN_VIEW")
            page.clean()
            page.add((login_view(page, mostrar_dialogo)))
            return True
    else: 
        print("Si crearSQLITE devuelve true es porque justo ahora se acaba de crear la BD y por tanto no hay ningun dato en la tabla EMPRESA habrá que rellenarlo" \
        "eso significa que toca abrir la ventana de inicio donde poner la info de la empresa y ajustes de la app")
        print("LANZAR INICIAR_APP")
        page.clean()
        page.add(iniciar_app(page))
        return False

def existeEmpresa():
    print("Aqui pongo la logica para validar si existen datos de la empresa en BD o está corrupta")

    return True

if __name__ == "__main__":
    ft.app(target=main)
