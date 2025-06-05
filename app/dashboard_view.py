import flet as ft
from backend import Constantes

def dashboard_view(page: ft.Page):
    def abrir_config_empresa(e):
        from app.config_empresa_view import config_empresa_view
        page.clean()
        page.add(config_empresa_view(page))

    def abrir_productos(e):
        from app.producto_view import producto_view
        page.clean()
        page.add(producto_view(page))

    def abrir_clientes(e):
        from app.clientes_view import clientes_view
        page.clean()
        page.add(clientes_view(page))

    def abrir_tpv(e):
        from app.tpv_view import venta_line_view
        page.clean()
        page.add(venta_line_view(page))

    def abri_usuario(e):
        from app.usuario_view import usuario_view
        page.clean()
        page.add(usuario_view(page))

    def salir(e):
        from app.login_view import login_view
        page.clean()
        page.add(login_view(page))

    botones = [
        ft.ElevatedButton("CONFIGURACIÓN DE EMPRESA", on_click=abrir_config_empresa, icon=ft.Icons.BUSINESS, width=250),
        ft.ElevatedButton("PRODUCTOS", on_click=abrir_productos, icon=ft.Icons.SHOPPING_CART, width=250),
        ft.ElevatedButton("CLIENTES", on_click=abrir_clientes, icon=ft.Icons.PEOPLE, width=250),
        ft.ElevatedButton("TPV", on_click=abrir_tpv, icon=ft.Icons.POINT_OF_SALE, width=250),
        ft.ElevatedButton("USUARIOS", on_click=abri_usuario, icon=ft.Icons.PERSON, width=250),
        ft.ElevatedButton("SALIR", on_click=salir, icon=ft.Icons.EXIT_TO_APP, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, width=250),
    ]

    tarjeta_menu = ft.Container(
        padding=30,
        border_radius=20,
        bgcolor=Constantes.COLOR_BORDE_CLARO if hasattr(Constantes, "COLOR_BORDE_CLARO") else ft.Colors.WHITE,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard", size=26, weight="bold", text_align=ft.TextAlign.CENTER),
                *botones
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(2, 4)
        )
    )

    fondo = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_ACCENT_100, ft.Colors.BLUE_GREY_400]
        ),
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[tarjeta_menu],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

    return fondo
