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
        from app.tpv_view import tpv_view
        page.clean()
        page.add(tpv_view(page))

    def abrir_usuario(e):
        from app.usuario_view import usuario_view
        page.clean()
        page.add(usuario_view(page))
    
    def abrir_ventas(e):
        from app.ventas_view import venta_view
        page.clean()
        page.add(venta_view(page))

    def salir(e):
        from app.login_view import login_view
        page.clean()
        page.add(login_view(page))


    # Botón estilizado reutilizable
    def crear_boton(texto, icono, on_click, color_bg=None, color_text=None):
        return ft.Container(
            content=ft.ElevatedButton(
                text=texto,
                icon=icono,
                on_click=on_click,
                style=ft.ButtonStyle(
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=12),
                    bgcolor=color_bg,
                    color=color_text,
                    elevation=4
                ),
                expand=True
            ),
            height=80,
            padding=5
        )

    # Lista de botones en diseño grid (2 columnas)
    grid_botones=ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(col=6, content=crear_boton("CONFIGURACIÓN", ft.Icons.BUSINESS, abrir_config_empresa)),
            ft.Container(col=6, content=crear_boton("PRODUCTOS", ft.Icons.SHOPPING_CART, abrir_productos)),
            ft.Container(col=6, content=crear_boton("CLIENTES", ft.Icons.PEOPLE, abrir_clientes)),
            ft.Container(col=6, content=crear_boton("TPV", ft.Icons.POINT_OF_SALE, abrir_tpv)),
            ft.Container(col=6, content=crear_boton("USUARIOS", ft.Icons.PERSON, abrir_usuario)),
            ft.Container(col=6, content=crear_boton("VENTAS", ft.Icons.LIST, abrir_ventas)),

            ft.Container(col=6, content=crear_boton("SALIR", ft.Icons.EXIT_TO_APP, salir, color_bg=ft.Colors.RED, color_text=ft.Colors.WHITE)),
        ]
    )

    tarjeta_menu=ft.Container(
        padding=30,
        border_radius=20,
        width=700,
        bgcolor=getattr(Constantes, "COLOR_BORDE_CLARO", ft.Colors.WHITE),
        content=ft.Column(
            controls=[
                ft.Text("Panel Principal", size=30, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                grid_botones
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(2, 6)
        )
    )

    fondo=ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_700]
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
