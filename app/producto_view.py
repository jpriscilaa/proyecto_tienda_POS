import flet as ft
from backend.modelo.Producto import Producto
from backend.modelo.Iva import Iva
from backend.modelo.Categoria import Categoria
from backend.modelo.Usuario import Usuario
from backend import Constantes
from app import ventana_alerta
import logging
logger = logging.getLogger(__name__)


def producto_view(page: ft.Page, usuario: Usuario):
    page.clean()
    page.window.width = 1080
    page.window.center = True

    tabla_productos = ft.Column()

    def editar_producto(e):
        if nombre.value:
            deshabilitar_campos(False)

    def agregar_producto(e):
        if n_ref.disabled:
            deshabilitar_campos(False)
            logger.info("Habilitamos los campos para que se pueda rellenar")
            n_ref.focus()
            page.update()
        else:
            e.control.disabled = True
            if all([precio.value, nombre.value, n_ref.value, categoria_dropdown.value, iva_dropdown.value]):
                producto_nuevo = Producto(
                    precio.value,
                    nombre.value,
                    n_ref.value,
                    Categoria.buscar_por_id(categoria_dropdown.value),
                    Iva.buscar_por_id(iva_dropdown.value),
                    prod_id_actual.value
                )

                if producto_nuevo.guardar():
                    logging.info(f"Se ha guardado producto {producto_nuevo}")
                    page.open(ventana_alerta.barra_ok_mensaje("PRODUCTO GUARDADO"))
                else:
                    logging.info("Ha fallado a la hora de guardar el producto")
                    page.open(ventana_alerta.barra_error_mensaje(
                        "ERROR AL GUARDAR, REVISE QUE NO EXISTA YA EL CODIGO DE BARRAS"))

                actualizar_tabla()
                limpiar_campos()
                e.control.disabled = False
                page.update()
            else:
                page.open(ventana_alerta.barra_error_mensaje("RELLENE LOS DATOS CORRECTAMENTE"))
                logging.info("Faltan datos necesarios para crear producto")

    def validar_nombre(e):
        nombre.error_text = "Este campo es obligatorio" if not nombre.value.strip() and not nombre.disabled else None
        page.update()

    def limpiar_campos(e=None, btn=False):
        prod_id_actual.value = None
        n_ref.value = None
        nombre.value = None
        precio.value = None
        categoria_dropdown.value = None
        iva_dropdown.value = None
        deshabilitar_campos(not btn)
        page.update()

    def deshabilitar_campos(habilitar: bool):
        n_ref.disabled = habilitar
        nombre.disabled = habilitar
        precio.disabled = habilitar
        categoria_dropdown.disabled = habilitar
        iva_dropdown.disabled = habilitar
        btn_limpiar_prod.disabled = habilitar
        btn_editar_prod.disabled = habilitar
        page.update()

    def seleccionar_producto(producto: Producto):
        prod_id_actual.value = str(producto.id)
        n_ref.value = producto.n_referencia
        nombre.value = producto.nombre
        precio.value = str(producto.precio)
        categoria_dropdown.value = producto.categoria.categoria_id
        iva_dropdown.value = producto.iva.iva_id
        btn_editar_prod.disabled = False
        page.update()

    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard = dashboard_view(page, usuario)
        page.add(dashboard)
        page.update()

    def actualizar_tabla(filtro=None):
        lista = Producto.obtener_todos()
        if filtro:
            lista = [p for p in lista if filtro.lower() in p.nombre.lower()]

        def eliminar_producto(e, producto_id):
            Producto.borrar_por_id(producto_id)
            page.open(ventana_alerta.barra_info_mensaje("Se ha eliminado producto"))
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
                selected=False,
                data=p,
                on_select_changed=lambda e: seleccionar_producto(e.control.data)
            )
            filas.append(fila)

        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
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
                expand=True,
                height=400,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()

    # Componentes
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
    btn_editar_prod = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar producto", width=80, height=80, on_click=editar_producto)
    btn_guardar_prod = ft.IconButton(icon=ft.Icons.SAVE, tooltip="Guardar producto", width=80, height=80, on_click=agregar_producto)
    btn_limpiar_prod = ft.IconButton(icon=ft.Icons.AUTO_DELETE, tooltip="Limpiar campos", width=80, height=80, on_click=lambda e: limpiar_campos(e, True))

    # Dropdowns
    categoria_dropdown = ft.Dropdown(label="Categoría", options=[
        ft.DropdownOption(text=c.nombre, key=c.categoria_id) for c in Categoria.obtener_todos()
    ], width=300, disabled=True)

    iva_dropdown = ft.Dropdown(label="IVA", options=[
        ft.DropdownOption(text=i.nombre, key=i.iva_id) for i in Iva.obtener_todos()
    ], width=300, disabled=True)

    # Estructura visual
    fila_superior = ft.Row(
        controls=[
            btn_volver_dashboard,
            ft.Text("Gestión de Producto", size=24, weight=ft.FontWeight.BOLD)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    columna_izquierda = ft.Container(
        expand=1,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                n_ref,
                nombre,
                precio,
                prod_id_actual,
                categoria_dropdown,
                iva_dropdown,
                ft.Row(controls=[btn_guardar_prod, btn_editar_prod, btn_limpiar_prod])
            ],
            spacing=10,
            tight=True
        )
    )

    columna_derecha = ft.Container(
        expand=2,
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                buscador_input,
                ft.Container(
                    expand=True,
                    height=400,
                    content=ft.Column(
                        controls=[tabla_productos],
                        scroll=ft.ScrollMode.AUTO
                    )
                )
            ],
            spacing=10,
            tight=True
        )
    )

    fila_medio = ft.Row(
        controls=[columna_izquierda, columna_derecha],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    datos = ft.Column(
        controls=[fila_superior, fila_medio],
        spacing=20,
        expand=True
    )

    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    # Eventos
    buscador_input.on_change = lambda e: actualizar_tabla(buscador_input.value)

    # Inicialización
    actualizar_tabla()
    deshabilitar_campos(True)

    return contenedor
