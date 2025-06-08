import flet as ft
from backend import Constantes
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva
from backend.modelo.Usuario import Usuario
import logging
logger=logging.getLogger(__name__)

def config_empresa_view(page: ft.Page, usuario: Usuario):
    empresa=Config_Empresa.obtener_config_empresa()
    
    nombre_empresa=ft.TextField(label="Nombre empresa", value=empresa.nombre, border=ft.InputBorder.UNDERLINE, border_radius=9, disabled=True)
    direccion_empresa=ft.TextField(label="Dirección empresa", value=empresa.direccion, border=ft.InputBorder.UNDERLINE, border_radius=9, disabled=True)
    telefono_empresa=ft.TextField(label="Teléfono empresa", value=empresa.telefono, border=ft.InputBorder.UNDERLINE, border_radius=9, disabled=True)
    moneda=ft.Dropdown(label="Moneda",border=ft.InputBorder.UNDERLINE,border_radius=9,disabled=True,value=empresa.moneda,options=[ft.dropdown.Option("EUR€"), ft.dropdown.Option("DOLR$")])


    def campos_empresa_abrir_cerrar(e, abierto: bool):
        nombre_empresa.disabled=abierto
        direccion_empresa.disabled=abierto
        telefono_empresa.disabled=abierto
        moneda.disabled=abierto
        page.update()
        pass

    def guardar_empresa(e):
        empresa_actualizada=Config_Empresa(
            empresa_id=1,
            nombre=nombre_empresa.value,
            direccion=direccion_empresa.value,
            telefono=telefono_empresa.value,
            moneda=moneda.value
        )
        empresa_actualizada.guardar()
        campos_empresa_abrir_cerrar(e, True)

    btn_editar=ft.IconButton(icon=ft.Icons.EDIT,icon_color=ft.Colors.BLUE,
        tooltip="Editar", on_click=lambda e: campos_empresa_abrir_cerrar(e, False))
    btn_guardar=ft.ElevatedButton(text="Guardar", on_click=guardar_empresa)

    # ------------------------------------------ Categorías ------------------------------------------
    categoria_nombre_input=ft.TextField(label="Nombre Categoría")
    buscador_input=ft.TextField(label="Buscar categoría", prefix_icon=ft.Icons.SEARCH)
    categoria_id_actual=ft.TextField(visible=False)  # Para almacenar el ID de la categoría seleccionada

    tabla_categorias=ft.Column()

    

    def habilitar_edicion_categoria(e):
        categoria_nombre_input.disabled=False
        page.update()

    btn_editar_categoria=ft.IconButton(
        icon=ft.Icons.EDIT,
        icon_color=ft.Colors.BLUE,
        tooltip="Editar",
        on_click=habilitar_edicion_categoria


    )

    def seleccionar_categoria(categoria: Categoria):
        categoria_id_actual.value=str(categoria.categoria_id)
        categoria_nombre_input.value=categoria.nombre
        print("Categoría seleccionada:", categoria.nombre)
        page.update()
        
    def campos_categoria_abrir_cerrar(e, abierto: bool):
        categoria_nombre_input.disabled=abierto
        page.update()
        pass

    def actualizar_tabla(filtro=None):
        lista=Categoria.obtener_todos()
        if filtro:
            lista=[c for c in lista if filtro.upper() in c.nombre]

        def eliminar_categoria(e, categoria_id):
            print(f"Eliminando categoría con ID: {categoria_id}")
            Categoria.borrar_por_id(categoria_id)
            actualizar_tabla(buscador_input.value)
 
        page.update()

        #creamos lista para meter datarow
        filas=[]
        for c in lista:
            fila=ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(c.nombre)), 
                    ft.DataCell(ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar categoría",
                            on_click=lambda e, categoria_id=c.categoria_id: eliminar_categoria(e, categoria_id)
                        )
                    )
                ],
                selected=False,
                data=c,  # Guardamos la categoría en el DataRow
                on_select_changed=lambda e: seleccionar_categoria(e.control.data)
                )
            filas.append(fila)

        data_table=ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: "#0000FF"},
            columns=[
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=filas
        )

        tabla_categorias.controls.clear()
        tabla_categorias.controls.append(
            ft.Container(
                height=300,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()

    def guardar_nueva_categoria(e):
        nombre = categoria_nombre_input.value.strip()

        # Si el campo está vacío y está deshabilitado, solo lo habilitamos para que escriba
        if not nombre and categoria_nombre_input.disabled:
            categoria_nombre_input.disabled = False
            page.update()
            return

        # Si está vacío pero habilitado, no hacemos nada
        if not nombre:
            return

        # Si hay una categoría seleccionada (edición)
        if categoria_id_actual.value:
            categoria_existente = Categoria.buscar_por_id(categoria_id_actual.value)
            if categoria_existente:
                categoria_existente.nombre = nombre
                categoria_existente.guardar()
        else:
            # Crear nueva categoría
            Categoria(nombre=nombre).guardar()

        # Limpiar y deshabilitar campo después de guardar
        categoria_id_actual.value = ""
        categoria_nombre_input.value = ""
        categoria_nombre_input.disabled = True

        actualizar_tabla(buscador_input.value)
        page.update()



    buscador_input.on_change=lambda e: actualizar_tabla(buscador_input.value)

    actualizar_tabla()
    # ------------------------------------------ Iva -----------------------------------------------
    iva_nombre=ft.TextField(label="Nombre IVA")
    iva_valor=ft.TextField(label="Valor %")
    buscador_iva=ft.TextField(label="Buscar IVA", prefix_icon=ft.Icons.SEARCH)
    tabla_ivas=ft.Column()
    iva_id_actual=ft.TextField(visible=False)

    def habilitar_edicion_iva(e):
        iva_nombre.disabled=False
        iva_valor.disabled=False
        page.update()

    btn_editar_iva=ft.IconButton(
        icon=ft.Icons.EDIT,
        icon_color=ft.Colors.BLUE,
        tooltip="Editar",
        on_click=habilitar_edicion_iva
    )

    def seleccionar_iva(iva: Iva):
        iva_id_actual.value=str(iva.iva_id)
        iva_nombre.value=iva.nombre
        iva_valor.value=str(iva.porcentaje)
        iva_nombre.disabled=True
        iva_valor.disabled=True
        page.update()

    def actualizar_tabla_iva(filtro=""):
        lista=Iva.obtener_todos()
        if filtro:
            lista=[i for i in lista if filtro.lower() in i.nombre.lower()]

        def eliminar_iva(e, iva_id):
            Iva.borrar_por_id(iva_id)
            actualizar_tabla_iva(buscador_iva.value)

        filas=[]
        for i in lista:
            fila=ft.DataRow(
                [
                    ft.DataCell(ft.Text(i.nombre)),
                    ft.DataCell(ft.Text(str(i.porcentaje))),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar IVA",
                            on_click=lambda e, iva_id=i.iva_id: eliminar_iva(e, iva_id)
                        )
                    )
                ],
                data=i,
                on_select_changed=lambda e: seleccionar_iva(e.control.data)
            )
            filas.append(fila)

        data_table=ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: "#0000FF"},
            columns=[
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Valor %")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=filas
        )

        tabla_ivas.controls.clear()
        tabla_ivas.controls.append(
            ft.Container(
                height=300,
                content=ft.Column(controls=[data_table], scroll=ft.ScrollMode.AUTO)
            )
        )
        page.update()

    def guardar_iva(e):
        nombre=iva_nombre.value.strip()
        valor=iva_valor.value.strip()

        if not nombre or not valor:
            return

        try:
            porcentaje=float(valor)
        except ValueError:
            return

        if iva_id_actual.value:  
            iva_existente=Iva.buscar_por_id(iva_id_actual.value)  
            if iva_existente:
                iva_existente.nombre=nombre
                iva_existente.porcentaje=porcentaje
                iva_existente.guardar()
        else:  
            nuevo_iva=Iva(nombre=nombre, porcentaje=porcentaje)
            nuevo_iva.guardar()

        iva_id_actual.value=""
        iva_nombre.value=""
        iva_valor.value=""
        iva_nombre.disabled=True
        iva_valor.disabled=True

        actualizar_tabla_iva(buscador_iva.value)
        page.update()
    
    actualizar_tabla_iva()

    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        page.add(dashboard_view(page,usuario))
        page.update()
    btn_volver_dashboard=ft.ElevatedButton(text="Volver al Dashboard",icon=ft.Icons.ARROW_BACK,on_click=volver_al_dashboard,bgcolor=ft.Colors.BLUE,color=ft.Colors.WHITE)

    # ------------------------------------------ Interfaz ------------------------------------------

    formulario=ft.Column([
        ft.Row([btn_volver_dashboard], alignment=ft.MainAxisAlignment.START),
        nombre_empresa,
        direccion_empresa,
        telefono_empresa,
        moneda,
        ft.Row([btn_editar, btn_guardar], alignment=ft.MainAxisAlignment.CENTER),

        ft.Text("Gestión de Categorías", size=18, weight="bold"),
        ft.Row([
            ft.Column([
                categoria_nombre_input,
                ft.ElevatedButton("Guardar Categoría", on_click=guardar_nueva_categoria)
            ], spacing=10),
            ft.Column([
                buscador_input,
                ft.Row([btn_editar_categoria, ft.Text("Categorías registradas:", weight="bold")]),
                tabla_categorias
            ], spacing=10, expand=True)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

        ft.Text("Gestión de IVA", size=18, weight="bold"),
        ft.Row([
            ft.Column([
                iva_nombre,
                iva_valor,
                ft.Row([btn_editar_iva, ft.ElevatedButton("Guardar IVA", on_click=guardar_iva)])
            ], spacing=10),
            ft.Column([
                buscador_iva,
                ft.Text("IVA registrados:", weight="bold"),
                tabla_ivas
            ], spacing=10, expand=True)
        ])
        
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

    contenedor=ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=formulario,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    page.title="Configuración Empresa"
    page.horizontal_alignment=ft.MainAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.START
    page.bgcolor=Constantes.COLOR_FONDO_PRINCIPAL

    return contenedor
