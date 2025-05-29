import flet as ft
from backend.modelo.Producto import Producto
from backend.modelo.Venta_line import VentaLine
import uuid

def venta_line_view(Page: ft.Page):
    # Lista para guardar líneas de venta
    lineas_venta = []

    # Controles
    lista_lineas_column = ft.Column(scroll=ft.ScrollMode.AUTO)
    subtotal_text = ft.Text("Subtotal: 0.00 €", size=16, weight=ft.FontWeight.BOLD)
    total_text = ft.Text("Total de la Compra: 0.00 €", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)

    # Inputs
    nref_input = ft.TextField(label="Nº Referencia", width=300)
    nombre_input = ft.TextField(label="Nombre", width=300, read_only=True)
    precio_input = ft.TextField(label="Precio", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    cantidad_input = ft.TextField(label="Cantidad", width=300, value="1", keyboard_type=ft.KeyboardType.NUMBER)
    linea_subtotal_text = ft.Text("Subtotal: 0.00 €", size=16, weight=ft.FontWeight.BOLD)

    # Actualizar subtotal de la línea
    def actualizar_linea_subtotal(e=None):
        try:
            precio = float(precio_input.value)
        except:
            precio = 0.0
        try:
            cantidad = int(cantidad_input.value)
        except:
            cantidad = 0
        subtotal = precio * cantidad
        linea_subtotal_text.value = f"Subtotal: {subtotal:.2f} €"
        Page.update()

    # Buscar producto
    def buscar_producto(e):
        ref = nref_input.value.strip()
        producto = Producto.buscar_por_referencia(ref)
        if producto:
            nombre_input.value = producto.nombre
            precio_input.value = str(producto.precio)
        else:
            nombre_input.value = ""
            precio_input.value = ""
        actualizar_linea_subtotal()

    # Calcular totales generales
    def calcular_totales():
        total = sum(linea['subtotal'] for linea in lineas_venta)
        subtotal_text.value = f"Subtotal líneas: {total:.2f} €"
        total_text.value = f"Total de la Compra: {total:.2f} €"
        Page.update()

    # Guardar línea
    def guardar_linea(e):
        try:
            producto = Producto.buscar_por_referencia(nref_input.value.strip())
            if not producto:
                raise Exception("Producto no encontrado")

            cantidad = int(cantidad_input.value)
            precio_stamp = float(precio_input.value)
            subtotal = precio_stamp * cantidad

            linea_id = str(uuid.uuid4())
            linea = VentaLine(linea_id, producto, cantidad, precio_stamp)
            if linea.guardar():
                # Guardar en la lista visual
                lineas_venta.append({
                    "producto": producto.nombre,
                    "cantidad": cantidad,
                    "precio": precio_stamp,
                    "subtotal": subtotal
                })
                lista_lineas_column.controls.append(
                    ft.Text(f"{producto.nombre} - {cantidad} x {precio_stamp:.2f} € = {subtotal:.2f} €")
                )
                calcular_totales()

                Page.dialog = ft.AlertDialog(title=ft.Text("Línea guardada correctamente"))
            else:
                Page.dialog = ft.AlertDialog(title=ft.Text("Error al guardar"))
            Page.dialog.open = True
            Page.update()

        except Exception as ex:
            Page.dialog = ft.AlertDialog(title=ft.Text(f"Error: {ex}"))
            Page.dialog.open = True
            Page.update()

    # Listeners
    nref_input.on_change = buscar_producto
    precio_input.on_change = actualizar_linea_subtotal
    cantidad_input.on_change = actualizar_linea_subtotal

    return ft.View(
        route="/venta_line",
        controls=[
            ft.Text("Gestión de Venta", size=30, weight=ft.FontWeight.BOLD),

            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Líneas de Venta:", size=18, weight=ft.FontWeight.BOLD),
                            lista_lineas_column,
                        ]),
                        expand=3,
                        padding=10,
                        border=ft.border.all(1),
                        border_radius=10
                    ),
                    ft.Container(
                        content=ft.Column([
                            subtotal_text,
                        ]),
                        expand=1,
                        padding=10,
                        border=ft.border.all(1),
                        border_radius=10
                    ),
                ],
                expand=True
            ),

            ft.Divider(),

            ft.Column(
                controls=[
                    ft.Text("Añadir Nueva Línea", size=20, weight=ft.FontWeight.BOLD),
                    nref_input,
                    ft.ElevatedButton("Buscar Ref", on_click=buscar_producto, width=300),
                    nombre_input,
                    precio_input,
                    cantidad_input,
                    linea_subtotal_text,
                    ft.ElevatedButton("Guardar Línea", on_click=guardar_linea, width=300),
                    total_text,
                    ft.ElevatedButton(
                        "Volver al Dashboard",
                        on_click=lambda e: Page.go("/dashboard"),
                        width=300,
                        bgcolor=ft.Colors.GREY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        padding=20, 
        scroll=ft.ScrollMode.AUTO,
    )
