import flet as ft  # Esto es lo correcto, no 'import flet as flet'
from backend.modelo.Producto import Producto
from backend.modelo.Iva import Iva
from backend.modelo.Categoria import Categoria
from backend import Constantes

def producto_view(page: ft.Page):
    page.clean()
    page.window.width=1000
    page.window.center=True
    #inicializamos un colum para que sea accesible al resto de componentes y metodos
    tabla_productos = ft.Column()

    def limpiar_campos():
        prod_id_actual.value = ""
        n_ref.value = ""
        nombre.value = ""
        precio.value = ""
        categoria_dropdown.value = None
        iva_dropdown.value = None
        page.update()

    def deshabilitar_campos(e, habilitar: bool):
        n_ref.disabled = habilitar
        nombre.disabled = habilitar
        precio.disabled = habilitar
        categoria_dropdown.disabled = habilitar
        iva_dropdown.disabled = habilitar
        page.update()
    
    def seleccionar_producto(producto: Producto):
        prod_id_actual.value = str(producto.id)
        n_ref.value = producto.n_referencia
        nombre.value = producto.nombre
        precio.value = str(producto.precio)
        categoria_dropdown.value = producto.categoria.nombre
        iva_dropdown.value = producto.iva.iva_id
        page.update()
    
    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard = dashboard_view(page)
        page.add(dashboard)
        page.update()
    
    def validar_nombre(e):
        if not nombre.value.strip():
            nombre.border_color = ft.Colors.RED
            nombre.error_text = "Este campo es obligatorio"
        else:
            nombre.border_color = ft.Colors.GREY
            nombre.error_text = None
        nombre.update()

    def actualizar_tabla(filtro=None):
        lista = Producto.obtener_todos()
        if filtro:
            lista = [p for p in lista if filtro.lower() in p.nombre.lower()]

        def eliminar_producto(e, producto_id):
            Producto.borrar_por_id(producto_id)
            actualizar_tabla(buscador_input.value)
            page.update()

        #Creamos la cabecera de la tabla
        cabecera=[
                ft.DataColumn(ft.Text("Referencia")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("IVA")),
                ft.DataColumn(ft.Text("Acciones"))
        ]
        #creamos las filas de la tabla
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

        #Creamos DataTable
        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
            columns=cabecera,
            rows=filas
        )

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

    #Cargar datos iniciales
    actualizar_tabla()

    #Campos
    n_ref = ft.TextField(label="Referencia")
    nombre = ft.TextField(label="Nombre", on_blur=validar_nombre)
    precio = ft.TextField(label="Precio")
    prod_id_actual = ft.TextField(label="ID del producto", visible=False)
    buscador_input = ft.TextField(label="Buscar producto", prefix_icon=ft.Icons.SEARCH)
    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO
    )
    btn_editar_prod = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar producto",
        width=80,
        height=80
    )
    btn_guardar_prod = ft.IconButton(
        icon=ft.Icons.ADD,
        tooltip="Editar producto",
        width=80,
        height=80
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
    categoria_dropdown = ft.Dropdown(label="Categoría", options=categoria_option, width=300)

    #Relleno lista de iva con cada categoria que hay en bd
    ivas = Iva.obtener_todos()
    iva_option = []
    for i in ivas:
        option=ft.DropdownOption(
            text=i.nombre,
            key=i.iva_id
        )
        iva_option.append(option)
    iva_dropdown = ft.Dropdown(label="IVA", options=iva_option, width=300)

    #Estructura de la vista
    columna_izquierda=ft.Container(alignment=ft.alignment.top_center, 
        content= ft.Column(
        controls=[
        n_ref,
        nombre,
        precio,
        prod_id_actual,
        categoria_dropdown,
        iva_dropdown,
        ft.Row(controls=[btn_editar_prod, btn_guardar_prod])
    ])
    )

    columna_derecha=ft.Container(alignment=ft.alignment.top_center,
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