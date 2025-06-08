import flet as ft
from backend.modelo.Producto import Producto
from backend.modelo.Venta import Venta
from backend.modelo.Venta_Linea import Venta_Linea
from backend.modelo.Cliente import Cliente
from backend import Constantes
from app import ventana_alerta
from app.dashboard_view import dashboard_view
import logging
from datetime import datetime

logger=logging.getLogger(__name__)

def tpv_view(page: ft.Page):

    page.clean()
    page.window.center=True
    page.window.width=1300
    page.window.height=900
    page.update()

    carrito=[]
    total_venta=0.0
    tabla_lineas=ft.Column()
    
    #Metodos
    def volver_al_dashboard(e):
        page.clean()
        page.add(dashboard_view(page))
        page.update()

    def buscar_producto(e):
        ref=buscador_input.value.strip() #para quitar espacios y ver si hay texto realmente
        if ref:
            producto=Producto.buscar_por_referencia(ref)
            if producto:
                agregar_a_carrito(producto)
            else:
                page.open(ventana_alerta.barra_error_mensaje("Producto no encontrado"))
        buscador_input.value=None
        buscador_input.focus()
        page.update()

    def agregar_a_carrito(producto: Producto):
        for prod in carrito:
            if prod["producto"].id == producto.id:
                prod["cantidad"] += 1
                break
        else: #el else funciona en un for en caso q no exista elemetos la lista o ha acabado la de recorrer la lista
            carrito.append({"producto": producto, 
                            "cantidad": 1})
        actualizar_tabla()

    def eliminar_linea(e, prod_id):
        carrito[:]=[item for item in carrito if item["producto"].id != prod_id]
        actualizar_tabla()

    def actualizar_tabla():
        total=0.00
        filas=[]
        for p in carrito:
            prod=p["producto"]
            cant=p["cantidad"]
            subtotal=round(cant * prod.precio, 2)
            total+=round(subtotal * (1 + prod.iva.porcentaje / 100), 2)
            fila=ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(prod.n_referencia)),
                    ft.DataCell(ft.Text(prod.nombre)),
                    ft.DataCell(ft.Text(f"{prod.precio:.2f} €")),
                    ft.DataCell(ft.Text(cant)),
                    ft.DataCell(ft.Text(f"{subtotal:.2f} €")),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar producto",
                        on_click=lambda e, id=prod.id: eliminar_linea(e, id)
                        )
                    )
                ],
                selected=False
                ,data=prod
                # ,on_select_changed=lambda e: seleccionar_producto(e.control.data)
            ) 
            filas.append(fila)

        data_table=ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
            columns=[
                ft.DataColumn(ft.Text("REFERENCIA")),
                ft.DataColumn(ft.Text("NOMBRE")),
                ft.DataColumn(ft.Text("PRECIO")),
                ft.DataColumn(ft.Text("CANTIDAD")),
                ft.DataColumn(ft.Text("TOTAL")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=filas
        )

        tabla_lineas.controls.clear()
        tabla_lineas.controls.append(data_table)
        total_texto.value=f"Total: {total:.2f} €"
        total_venta=total
        cantidad_products=1
        page.update()

    def finalizar_venta(e):
        if not carrito:
            page.open(ventana_alerta.barra_error_mensaje("No hay productos en la venta"))
            return

        venta=Venta(
            cantidad_prod=len(carrito),
            total=total_venta,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            pago="TEMPORAL"
        ) 
        venta.guardar() #Crea la venta vacía
        for item in carrito:
            prod=item["producto"]
            und=item["cantidad"]
            linea=Venta_Linea(
                venta=venta,
                producto=prod,
                cantidad=und,
                iva=prod.iva.porcentaje,
                precio_unitario=prod.precio,
                total_linea=und*prod.precio
            )
            linea.guardar()
        page.open(ventana_alerta.barra_ok_mensaje("Venta registrada correctamente"))
        page.open(ventana_alerta.finalizar_venta(page)),
        page.update()
        carrito.clear()
        actualizar_tabla()

    #Componentes
    total_texto=ft.Text(value="Total: 0.00 €", size=40, weight=ft.FontWeight.BOLD)
    buscador_input=ft.TextField(
        label="Escanea o escribe referencia",
        prefix_icon=ft.Icons.SEARCH,
        on_submit=buscar_producto
    )
    btn_volver=ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO
    )
    btn_finalizar=ft.ElevatedButton(
        text="Finalizar Venta",
        icon=ft.Icons.CHECK_CIRCLE,
        on_click=finalizar_venta,
        bgcolor=Constantes.COLOR_BOTON_PRIMARIO,
        color=Constantes.COLOR_BORDE_CLARO,
        width=200,
        height=90
    )

    #Estructura
    fila_superior=ft.Row(controls=[btn_volver, ft.Text("TPV - Punto de Venta", size=24)])
    contenedor_tabla=ft.Container(
        height=400, 
        content=ft.Column([tabla_lineas], 
        scroll=ft.ScrollMode.AUTO)
        )

    layout=ft.Column([
        fila_superior,
        buscador_input,
        contenedor_tabla,
        total_texto,
        btn_finalizar
    ])

    contenedor=ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=layout,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    return contenedor