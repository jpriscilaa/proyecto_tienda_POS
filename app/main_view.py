import flet as ft
from app.router import route_app

def main(page: ft.Page):
    # Cambiar color de fondo de toda la ventana
    page.bgcolor=ft.Colors.WHITE

    # Cambiar fuente, tema, tamaño, etc.


    route_app(page)

if __name__ == "__main__":
    ft.app(target=main)
