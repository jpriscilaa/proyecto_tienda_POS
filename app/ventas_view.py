from datetime import datetime
import flet as ft
from backend import Constantes
from backend.modelo.Venta import Venta
import logging

log = logging.getLogger(__name__)

def venta_view(page: ft.Page, usuario):
    tabla_ventas = ft.Column()

    buscador_ventas = ft.TextField(
        label="Buscar venta",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: actualizar_tabla(buscador_ventas.value)
    )

    def eliminar_venta(e, venta_id):
        Venta.borrar_por_id(venta_id)
        # Aquí puedes poner un mensaje o snackbar si quieres:
        # page.snack_bar = ft.SnackBar(ft.Text("Venta eliminada"))
        # page.snack_bar.open = True
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



    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO,
        on_click=lambda e: page.go_back()
    )

    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                ft.Row([btn_volver_dashboard, ft.Text("Gestión de Ventas", size=24, weight=ft.FontWeight.BOLD)]),
                buscador_ventas,
                tabla_ventas,
            ]
        ),
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    actualizar_tabla()

    return contenedor
