import flet as ft

def login_view(page: ft.Page):
    def ir_a_menu(e):
        print("CLICAMOS EN ENTRAR")
        from app.dashboard_view import dashboard_view
        page.clean()
        page.add(dashboard_view(page))
        print("Hemos accedido al dashboard")

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
                ft.ElevatedButton("Entrar", on_click=ir_a_menu),
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
