import flet as ft

from backend.modelo.Usuario import Usuario
from app import ventana_alerta

def login_view(page: ft.Page):
    def mostrar_dialogo():
        page.open(ventana_alerta.alerta_login())
        pass

    usuario_login = ft.TextField(label="Usuario")
    contrasena_login = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    #dlg_alerta = ft.AlertDialog(
    #    modal=True,
    #    title=ft.Text("Error inicio de sesión"),
    #    content=ft.Text("Usuario o contraseña incorrectos"),
    #    actions=[
    #        ft.TextButton("Ok", on_click=lambda e: cerrar_dialogo()),
    #    ],s
    #    actions_alignment=ft.MainAxisAlignment.END,
    #    on_dismiss=lambda e: print("Modal dialog dismissed!"),
    #)
#
    #def cerrar_dialogo():
    #    dlg_alerta.open = False
    #    page.update()
#
    def ir_a_menu(e):
        usuario = Usuario.obtener_por_nombre_usuario(usuario_login.value)
        #usuario va a recibir el usuario si existe, si no, devuelve none con eso valido con un if si existe y luego la contraseña
        if usuario and usuario.contrasena == contrasena_login.value:
            from app.dashboard_view import dashboard_view
            page.clean()
            page.add(dashboard_view(page))
        else:
            mostrar_dialogo()
            
       # print("CLICAMOS EN ENTRAR")
       # from app.dashboard_view import dashboard_view
       # page.clean()
       # page.add(dashboard_view(page))
       # print("Hemos accedido al dashboard")

    login_container = ft.Container(
        width=320,
        height=420,
        padding=20,
        border_radius=20,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            controls=[
                ft.Text("Iniciar Sesión", size=28, weight="bold"),
                usuario_login,
                contrasena_login,
                ft.ElevatedButton("Entrar", on_click=lambda e: ir_a_menu(e)),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    fondo = ft.Container(
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
