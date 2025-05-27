import flet as ft
from backend.servicios.cliente_service import listar_clientes, guardar_cliente, obtener_cliente_por_documento
from backend.modelo.Cliente import Cliente
import uuid

def clientes_view(page: ft.Page):
    Cliente.crear_tabla() 

    # --- CONTROLES DE FORMULARIO ---
    id_cliente = str(uuid.uuid4())
    nombre_input = ft.TextField(label="Nombre", expand=True)
    documento_input = ft.TextField(label="Documento", expand=True)
    telefono_input = ft.TextField(label="Teléfono", expand=True)

    mensaje = ft.Text("", color=ft.Colors.RED)

    def limpiar_form():
        nonlocal id_cliente
        id_cliente = str(uuid.uuid4())
        nombre_input.value = ""
        documento_input.value = ""
        telefono_input.value = ""
        mensaje.value = ""
        page.update()

    def guardar():
        try:
            cliente = Cliente(
                id=id_cliente,
                nombre=nombre_input.value,
                documento=documento_input.value,
                telefono=telefono_input.value
            )
            guardar_cliente(cliente)
            cargar_clientes()
            limpiar_form()
            mensaje.value = "Cliente guardado con éxito"
        except Exception as e:
            mensaje.value = f"Error: {e}"
        page.update()

    # --- BÚSQUEDA ---
    filtro_documento = ft.TextField(label="Buscar por documento", on_change=lambda e: cargar_clientes(e.control.value))

    tabla_clientes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Teléfono")),
        ],
        rows=[]
    )

    def cargar_clientes(filtro=""):
        clientes = (
            [obtener_cliente_por_documento(filtro)]
            if filtro
            else listar_clientes()
        )

        tabla_clientes.rows.clear()
        for c in clientes:
            if c:  # Evitar None cuando no hay coincidencia
                tabla_clientes.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(c.nombre)),
                        ft.DataCell(ft.Text(c.documento)),
                        ft.DataCell(ft.Text(c.telefono)),
                    ])
                )
        page.update()

    # --- LAYOUT ---

    form_column = ft.Column(
        [
            nombre_input,
            documento_input,
            telefono_input,
            ft.Row([ft.ElevatedButton("Guardar", on_click=lambda e: guardar()),
                    ft.ElevatedButton("Limpiar", on_click=lambda e: limpiar_form())]),
            mensaje
        ],
        expand=1,
    )

    tabla_column = ft.Column(
        [
            filtro_documento,
            tabla_clientes
        ],
        expand=2
    )

    contenido = ft.Row(
        [form_column, tabla_column],
        expand=True
    )

    page.add(contenido)
    page.add(contenido)
    cargar_clientes()

    return ft.View(
        route="/clientes",
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    scroll=True,
                    controls=[
                        ft.Text("Clientes", size=30, weight=ft.FontWeight.BOLD),
                        contenido
                    ]
                )
            )
        ]
    )