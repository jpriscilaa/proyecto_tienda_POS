import flet as ft  # Esto es lo correcto, no 'import flet as flet'
from backend.modelo.Producto import Producto
from backend.modelo.Iva import Iva
from backend.modelo.Categoria import Categoria
from backend import Constantes

def producto_view(page: ft.Page):  
 
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
    
    def seleccionar_producto(producto: Producto):
        prod_id_actual.value = str(producto.id)
        n_ref.value = producto.n_referencia
        nombre.value = producto.nombre
        precio.value = str(producto.precio)
        categoria_dropdown.value = producto.categoria.nombre
        iva_dropdown.value = producto.iva.iva_id
        page.update()
    
    btn_editar_prod = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar producto"
    )

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

    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard = dashboard_view(page)
        page.add(dashboard)
        page.update()


    #Cargar datos iniciales
    actualizar_tabla()

    #Campos
    n_ref = ft.TextField(label="Referencia")
    nombre = ft.TextField(label="Nombre")
    precio = ft.TextField(label="Precio")
    prod_id_actual = ft.TextField(label="ID del producto", visible=False)
    buscador_input = ft.TextField(label="Buscar producto", prefix_icon=ft.Icons.SEARCH)
    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    #Relleno lista de categoria con cada categoria que hay en bd
    categorias = Categoria.obtener_todos()
    categoria_option = []
    for c in categorias:
        option=ft.DropdownOption(
            text=c.nombre,
            key=c.categoria_id
        )
        categoria_option.append(option)
    categoria_dropdown = ft.Dropdown(label="Categoría", options=categoria_option)

    #Relleno lista de iva con cada categoria que hay en bd
    ivas = Iva.obtener_todos()
    iva_option = []
    for i in ivas:
        option=ft.DropdownOption(
            text=i.nombre,
            key=i.iva_id
        )
        iva_option.append(option)
    iva_dropdown = ft.Dropdown(label="IVA", options=iva_option)

    #Estructura de la vista
    formulario = ft.Column([
        ft.Row([btn_volver_dashboard, ft.Text("Gestión de Producto", size=20, weight="bold", color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.START),
        ft.Row([ft.Column([
                nombre,
                n_ref,
                precio,
                categoria_dropdown,
                iva_dropdown,
                ft.Row([
                    ft.ElevatedButton("Guardar"),
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

    columna_izquierda=ft.Container(alignment=ft.alignment.top_center,
        bgcolor=ft.Colors.YELLOW, 
        content= ft.Column(
        controls=[
        n_ref,
        nombre,
        precio,
        prod_id_actual
    ])
    )

    columna_derecha=ft.Container(alignment=ft.alignment.top_center,
        bgcolor=ft.Colors.RED, 
        content=ft.Column(
        controls=[
        buscador_input,
        tabla_productos
    ])
    )
    fila_superior=ft.Row(controls=[btn_volver_dashboard, ft.Text("Gestión de Producto")])
    fila_medio=ft.Row(controls=[columna_izquierda, columna_derecha], vertical_alignment=ft.CrossAxisAlignment.START)
    datos=ft.Column(controls=[fila_superior, fila_medio])
    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    # Configurar el evento de búsqueda
    buscador_input.on_change = lambda e: actualizar_tabla(buscador_input.value)

    return contenedor