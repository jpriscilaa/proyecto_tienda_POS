import flet as ft

def iniciar_app(page: ft.Page):
    page.title = "Primera configuración"
    page.bgcolor = "#000000"
    form_controls = [
        ("NOMBRE EMPRESA", ft.TextField(label="Nombre")),
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

    
    return ft.Column([
                content
            ],
            spacing=0,
            alignment=ft.alignment.center
    )