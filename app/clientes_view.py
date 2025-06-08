import flet as ft
from backend import Constantes
from backend.modelo.Cliente import Cliente
from backend.modelo.Usuario import Usuario
import uuid
import logging
log=logging.getLogger(__name__)

def clientes_view(page: ft.Page, usuario: Usuario):

    cliente_seleccionado: Cliente=None
    page.clean()
    page.window.width=1000
    page.window.center=True

    tabla_clientes=ft.Column()

    #Metodos
    def deshabilitar_campos(habilitar: bool):
        nombre.disabled=habilitar
        apellido.disabled=habilitar
        documento.disabled=habilitar
        telefono.disabled=habilitar
        direccion.disabled=habilitar
       
        btn_editar_prod.disabled=habilitar
        btn_limpiar_prod.disabled=habilitar
        page.update()
    
    def limpiar_campos(e=None, btn=None):
        cliente_id_actual.value=""
        nombre.value=""
        apellido.value=""
        documento.value=""
        telefono.value=""
        direccion.value=""
        nombre.focus()
        page.update()
        if btn==True:
            deshabilitar_campos(habilitar=True)
            pass
    def nuevo_cliente(e):
        if nombre.disabled==True:
            deshabilitar_campos(habilitar=False)
        else:
            if nombre.disabled==False and apellido.value and documento.value and telefono.value and direccion.value:
                cliente_nuevo=Cliente(
                    cliente_nombre=nombre.value,
                    cliente_apellido=apellido.value,
                    cliente_documento=documento.value,
                    cliente_telefono=telefono.value,
                    cliente_direccion=direccion.value
                )
                log.info("Dirección recibida:", direccion.value)

                salida=cliente_nuevo.guardar()
                if salida:
                    log.info("Se ha insertado corrextamente")
                else:
                    log.info("Ha fallado a la hora se guardar el prodoucto")

                actualizar_tabla()
                limpiar_campos()
                
            else:
                log.info("Faltan datos necesarios para crear producto")
            pass
    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard=dashboard_view(page, usuario)
        page.add(dashboard)
        page.update()
    
    def seleccionar_producto(cliente: Cliente):
        cliente_id_actual.value=str(cliente.id)
        nombre.value=cliente.nombre
        apellido.value=cliente.apellido
        documento.value=cliente.documento
        telefono.value=cliente.telefono
        direccion.value=cliente.direccion
        page.update()

    def actualizar_tabla(filtro=None):
        lista=Cliente.obtener_todos()
        if filtro:
            lista=[cl for cl in lista if filtro.lower() in cl.nombre.lower()]

        def eliminar_clientes(e, cliente_id):
            Cliente.borrar_por_id(cliente_id)
            actualizar_tabla(buscador_input.value)
            page.update()
        filas=[]
        for cl in lista:
            fila=ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(cl.nombre)),
                    ft.DataCell(ft.Text(cl.apellido)),
                    ft.DataCell(ft.Text(cl.documento)),
                    ft.DataCell(ft.Text(cl.telefono)),
                    ft.DataCell(ft.Text(cl.direccion)),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar producto",
                        on_click=lambda e, id=cl.id: eliminar_clientes(e, id)
                        )
                    )
                ],
                selected=False
                ,data=cl
                ,on_select_changed=lambda e: seleccionar_producto(e.control.data)
            ) 
            filas.append(fila)

        data_table=ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Documento")),
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Direccion/Domicilio")),

                ft.DataColumn(ft.Text("Acciones"))

            ],
            rows=filas
        )

        tabla_clientes.controls.clear()
        tabla_clientes.controls.append(
            ft.Container(height=400,
                         content=ft.Column(
                             controls=[data_table],
                             scroll=ft.ScrollMode.AUTO
                         ))
        )
        page.update()
    #Campos
    nombre=ft.TextField(label="Nombre", disabled=True)
    apellido=ft.TextField(label="Apellidos", disabled=True)
    documento=ft.TextField(label="Documento (DNI/Pasaporte)", disabled=True)
    telefono=ft.TextField(label="Numero de telefono", disabled=True)
    direccion=ft.TextField(label="Direccion de residencia", disabled=True)
    cliente_id_actual=ft.TextField(label="ID del producto", visible=False, disabled=True)

    buscador_input=ft.TextField(label="Buscar cliente por documento", prefix_icon=ft.Icons.SEARCH)
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
        height=80
    )
    btn_guardar_prod=ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Nuevo producto",
        width=80,
        height=80,
        on_click=nuevo_cliente
    )
    btn_limpiar_prod=ft.IconButton(
        icon=ft.Icons.AUTO_DELETE,
        tooltip="Nuevo producto",
        width=80,
        height=80,
        on_click=lambda e: limpiar_campos(e, True)
    )   

   #Estructura de la vista
    columna_izquierda=ft.Container(alignment=ft.alignment.top_center, 
        content=ft.Column(
        controls=[
        nombre,
        apellido,
        documento,
        telefono,
        direccion,
        ft.Row(controls=[btn_guardar_prod, btn_editar_prod, btn_limpiar_prod])
    ])
    )

    columna_derecha=ft.Container(alignment=ft.alignment.top_center,
        content=ft.Column(
        controls=[
        buscador_input,
        tabla_clientes
    ])
    )
    fila_superior=ft.Row(controls=[btn_volver_dashboard, ft.Text("Gestión de Clientes",size=24, weight=ft.FontWeight.BOLD)])
    fila_medio=ft.Row(controls=[columna_izquierda, columna_derecha], vertical_alignment=ft.CrossAxisAlignment.START)
    datos=ft.Column(controls=[fila_superior, fila_medio])
    contenedor=ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    buscador_input.on_change=lambda e: actualizar_tabla(buscador_input.value)
    actualizar_tabla()
    deshabilitar_campos(True)

    return contenedor