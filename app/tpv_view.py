import flet as ft
from backend.modelo.Producto import Producto
from backend.modelo.Venta_line import VentaLine
import uuid

def venta_line_view(Page: ft.Page):
    # Inputs
    nref_input = ft.TextField(label="Nº Referencia", width=300)
    nombre_input = ft.TextField(label="Nombre", width=300)
    precio_input = ft.TextField(label="Precio", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    cantidad_input = ft.TextField(label="Cantidad", width=300, value="1", keyboard_type=ft.KeyboardType.NUMBER)
    subtotal_text = ft.Text("Subtotal: 0.00 €", size=18, weight=ft.FontWeight.BOLD)

    # Función para actualizar subtotal
    def actualizar_subtotal(e=None):
        try:
            precio = float(precio_input.value)
        except:
            precio = 0.0
        try:
            cantidad = int(cantidad_input.value)
        except:
            cantidad = 0
        subtotal = precio * cantidad
        subtotal_text.value = f"Subtotal: {subtotal:.2f} €"
        Page.update()

    # Cuando se introduce el número de referencia
    def buscar_producto(e):
        ref = nref_input.value.strip()
        producto = Producto.buscar_por_referencia(ref)
        if producto:
            nombre_input.value = producto.nombre
            precio_input.value = str(producto.precio)
        else:
            nombre_input.value = ""
            precio_input.value = ""
        actualizar_subtotal()

    # Guardar línea de venta
    def guardar_linea(e):
        try:
            producto = Producto.buscar_por_referencia(nref_input.value.strip())
            if not producto:
                raise Exception("Producto no encontrado")

            cantidad = int(cantidad_input.value)
            precio_stamp = float(precio_input.value)
            linea_id = str(uuid.uuid4())
            linea = VentaLine(linea_id, producto, cantidad, precio_stamp)
            if linea.guardar():
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
    precio_input.on_change = actualizar_subtotal
    cantidad_input.on_change = actualizar_subtotal

    return ft.View(
        route="/venta_line",
        controls=[
            ft.Text("Añadir Línea de Venta", size=30, weight=ft.FontWeight.BOLD),
            nref_input,
            ft.ElevatedButton("Buscar Ref", on_click=buscar_producto, width=300),

            nombre_input,
            precio_input,
            cantidad_input,
            subtotal_text,
            ft.ElevatedButton("Guardar Línea", on_click=guardar_linea, width=300),
            ft.ElevatedButton(
                "Volver al Dashboard",
                on_click=lambda e: Page.go("/dashboard"),
                width=300,
                bgcolor=ft.Colors.GREY,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
