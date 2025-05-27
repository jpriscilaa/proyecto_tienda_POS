import flet as ft
import uuid
from backend.servicios.producto_service import crear_producto, listar_productos, actualizar_producto
from backend.servicios.categoria_service import listar_categorias
from backend.servicios.iva_service import listar_ivas
from backend.servicios.crear_tablas import inicializar_tablas

def producto_view(page: ft.Page):
    inicializar_tablas()

    # Campos de entrada
    n_ref = ft.TextField(label="Referencia")
    nombre = ft.TextField(label="Nombre")
    precio = ft.TextField(label="Precio")
    categoria_dropdown = ft.Dropdown(label="Categoría")
    iva_dropdown = ft.Dropdown(label="IVA")
    filtro = ft.TextField(label="Buscar producto")

    producto_seleccionado = {"id": None}

    categorias = listar_categorias()
    ivas = listar_ivas()
    productos = listar_productos()

    categoria_dropdown.options = [ft.dropdown.Option(key=c.categoria_id, text=c.nombre) for c in categorias]
    iva_dropdown.options = [ft.dropdown.Option(key=i.iva_id, text=f"{i.nombre} ({i.porcentaje}%)") for i in ivas]

    # Tabla de productos
    data_table = ft.DataTable(
        expand=True,
        border=ft.border.all(1, "gray"),
        border_radius=10,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Referencia")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("IVA")),
        ],
        rows=[]
    )

    def mostrar_productos(lista):
        data_table.rows.clear()
        for p in lista:
            data_table.rows.append(
                ft.DataRow(
                    on_select_changed=get_index,
                    cells=[
                        ft.DataCell(ft.Text(p[0])),
                        ft.DataCell(ft.Text(p[1])),
                        ft.DataCell(ft.Text(str(p[2]))),
                        ft.DataCell(ft.Text(p[3])),
                        ft.DataCell(ft.Text(p[4])),
                        ft.DataCell(ft.Text(p[5])),
                    ]
                )
            )
        page.update()

    def get_index(e):
        if e.control.selected:
            producto_seleccionado["id"] = e.control.cells[0].content.value
            n_ref.value = e.control.cells[1].content.value
            nombre.value = e.control.cells[2].content.value
            precio.value = e.control.cells[3].content.value
            categoria_dropdown.value = e.control.cells[4].content.value
            iva_dropdown.value = e.control.cells[5].content.value
        else:
            producto_seleccionado["id"] = None
        page.update()

    def buscar(e):
        texto = filtro.value.lower()
        if texto == "":
            mostrar_productos(productos)
        else:
            filtrados = [p for p in productos if texto in p[1].lower()]
            mostrar_productos(filtrados)

    def agregar_producto_click(e):
        print("Agregando producto...")
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
        print("Validación de campos completada")
        print("entra en crear producto")
        try:
            crear_producto(
            print("Creando producto..."),
            id=str(uuid.uuid4()), # Esto genera un ID único cada vez
            n_referencia=n_ref.value,
            nombre=nombre.value,
            precio=float(precio.value),
            categoria_id=categoria_dropdown.value,
            iva_id=iva_dropdown.value
            )
            print
            limpiar_formulario()
            recargar()
            page.snack_bar = ft.SnackBar(ft.Text("Producto agregado"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al agregar producto: {ex}"))
            page.snack_bar.open = True
            page.update()

    def actualizar_producto_click(e):
        if producto_seleccionado["id"] is None:
            page.snack_bar = ft.SnackBar(ft.Text("Selecciona un producto para editar"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            actualizar_producto(
                id=producto_seleccionado["id"],
                n_referencia=n_ref.value,
                nombre=nombre.value,
                precio=float(precio.value),
                categoria_id=categoria_dropdown.value,
                iva_id=iva_dropdown.value
            )
            limpiar_formulario()
            recargar()
            page.snack_bar = ft.SnackBar(ft.Text("Producto actualizado"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar producto: {ex}"))
            page.snack_bar.open = True
            page.update()

    def limpiar_formulario():
        producto_seleccionado["id"] = None
        n_ref.value = ""
        nombre.value = ""
        precio.value = ""
        categoria_dropdown.value = None
        iva_dropdown.value = None

    def recargar():
        nonlocal productos
        productos = listar_productos()
        mostrar_productos(productos)

    filtro.on_change = buscar
    mostrar_productos(productos)

    # Estructura visual
    return ft.View(
        route="/productos",
        controls=[
            ft.Text("Gestión de Productos", size=28),
            filtro,
            ft.Row([
                ft.Column([
                    n_ref,
                    nombre,
                    precio,
                    categoria_dropdown,
                    iva_dropdown,
                    ft.Row([
                        ft.ElevatedButton("Agregar", on_click=agregar_producto_click),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_producto_click),
                    ]),
                ], expand=1),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Lista de Productos", size=20),
                        data_table
                    ]),
                    padding=10,
                    expand=2
                )
            ])
        ]
    )
