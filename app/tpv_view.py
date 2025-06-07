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
    page.window.width=1300
    page.window.height=900
    page.window.center=True

    carrito=[]
    total_venta=0.0
    tabla_lineas=ft.Column()
    total_texto=ft.Text(value="Total: 0.00 €", size=20, weight=ft.FontWeight.BOLD)
    
    #Metodos
    def volver_al_dashboard(e):
        page.clean()
        page.add(dashboard_view(page))
        page.update()

    def buscar_producto(e):
        ref=buscador_input.value.strip()
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
        global carrito
        carrito=[item for item in carrito if item["producto"].id != prod_id]
        actualizar_tabla()

    def actualizar_tabla():
        filas=[]
        total=0.0
        for item in carrito:
            prod=item["producto"]
            cant=item["cantidad"]
            subtotal=cant * prod.precio
            total += subtotal * (1 + prod.iva.porcentaje / 100)

            fila=ft.Row([
                ft.Text(f"{prod.nombre} x{cant}"),
                ft.Text(f"{subtotal:.2f} €"),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    on_click=lambda e, id=prod.id: eliminar_linea(e, id)
                )
            ])
            filas.append(fila)

        tabla_lineas.controls.clear()
        tabla_lineas.controls.extend(filas)
        total_texto.value=f"Total: {total:.2f} €"
        total_venta=total
        cantidad_products=1
        page.update()

    def finalizar_venta(e):
        if not carrito:
            page.open(ventana_alerta.barra_error_mensaje("No hay productos en la venta"))
            return
        cliente_anonimo=Cliente.buscar_por_id("1")

        venta=Venta(
            cliente=cliente_anonimo,
            cantidad_productos=1,
            total=total_venta
        ) 
        venta.guardar() #Crea la venta vacía
        for item in carrito:
            producto=item["producto"]
            cantidad=item["cantidad"]
            linea=Venta_Linea(
                venta_id=venta.id,
                producto=producto,
                cantidad=cantidad
            )
            linea.guardar()
        page.open(ventana_alerta.barra_ok_mensaje("Venta registrada correctamente"))
        carrito.clear()
        actualizar_tabla()

    #Componentes
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
        bgcolor="green",
        color="white"
    )

    #Estructura
    fila_superior=ft.Row(controls=[btn_volver, ft.Text("TPV - Punto de Venta", size=24)])
    contenedor_tabla=ft.Container(height=400, content=ft.Column([tabla_lineas], scroll=ft.ScrollMode.AUTO))

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