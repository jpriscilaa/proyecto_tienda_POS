import flet as ft  # Esto es lo correcto, no 'import flet as flet'
from backend.modelo.Producto import Producto
from backend.modelo.Iva import Iva
from backend.modelo.Categoria import Categoria
import uuid

def producto_view(page: ft.Page):  
 
 '''   # Campos
    n_ref = ft.TextField(label="Referencia")
    nombre = ft.TextField(label="Nombre")
    precio = ft.TextField(label="Precio")
    categoria_dropdown = ft.Dropdown(label="Categoría")
    iva_dropdown = ft.Dropdown(label="IVA")
    prod_id_actual = ft.TextField(label="ID del producto", visible=False)
    buscador_input = ft.TextField(label="Buscar producto", prefix_icon=ft.Icons.SEARCH)

    categorias = Categoria.obtener_todos()
    ivas = Iva.obtener_todos()

    categoria_dropdown.options = [ft.dropdown.Option(c.nombre) for c in categorias]
    iva_dropdown.options = [ft.dropdown.Option(i.iva_id, f"{i.nombre} ({i.porcentaje}%)") for i in ivas]
    tabla_productos = ft.Column()

    def limpiar_campos():
        prod_id_actual.value = ""
        n_ref.value = ""
        nombre.value = ""
        precio.value = ""
        categoria_dropdown.value = None
        iva_dropdown.value = None
        page.update()

    def habilitar_campos(e):
        n_ref.disabled = False
        nombre.disabled = False
        precio.disabled = False
        categoria_dropdown.disabled = False
        iva_dropdown.disabled = False
        page.update()
    
    btn_editar_prod = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar producto",
        on_click=habilitar_campos
    )

    def seleccionar_producto(producto: Producto):
        prod_id_actual.value = str(producto.id)
        n_ref.value = producto.n_referencia
        nombre.value = producto.nombre
        precio.value = str(producto.precio)
        categoria_dropdown.value = producto.categoria.nombre
        iva_dropdown.value = producto.iva.iva_id
        page.update()
    
    def actualizar_tabla(filtro=None):
        lista = Producto.obtener_todos()
        if filtro:
            lista = [p for p in lista if filtro.lower() in p.nombre.lower()]

        def eliminar_producto(e, producto_id):
            Producto.borrar_por_id(producto_id)
            actualizar_tabla(buscador_input.value)
            page.update()

        filas = []

        for p in lista:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.n_referencia)),
                    ft.DataCell(ft.Text(p.nombre)),
                    ft.DataCell(ft.Text(f"{p.precio} €")),
                    ft.DataCell(ft.Text(p.categoria.nombre)),
                    ft.DataCell(ft.Text(f"{p.iva.porcentaje}%")),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar producto",
                        on_click=lambda e, id=p.id: eliminar_producto(e, id)
                    ))
                ],
                on_select_changed=lambda e, p=p: seleccionar_producto(p)
            )
            filas.append(fila)
        
        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: ft.Colors.BLUE_50},
            columns=[
                ft.DataColumn(ft.Text("Referencia")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("IVA")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=filas
        )

        tabla_productos.controls.clear()
        tabla_productos.controls.append(
            ft.Container(
                height=400,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()

    def guardar_producto(e):
        nombre_producto = nombre.value.strip()
        if not nombre_producto:
            return

        categoria = next((c for c in categorias if c.nombre == categoria_dropdown.value), None)
        iva = next((i for i in ivas if i.iva_id == iva_dropdown.value), None)

        if not categoria or not iva:
            return

        if prod_id_actual.value:
            # EDITAR producto existente
            producto_existente = Producto.buscar_por_id(prod_id_actual.value)
            if producto_existente:
                producto_existente.n_referencia = n_ref.value.strip()
                producto_existente.nombre = nombre_producto
                producto_existente.precio = float(precio.value.strip())
                producto_existente.categoria = categoria
                producto_existente.iva = iva
                producto_existente.guardar()
        else:
            # CREAR nuevo producto
            nuevo_producto = Producto(
                categoria=categoria,
                iva=iva,
                n_referencia=n_ref.value.strip(),
                nombre=nombre_producto,
                precio=float(precio.value.strip())
            )
            nuevo_producto.guardar()

        limpiar_campos()
        actualizar_tabla()

    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard = dashboard_view(page)
        page.add(dashboard)
        page.update()

    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    # Cargar datos iniciales
    actualizar_tabla()

    # Estructura de la vista
    formulario = ft.Column([
        ft.Row([btn_volver_dashboard], alignment=ft.MainAxisAlignment.START),
        ft.Text("Gestión de Producto", size=20, weight="bold", color=ft.Colors.WHITE),
        ft.Row([
            ft.Column([
                nombre,
                n_ref,
                precio,
                categoria_dropdown,
                iva_dropdown,
                ft.Row([
                    ft.ElevatedButton("Guardar", on_click=guardar_producto),
                    ft.ElevatedButton("Limpiar", on_click=lambda e: limpiar_campos())
                ])
            ], spacing=10, width=300),
            ft.Column([
                buscador_input,
                ft.Row([btn_editar_prod], alignment=ft.MainAxisAlignment.END),
                tabla_productos
            ], width=600, scroll=ft.ScrollMode.AUTO)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ])

    # Configurar el evento de búsqueda
    buscador_input.on_change = lambda e: actualizar_tabla(buscador_input.value)

    return formulario'''