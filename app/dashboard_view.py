import flet as ft

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

    menu = ft.Container(
        padding=20,
        border_radius=20,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                ft.ElevatedButton("CONFIGURACION DE EMPRESA", on_click=abrir_config_empresa),
                ft.ElevatedButton("PRODUCTOS", on_click=abrir_productos),
                ft.ElevatedButton("CLIENTES", on_click=abrir_clientes),
                ft.ElevatedButton("TPV", on_click=abrir_tpv),
                ft.ElevatedButton("USUARIOS", on_click=abri_usuario),
                ft.ElevatedButton("SALIR", on_click=salir)
            ]
        )
    )

    return menu
