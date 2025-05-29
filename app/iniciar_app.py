import flet as ft

def iniciar_app(page: ft.Page):
    page.title = "Primera configuración"
    page.bgcolor = "#000000"
    form_controls = [
        ("NOMBRE EMPRESA", ft.TextField()),
        ("NOMBRE USUARIO", ft.TextField()),
        ("CONTRASEÑA USUARIO", ft.TextField(password=True)),
        ("PAIS", ft.Dropdown(options=[
            ft.dropdown.Option("México"),
            ft.dropdown.Option("Argentina"),
            ft.dropdown.Option("España")
        ])),
        ("DIRECCION", ft.TextField()),
        ("TELEFONO", ft.TextField()),
        ("MONEDA", ft.Dropdown(options=[
            ft.dropdown.Option("€"),
            ft.dropdown.Option("$")
        ])),
    ]
    form_items = []
    for label, field in form_controls:
        form_items.append(
            ft.Row(
                controls=[
                    ft.Text(label, size=16, width=180),
                    field
                ],
                
                spacing=20
            )
        )

    content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(form_items, spacing=15),
        bgcolor="#00465e",
        padding=30,
        border_radius=20
    )

    page.add(
        ft.Column(
            [
                content
            ],
            spacing=0,
            alignment=ft.alignment.center
        )
    )

# def iniciar_app(page: ft.Page):

#     login_container = ft.Container(
#         width=320,
#         height=420,
#         padding=20,
#         border_radius=20,
#         alignment=ft.alignment.center,
#         bgcolor=ft.Colors.WHITE,
#         content=ft.Column(
#             controls=[
#                 ft.Text("Iniciar Sesión", size=28, weight="bold"),
#                 ft.TextField(label="Usuario"),
#                 ft.TextField(label="Contraseña", password=True, can_reveal_password=True),
#                 ft.ElevatedButton("Entrar", on_click=lambda e: page.go("/dashboard")),
#             ],
#             spacing=20,
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER
#         )
#     )

#     fondo = ft.Container(
#         expand=True,
#         alignment=ft.alignment.center,
#         gradient=ft.LinearGradient(
#             begin=ft.alignment.top_center,
#             end=ft.alignment.bottom_center,
#             colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_ACCENT_100, ft.Colors.BLUE_GREY_400]
#         ),
#         content=login_container
#     )

#     return ft.View(
#         route="/",
#         controls=[login_container]
#     )
