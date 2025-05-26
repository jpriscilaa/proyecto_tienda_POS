import flet as ft
from backend.servicios.producto_service import crear_producto
from backend.servicios.categoria_service import listar_categorias
from backend.servicios.iva_service import listar_ivas
from backend.modelo.Categoria import Categoria
from backend.servicios.crear_tablas import inicializar_tablas

def producto_view(page: ft.Page):
    inicializar_tablas()

    # Inputs
    nombre = ft.TextField(label="Nombre")
    precio = ft.TextField(label="Precio")
    categoria_dropdown = ft.Dropdown(label="Categoría")
    iva_dropdown = ft.Dropdown(label="IVA")

    # Cargar opciones para dropdowns
    categorias = listar_categorias()
    ivas = listar_ivas()

    categoria_dropdown.options = [ft.dropdown.Option(key=c.categoria_id, text=c.nombre) for c in categorias]
    iva_dropdown.options = [ft.dropdown.Option(key=i.iva_id, text=f"{i.nombre} ({i.porcentaje}%)") for i in ivas]

    # Mensaje para feedback
    mensaje = ft.Text("", color=ft.Colors.RED)

    def agregar_producto(e):
        if nombre.value == "" or precio.value == "":
            page.snack_bar = ft.SnackBar(ft.Text("Faltan el nombre o el precio"))
            page.snack_bar.open = True
            page.update()
            return

        if categoria_dropdown.value is None or iva_dropdown.value is None:
            page.snack_bar = ft.SnackBar(ft.Text("Falta seleccionar categoría o IVA"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            precio_numero = float(precio.value)
            producto_id = "prod_" + nombre.value.lower().replace(" ", "")[:4]

            crear_producto(
                id=producto_id,
                nombre=nombre.value,
                precio=precio_numero,
                categoria_id=categoria_dropdown.value,
                iva_id=iva_dropdown.value
            )

            nombre.value = ""
            precio.value = ""
            categoria_dropdown.value = None
            iva_dropdown.value = None

            page.snack_bar = ft.SnackBar(ft.Text("Producto agregado"))
            page.snack_bar.open = True
            page.update()

        except:
            page.snack_bar = ft.SnackBar(ft.Text("Error al agregar producto"))
            page.snack_bar.open = True
            page.update()

   
    return ft.View(
        "/productos",
        controls=[
            ft.Text("Gestión de Productos", size=20, weight="bold"),
            nombre,
            precio,
            categoria_dropdown,
            iva_dropdown,
            ft.ElevatedButton("Agregar producto", on_click=agregar_producto),
            mensaje
        ]
    )
