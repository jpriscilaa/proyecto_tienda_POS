import flet as ft
from backend.modelo.Producto import Producto
from backend.modelo.Iva import Iva
from backend.modelo.Categoria import Categoria
from backend.modelo.Usuario import Usuario
from backend import Constantes
from app import ventana_alerta
import logging
logger=logging.getLogger(__name__)

def producto_view(page: ft.Page, usuario: Usuario):
    
    page.clean()
    page.window.width=1080
    page.window.center=True
    #inicializamos un colum para que sea accesible al resto de componentes y metodos
    tabla_productos=ft.Column()

    #Metodos
    def editar_producto(e):
        if nombre.value:
            deshabilitar_campos(False)

    def agregar_producto(e):
        #con control.disable hacemos que no se pueda volver a clicar el componente q recibo por el evento e
        
        if n_ref.disabled==True:
            deshabilitar_campos(habilitar=False)
            logger.info("Habilitamos los campos par que se pueda rellenar")
            n_ref.focus()
            page.update()
        else:
            e.control.disabled=True
            if n_ref.disabled==False and precio.value and nombre.value and n_ref.value and categoria_dropdown.value and iva_dropdown.value:
                producto_nuevo=Producto(
                    precio.value,
                    nombre.value,
                    n_ref.value,
                    Categoria.buscar_por_id(categoria_dropdown.value),
                    Iva.buscar_por_id(iva_dropdown.value),
                    prod_id_actual.value
                )

                #he modificado guardar para que me devuelva un boolean y asi saber si ha funcionado o ha fallado
                if producto_nuevo.guardar():
                    logging.info("Se ha guardado producto " + producto_nuevo.__str__())
                    page.open(ventana_alerta.barra_ok_mensaje("PRODUCTO GUARDADO"))
                    page.update()
                else:
                    logging.info("Ha fallado a la hora de guardar el producto")
                    page.open(ventana_alerta.barra_error_mensaje("ERROR AL GUARDAR, REVISE QUE NO EXISTA YA EL CODIGO DE BARRAS"))
                    page.update()

                actualizar_tabla()
                limpiar_campos()

                #Ya que se guarda el trabajo ahora se activa para que se pueda volver a clicar
                e.control.disabled=False
                page.update()
                
            else:
                page.open(ventana_alerta.barra_error_mensaje("RELLENE LOS DATOS CORRECTAMENTE"))
                logging.info("Faltan datos necesarios para crear producto")
            pass

    def validar_nombre(e):
        if not nombre.value.strip() and nombre.disabled==False:
            nombre.error_text="Este campo es obligatorio"
        else:
            nombre.error_text=None
        page.update()

    def limpiar_campos(e=None, btn=None):
        prod_id_actual.value=None
        n_ref.value=None
        nombre.value=None
        precio.value=None
        categoria_dropdown.value=None
        iva_dropdown.value=None
        if btn==True:
            deshabilitar_campos(habilitar=True)
        else:
            n_ref.focus()
        page.update()

    def deshabilitar_campos(habilitar: bool):
        n_ref.disabled=habilitar
        nombre.disabled=habilitar
        precio.disabled=habilitar
        categoria_dropdown.disabled=habilitar
        iva_dropdown.disabled=habilitar
        btn_limpiar_prod.disabled=habilitar
        btn_editar_prod.disabled=habilitar
        page.update()
    
    def seleccionar_producto(producto: Producto):
        producto_seleccionado=producto
        prod_id_actual.value=str(producto.id)
        n_ref.value=producto.n_referencia
        nombre.value=producto.nombre
        precio.value=str(producto.precio)
        categoria_dropdown.value=producto.categoria.categoria_id
        iva_dropdown.value=producto.iva.iva_id
        btn_editar_prod.disabled=False
        page.update()
    
    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard=dashboard_view(page,usuario)
        page.add(dashboard)
        page.update()
    
    def actualizar_tabla(filtro=None):
        lista=Producto.obtener_todos()
        if filtro:
            lista=[p for p in lista if filtro.lower() in p.nombre.lower()]

        def eliminar_producto(e, producto_id):
            Producto.borrar_por_id(producto_id)
            page.open(ventana_alerta.barra_info_mensaje("Se ha eliminado producto"))
            actualizar_tabla(buscador_input.value)
            page.update()
        filas=[]
        for p in lista:
            fila=ft.DataRow(
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
                        )
                    )
                ],
                selected=False
                ,data=p
                ,on_select_changed=lambda e: seleccionar_producto(e.control.data)
            ) 
            filas.append(fila)

        data_table=ft.DataTable(
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
        #borro controls y agrego la tabla
        tabla_productos.controls.clear()
        tabla_productos.controls.append(
            ft.Container(height=400,
                         content=ft.Column(
                             controls=[data_table],
                             scroll=ft.ScrollMode.AUTO
                         ))
        )
        page.update()

    #componentes vista
    n_ref=ft.TextField(label="Referencia")
    nombre=ft.TextField(label="Nombre", on_blur=validar_nombre)
    precio=ft.TextField(label="Precio")
    prod_id_actual=ft.TextField(label="ID del producto", visible=False, value=None)
    buscador_input=ft.TextField(label="Buscar producto", prefix_icon=ft.Icons.SEARCH)
    btn_volver_dashboard=ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO
    )
    btn_editar_prod=ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar producto",
        width=80,
        height=80,
        on_click=editar_producto
    )
    btn_guardar_prod=ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Guardar producto",
        width=80,
        height=80,
        on_click=agregar_producto
    )
    btn_limpiar_prod=ft.IconButton(
        icon=ft.Icons.AUTO_DELETE,
        tooltip="Limpiar campos",
        width=80,
        height=80,
        on_click=lambda e: limpiar_campos(e, True)
    )   

    #Relleno lista de categoria con cada categoria que hay en bd
    categorias=Categoria.obtener_todos()
    categoria_option=[]
    for c in categorias:
        option=ft.DropdownOption(
            text=c.nombre,
            key=c.categoria_id
        )
        categoria_option.append(option)
    categoria_dropdown=ft.Dropdown(label="Categoría", options=categoria_option, width=300, disabled=True)

    #Relleno lista de iva con cada iva que hay en bd
    ivas=Iva.obtener_todos()
    iva_option=[]
    for i in ivas:
        option=ft.DropdownOption(
            text=i.nombre,
            key=i.iva_id
        )
        iva_option.append(option)
    iva_dropdown=ft.Dropdown(label="IVA", options=iva_option, width=300, disabled=True)
    #iva_dropdown.value=Iva.buscar_por_nombre("Exento").iva_id

    #Estructura de la vista
    columna_izquierda=ft.Container(alignment=ft.alignment.top_center, 
                                            expand=True,

        content=ft.Column(
        controls=[
        n_ref,
        nombre,
        precio,
        prod_id_actual,
        categoria_dropdown,
        iva_dropdown,
        ft.Row(controls=[btn_guardar_prod, btn_editar_prod, btn_limpiar_prod])
    ])
    )

    columna_derecha=ft.Container(alignment=ft.alignment.top_center,
                                         expand=True,

        content=ft.Column(
        controls=[
        buscador_input,
        tabla_productos
    ])
    )
    fila_superior=ft.Row(expand=True,controls=[btn_volver_dashboard, ft.Text("Gestión de Producto", size=24)])
    fila_medio=ft.Row(expand=True,controls=[columna_izquierda, columna_derecha], vertical_alignment=ft.CrossAxisAlignment.START)
    datos=ft.Column(controls=[fila_superior, fila_medio])
    contenedor=ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    # Configurar el evento de búsqueda
    buscador_input.on_change=lambda e: actualizar_tabla(buscador_input.value)
    
    #Cargar datos iniciales
    actualizar_tabla()
    deshabilitar_campos(True)

    return contenedor