import flet as ft

def login_view(page: ft.Page):

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
                ft.TextField(label="Usuario"),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True),
                ft.ElevatedButton("Entrar", on_click=lambda e: page.go("/dashboard")),
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

    return ft.View(
        route="/",
        controls=[fondo]
    )
