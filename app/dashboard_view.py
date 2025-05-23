import flet as ft

def dashboard_view(page: ft.Page):
    return ft.View(
        route="/dashboard",
        controls=[
            ft.Column(
                [
                    ft.Text("Bienvenido al Dashboard", size=30),
                    ft.ElevatedButton(
                        "Configuración de la Empresa",
                        on_click=lambda e: page.go("/config_empr"),
                        width=300,
                        height=60,
                    ),
                    ft.ElevatedButton(
                        "Gestión de Productos",
                        on_click=lambda e: page.go("/productos"),
                        width=300,
                        height=60,
                    ),
                    ft.ElevatedButton(
                        "Cerrar sesión",
                        on_click=lambda e: page.go("/"),
                        width=300,
                        height=60,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
