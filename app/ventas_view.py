from datetime import datetime
import flet as ft
from fpdf import FPDF
from app.dashboard_view import dashboard_view
from backend import Constantes
from backend.modelo.Cliente import Cliente
from backend.modelo.Venta import Venta
from backend.modelo.Usuario import Usuario
import logging
logger=logging.getLogger(__name__)

def venta_view(page: ft.Page, usuario: Usuario):
    def guardar_pdf(e):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        column_width = [40, 30, 50, 30, 30]
        header = ("FECHA", "PAGO", "CLIENTE", "CANTIDAD", "TOTAL")
        data = [header]

        ventas = Venta.obtener_todos()
        for v in ventas:
            cliente_str = f"{v.cliente.nombre} {v.cliente.apellido}" if v.cliente else "Cliente desconocido"
            data.append([
                v.fecha,
                v.pago,
                cliente_str,
                str(v.cantidad_prod),
                f"{v.total:.2f} EUR"

            ])

        for row in data:
            for item, width in zip(row, column_width):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()

        file_name = datetime.now().strftime("VENTAS_%Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)

    def volver_al_dashboard(e):
        page.clean()
        page.add(dashboard_view(page, usuario))

    tabla_ventas = ft.Column()

    def seleccionar_venta(venta):
        venta_id.value = str(venta.id)
        fecha.value = venta.fecha
        pago.value = venta.pago
        cliente_nombre.value = venta.cliente.nombre if venta.cliente else ""
        cliente_apellido.value = venta.cliente.apellido if venta.cliente else ""
        cantidad_prod.value = str(venta.cantidad_prod)
        total.value = str(venta.total)
        print("Venta seleccionada:", venta.id)
        page.update()

    def actualizar_tabla(filtro=None):
        lista = Venta.obtener_todos()
        if filtro:
            palabras = filtro.lower().split()
            lista_filtrada = []

            for v in lista:
                cliente_str = f"{v.cliente.nombre} {v.cliente.apellido}" if v.cliente else ""
                texto_busqueda = f"{v.fecha} {v.pago} {cliente_str}".lower()
                if all(palabra in texto_busqueda for palabra in palabras):
                    lista_filtrada.append(v)

            lista = lista_filtrada 

        filas = []
        for v in lista:
            cliente_str = f"{v.cliente.nombre} {v.cliente.apellido}" if v.cliente else "Cliente desconocido"
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v.fecha)),
                    ft.DataCell(ft.Text(v.pago)),
                    ft.DataCell(ft.Text(cliente_str)),
                    ft.DataCell(ft.Text(str(v.cantidad_prod))),
                    ft.DataCell(ft.Text(str(v.total))),
                ],
                selected=False,
                data=v,
                on_select_changed=lambda e: seleccionar_venta(e.control.data)
            )
            filas.append(fila)

        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Pago")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Total"))
            ],
            rows=filas
        )

        tabla_ventas.controls.clear()
        tabla_ventas.controls.append(
            ft.Container(
                height=400,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()

    # --- Componentes ---
    venta_id = ft.TextField(label="ID Venta", visible=False)
    fecha = ft.TextField(label="Fecha (YYYY-MM-DD)")
    pago = ft.Dropdown(label="Método de pago", options=[
        ft.dropdown.Option("EFECTIVO"),
        ft.dropdown.Option("TARJETA"),
        ft.dropdown.Option("TRANSFERENCIA")
    ])
    cliente_nombre = ft.TextField(label="Nombre Cliente")
    cliente_apellido = ft.TextField(label="Apellido Cliente")
    cantidad_prod = ft.TextField(label="Cantidad de productos")
    total = ft.TextField(label="Total (€)")

    buscador_ventas = ft.TextField(
        label="Buscar venta", 
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: actualizar_tabla(buscador_ventas.value)
    )

    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO,
        on_click=volver_al_dashboard
    )

    btn_guardar_venta = ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Guardar venta",
        width=80,
        height=80
    )

    btn_editar_venta = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar venta",
        width=80,
        height=80
    )

    btn_limpiar_venta = ft.IconButton(
        icon=ft.Icons.AUTO_DELETE,
        tooltip="Limpiar campos",
        width=80,
        height=80
    )

    btn_pdf = ft.ElevatedButton(
        text="Generar PDF",
        icon=ft.Icons.PICTURE_AS_PDF,
        on_click=guardar_pdf
    )

    # Layout visual
    columna_izquierda = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                venta_id,
                fecha,
                pago,
                cliente_nombre,
                cliente_apellido,
                cantidad_prod,
                total,
                ft.Row(controls=[btn_guardar_venta, btn_editar_venta, btn_limpiar_venta])
            ]
        )
    )

    columna_derecha = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                buscador_ventas,
                btn_pdf,
                tabla_ventas
            ]
        )
    )

    fila_superior = ft.Row(
        controls=[btn_volver_dashboard, ft.Text("Gestión de Ventas",size=24, weight=ft.FontWeight.BOLD)]
    )

    fila_medio = ft.Row(
        controls=[columna_izquierda, columna_derecha],
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    datos = ft.Column(
        controls=[fila_superior, fila_medio]
    )

    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    actualizar_tabla()
    return contenedor
