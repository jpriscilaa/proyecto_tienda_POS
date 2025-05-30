import flet as ft

def dashboard_view(page: ft.Page):
    menu = ft.Container(
        content=ft.Column(
            controls=[
                ft.ElevatedButton("CONFIGURACION DE EMPRESA"),
                ft.ElevatedButton("PRODUCTOS"),
                ft.ElevatedButton("CLIENTES"),
                ft.ElevatedButton("TPV"),
                ft.ElevatedButton("SALIR"),
            ]
        )
    )

    return menu
