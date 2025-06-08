import flet as ft
from backend import Constantes
from backend.modelo.Usuario import Usuario
from app import ventana_alerta
import logging
logger=logging.getLogger(__name__)

def login_view(page: ft.Page):

    #metodos
    def mostrar_dialogo():
        page.open(ventana_alerta.barra_error_mensaje("USUARIO O CONTRASEÑA INCORRECTOS"))

    def ir_a_menu(e):
        usuario=Usuario.obtener_por_nombre_usuario(usuario_login.value)
        #usuario va a recibir el usuario si existe, si no, devuelve none con eso valido con un if si existe y luego la contraseña
        if usuario and usuario.contrasena == contrasena_login.value:
            from app.dashboard_view import dashboard_view
            page.clean()
            page.add(dashboard_view(page, usuario))
        else:
            mostrar_dialogo()

    #elementos para la vista
    usuario_login=ft.TextField(label="Usuario", autofocus=True)
    contrasena_login=ft.TextField(label="Contraseña", password=True, can_reveal_password=True, on_submit=lambda e: ir_a_menu(e))

    login_container=ft.Container(
        width=320,
        height=420,
        padding=20,
        border_radius=20,
        alignment=ft.alignment.center,
        bgcolor=Constantes.COLOR_BORDE_CLARO,
        content=ft.Column(
            controls=[
                ft.Text("Iniciar Sesión", size=28, weight="bold"),
                usuario_login,
                contrasena_login,
                ft.Row([
                ft.ElevatedButton("Entrar", on_click=ir_a_menu),
                ft.ElevatedButton(
                    text="Salir",
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=lambda e: page.window.close()
                ),]
                ,alignment=ft.MainAxisAlignment.CENTER)

            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    fondo=ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_ACCENT_100, ft.Colors.BLUE_GREY_400]
        ),
        content=login_container
    )

    return fondo
