import flet as ft
from backend.servicios.producto_service import crear_producto, listar_productos, actualizar_producto
from backend.servicios.categoria_service import listar_categorias
from backend.servicios.iva_service import listar_ivas
from backend.servicios.crear_tablas import inicializar_tablas
import uuid

def producto_view(page: ft.Page):
    # Inicializar tablas si no existen
    inicializar_tablas()    
    # Campos
    n_ref = ft.TextField(label="Referencia")
    nombre = ft.TextField(label="Nombre")
    precio = ft.TextField(label="Precio")
    categoria_dropdown = ft.Dropdown(label="Categoría")
    iva_dropdown = ft.Dropdown(label="IVA")
    filtro = ft.TextField(label="Buscar producto")

    producto_seleccionado = {"id": None}
    categorias = listar_categorias()
    ivas = listar_ivas()

    categoria_dropdown.options = [ft.dropdown.Option(c.categoria_id, c.nombre) for c in categorias]
    iva_dropdown.options = [ft.dropdown.Option(i.iva_id, f"{i.nombre} ({i.porcentaje}%)") for i in ivas]


    # Tabla de productos
    tabla = ft.DataTable(
        expand=True,
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

    def seleccionar_producto(e, prod):
        if e.control.selected:
            producto_seleccionado["id"] = prod[0]
            n_ref.value, nombre.value, precio.value = prod[1], prod[2], str(prod[3])
            categoria_dropdown.value = next((c.categoria_id for c in categorias if c.nombre == prod[4]), None)
            iva_dropdown.value = next((i.iva_id for i in ivas if f"{i.nombre} ({i.porcentaje}%)" == prod[5]), None)
        else:
            limpiar_formulario()
        page.update()

    def mostrar_productos(lista):
        for p in lista:
            fila = ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(col))) for col in p],
                on_select_changed=lambda e, prod=p: seleccionar_producto(e, prod)
            )
            tabla.rows.append(fila)
        page.update()

    def buscar(e):
        texto = filtro.value.lower()
        productos = listar_productos()
        if texto:
            productos = [p for p in productos if texto in p[1].lower()]
        mostrar_productos(productos)

    def limpiar_formulario():
        producto_seleccionado["id"] = None
        n_ref.value, nombre.value, precio.value = "", "", ""
        categoria_dropdown.value, iva_dropdown.value = None, None
    
    def seleccionar_producto(e, prod):
        if e.control.selected:
            producto_seleccionado["id"] = prod[0]
            n_ref.value, nombre.value, precio.value = prod[1], prod[2], str(prod[3])
            categoria_dropdown.value = next((c.categoria_id for c in categorias if c.nombre == prod[4]), None)
            iva_dropdown.value = next((i.iva_id for i in ivas if f"{i.nombre} ({i.porcentaje}%)" == prod[5]), None)
        else:
            limpiar_formulario()
        page.update()

    def buscar(e):
        texto = filtro.value.lower()
        productos = listar_productos()
        if texto:
            productos = [p for p in productos if texto in p[1].lower()]
        mostrar_productos(productos)

    def recargar():
        mostrar_productos(listar_productos())

    def mostrar_mensaje(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto), open=True)
        page.update()

    def agregar_producto(e):
        if not nombre.value or not precio.value or not categoria_dropdown.value or not iva_dropdown.value:
            return mostrar_mensaje("Todos los campos son obligatorios")
        try:
            crear_producto(
                id=str(uuid.uuid4()),
                n_referencia=n_ref.value,
                nombre=nombre.value,
                precio=float(precio.value),
                categoria_id=categoria_dropdown.value,
                iva_id=iva_dropdown.value
            )
            limpiar_formulario()
            recargar()
            mostrar_mensaje("Producto agregado correctamente")
        except Exception as ex:
            mostrar_mensaje(f"Error: {ex}")

    def actualizar(e):
        if not producto_seleccionado["id"]:
            return mostrar_mensaje("Selecciona un producto")
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
            mostrar_mensaje("Producto actualizado")
        except Exception as ex:
            mostrar_mensaje(f"Error: {ex}")

    filtro.on_change = buscar
    recargar()

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
                        ft.ElevatedButton("Agregar", on_click=agregar_producto),
                        ft.ElevatedButton("Actualizar", on_click=actualizar),
                    ]),
                ], expand=1),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Lista de Productos", size=20),
                        tabla
                    ]),
                    padding=10,
                    expand=2
                )
            ])
        ]
    )
