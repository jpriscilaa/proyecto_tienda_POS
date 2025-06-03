from app.producto_view import producto_view
import flet as ft

def main(page: ft.Page):   
    page.clean()

    page.add(producto_view(page))

if __name__ == "__main__":
    ft.app(target=main)