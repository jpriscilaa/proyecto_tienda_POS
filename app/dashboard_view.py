import flet as ft
from backend.modelo.Usuario import Usuario
from backend import Constantes
import logging
logger=logging.getLogger(__name__)

def dashboard_view(page: ft.Page, usuario: Usuario):
    def abrir_config_empresa(e):
        from app.config_empresa_view import config_empresa_view
        page.clean()
        page.add(config_empresa_view(page, usuario))

    def abrir_productos(e):
        from app.producto_view import producto_view
        page.clean()
        page.add(producto_view(page, usuario))

    def abrir_clientes(e):
        from app.clientes_view import clientes_view
        page.clean()
        page.add(clientes_view(page, usuario))

    def abrir_tpv(e):
        from app.tpv_view import tpv_view
        page.clean()
        page.add(tpv_view(page, usuario))

    def abrir_usuario(e):
        from app.usuario_view import usuario_view
        page.clean()
        page.add(usuario_view(page, usuario))

    def abrir_ventas(e):
        from app.ventas_view import venta_view
        page.clean()
        page.add(venta_view(page, usuario))

    def salir(e):
        from app.login_view import login_view
        page.clean()
        page.add(login_view(page))

    def crear_boton(texto, icono, on_click, color_bg=None, color_text=None):
        return ft.Container(
            content=ft.ElevatedButton(
                text=texto,
                icon=icono,
                on_click=on_click,
                expand=True
            ),
            height=80,
            padding=5
        )

    #aquo ponemos directamente los botones con ifs
    controles_botones = []

    if usuario.rol.upper() == "ADMINISTRADOR":
        controles_botones.append(ft.Container(col=6, content=crear_boton("CONFIGURACIÓN", ft.Icons.BUSINESS, abrir_config_empresa)))
        controles_botones.append(ft.Container(col=6, content=crear_boton("PRODUCTOS", ft.Icons.SHOPPING_CART, abrir_productos)))
        controles_botones.append(ft.Container(col=6, content=crear_boton("USUARIOS", ft.Icons.PERSON, abrir_usuario)))

    #estos botones son comunes a todos
    controles_botones.append(ft.Container(col=6, content=crear_boton("CLIENTES", ft.Icons.PEOPLE, abrir_clientes)))
    controles_botones.append(ft.Container(col=6, content=crear_boton("TPV", ft.Icons.POINT_OF_SALE, abrir_tpv)))
    controles_botones.append(ft.Container(col=6, content=crear_boton("VENTAS", ft.Icons.LIST, abrir_ventas)))
    controles_botones.append(ft.Container(col=6, content=crear_boton("SALIR", ft.Icons.EXIT_TO_APP, salir, color_bg=ft.Colors.RED, color_text=ft.Colors.WHITE)))

    grid_botones = ft.ResponsiveRow(columns=12, controls=controles_botones)

    tarjeta_menu = ft.Container(
        padding=30,
        border_radius=20,
        width=700,
        bgcolor=Constantes.COLOR_BORDE_CLARO,
        content=ft.Column(
            controls=[
                ft.Text("Panel Principal", size=30, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                grid_botones
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    fondo = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_700]
        ),
        content=ft.Row(
            controls=[ft.Column(controls=[tarjeta_menu], alignment=ft.MainAxisAlignment.CENTER)],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    return fondo
