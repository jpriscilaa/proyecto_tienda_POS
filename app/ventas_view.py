from datetime import datetime
import flet as ft
from fpdf import FPDF
from app import ventana_alerta
from backend import Constantes
from backend.modelo.Venta import Venta
import logging

log = logging.getLogger(__name__)

def venta_view(page: ft.Page, usuario):
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
        page.open(ventana_alerta.barra_ok_mensaje("PDF CREADO Y GUARDADO"))



    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard = dashboard_view(page, usuario)
        page.add(dashboard)
        page.update()


    
    tabla_ventas = ft.Column()

    buscador_ventas = ft.TextField(
        label="Buscar venta",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: actualizar_tabla(buscador_ventas.value)
    )

    def eliminar_venta(e, venta_id):
        Venta.borrar_por_id(venta_id)
        actualizar_tabla(buscador_ventas.value)
        page.update()

    def actualizar_tabla(filtro=None):
        lista = Venta.obtener_todos()
        if filtro:
            palabras = filtro.lower().split()
            lista = [
                v for v in lista
                if all(
                    palabra in f"{v.fecha} {v.pago} {(v.cliente.nombre + ' ' + v.cliente.apellido) if v.cliente else ''}".lower()
                    for palabra in palabras
                )
            ]

        filas = []
        for v in lista:
            cliente_str = f"{v.cliente.nombre} {v.cliente.apellido}" if v.cliente else "Cliente desconocido"
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v.fecha)),
                    ft.DataCell(ft.Text(v.pago)),
                    ft.DataCell(ft.Text(cliente_str)),
                    ft.DataCell(ft.Text(str(v.cantidad_prod))),
                    ft.DataCell(ft.Text(f"{v.total:.2f}")),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar venta",
                        on_click=lambda e, id=v.id: eliminar_venta(e, id)
                    ))
                ],
                selected=False,
                data=v,
            )
            filas.append(fila)

        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Pago")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
            width=page.width
        )

        tabla_ventas.controls.clear()
        tabla_ventas.controls.append(
            ft.Container(
                expand=True,
                height=400,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO  # aquí va el scroll para que la tabla pueda desplazarse
                )
            )
        )
        page.update()

    btn_pdf = ft.ElevatedButton(
        text="Generar PDF",
        icon=ft.Icons.PICTURE_AS_PDF,
        on_click=guardar_pdf
    )

    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO,
        on_click=volver_al_dashboard

    )

    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                ft.Row([btn_volver_dashboard, ft.Text("Gestión de Ventas", size=24, weight=ft.FontWeight.BOLD)]),
                buscador_ventas,
                btn_pdf,
                tabla_ventas,
            ]
        ),
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    actualizar_tabla()

    return contenedor
