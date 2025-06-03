import flet as ft

def main(page: ft.Page):
    page.title = "Gestión de Productos"
    page.window_width = 1000
    page.window_height = 600
    page.padding = 20
    page.scroll = "auto"

    # Botón ATRÁS
    boton_atras = ft.ElevatedButton(
        text="BOTON ATRÁS",
        bgcolor=ft.Colors.PINK_200,
        width=150
    )

    # Título de la ventana
    titulo_ventana = ft.Text("NOMBRE DE LA VENTANA", size=24, weight="bold")

    # --- FILA SUPERIOR: botón + título ---
    fila_superior = ft.Row(
        controls=[
            boton_atras,
            ft.Container(width=20),  # Espaciado
            titulo_ventana
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Campos verticales a la izquierda
    campos_textfield = [
        ft.TextField(label=f"TEXTFIELD {i+1}", width=150)
        for i in range(6)
    ]

    columna_izquierda = ft.Column(
        controls=campos_textfield
    )

    # Buscador
    buscador = ft.TextField(label="TEXTFIELD BUSCADOR", width=400)

    # Tabla de productos (ejemplo)
    tabla_productos = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Producto")),
            ft.DataColumn(label=ft.Text("Precio")),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("Ejemplo 1")), ft.DataCell(ft.Text("10.00"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Ejemplo 2")), ft.DataCell(ft.Text("20.00"))]),
        ],
    )

    columna_derecha = ft.Column(
        controls=[
            buscador,
            tabla_productos,
            # ft.Container(
            #     content=tabla_productos,
            #     expand=True,
            #     padding=10,
            #     border_radius=10,
            #     bgcolor=ft.Colors.BLUE_50,
            # )
        ]
    )

    # Fila principal bajo la fila superior
    fila_principal = ft.Row(
        controls=[
            columna_izquierda,
            # ft.VerticalDivider(width=20),
            columna_derecha
        ],
        expand=True
    )

    # Layout general
    layout = ft.Column(
        controls=[
            fila_superior,
            # ft.Divider(height=10),
            fila_principal
        ],
        expand=True
    )
    container=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Texto 1"),
                ft.Text("Texto 2"),
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        bgcolor=ft.Colors.BLACK,
        padding=10,
        expand=True
    )
    container1=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Texto 1"),
                ft.Text("Texto 2"),
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        bgcolor=ft.Colors.BLACK,
        padding=10,
        expand=True
    )    
    columna=ft.Row(controls=[
        container, container1

    ])


    page.add(columna)

ft.app(target=main)