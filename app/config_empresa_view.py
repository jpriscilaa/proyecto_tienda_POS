import flet as ft
from backend import Constantes
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva
def config_empresa_view(page: ft.Page):
    empresa = Config_Empresa.obtener_config_empresa()
    
    nombre_empresa = ft.TextField(label="Nombre empresa", value=empresa.nombre, border=ft.InputBorder.UNDERLINE, border_radius=9, disabled=True)
    direccion_empresa = ft.TextField(label="Dirección empresa", value=empresa.direccion, border=ft.InputBorder.UNDERLINE, border_radius=9, disabled=True)
    telefono_empresa = ft.TextField(label="Teléfono empresa", value=empresa.telefono, border=ft.InputBorder.UNDERLINE, border_radius=9, disabled=True)
    moneda = ft.Dropdown(label="Moneda",border=ft.InputBorder.UNDERLINE,border_radius=9,disabled=True,value=empresa.moneda,options=[ft.dropdown.Option("EUR€"), ft.dropdown.Option("DOLR$")])
    
    def campos_empresa_abrir_cerrar(e, abierto: bool):
        nombre_empresa.disabled = abierto
        direccion_empresa.disabled = abierto
        telefono_empresa.disabled = abierto
        moneda.disabled = abierto
        page.update()
        pass

    def guardar_empresa(e):
        empresa_actualizada = Config_Empresa(
            empresa_id=1,
            nombre=nombre_empresa.value,
            direccion=direccion_empresa.value,
            telefono=telefono_empresa.value,
            moneda=moneda.value
        )
        empresa_actualizada.guardar()
        campos_empresa_abrir_cerrar(e, True)

    btn_editar = ft.ElevatedButton(text="Editar", on_click=lambda e: campos_empresa_abrir_cerrar(e, False))
    btn_guardar = ft.ElevatedButton(text="Guardar", on_click=guardar_empresa)

    # ------------------------------------------ Categorías ------------------------------------------
    categoria_nombre_input = ft.TextField(label="Nombre Categoría")
    buscador_input = ft.TextField(label="Buscar categoría", prefix_icon=ft.Icons.SEARCH)

    tabla_categorias = ft.Column()

    def seleccionar_categoria(categoria: Categoria):
        print("Categoría seleccionada:", categoria.nombre)
        

    def actualizar_tabla(filtro=None):
        lista = Categoria.obtener_todos()
        if filtro:
            lista = [c for c in lista if filtro.upper() in c.nombre]

        def eliminar_categoria(e, categoria_id):
            Categoria.borrar_por_id(categoria_id)
            actualizar_tabla(buscador_input.value)

        page.update()

        #creamos lista para meter datarow
        filas=[]
        for c in lista:
            fila = ft.DataRow([
                ft.DataCell(ft.Text(c.nombre)), 
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Eliminar categoría",
                        on_click=lambda e, id=c.categoria_id: eliminar_categoria(e, id)
                    )
                )],
                selected=False,
                on_select_changed=lambda e: seleccionar_categoria(e.control.data)
                )
            filas.append(fila)

        data_table = ft.DataTable(
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
        if categoria_nombre_input.value.strip():
            Categoria(nombre=categoria_nombre_input.value.strip()).guardar()
            categoria_nombre_input.value = ""
            actualizar_tabla(buscador_input.value)

    buscador_input.on_change = lambda e: actualizar_tabla(buscador_input.value)

    actualizar_tabla()
    # ------------------------------------------ Iva -----------------------------------------------

    iva_nombre = ft.TextField(label="Nombre IVA")
    iva_valor = ft.TextField(label="Valor %")
    buscador_iva = ft.TextField(label="Buscar IVA", prefix_icon=ft.Icons.SEARCH)
    tabla_ivas = ft.Column()

    def habilitar_edicion_iva(e):
        iva_nombre.disabled = False
        iva_valor.disabled = False
        page.update()
    def actualizar_tabla_iva(filtro=""):
        lista = Iva.obtener_todos()
        if filtro:
            lista = [i for i in lista if filtro.lower() in i.nombre.lower()]

        def eliminar_iva(e, iva_id):
            Iva.borrar_por_id(iva_id)
            actualizar_tabla_iva(buscador_iva.value)

        page.update()

        filas = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(i.nombre)),
                    ft.DataCell(ft.Text(f"{i.porcentaje}%")),  # <-- Aquí estaba el error
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar IVA",
                            on_click=lambda e, id=i.iva_id: eliminar_iva(e, id)
                        )
                    )
                ]
            ) for i in lista
        ]

        data_table = ft.DataTable(
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
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()

    def guardar_iva(e):
        habilitar_edicion_iva(e)
        if iva_nombre.value.strip() and iva_valor.value.strip(): 
            iva = Iva(nombre=iva_nombre.value.strip(), porcentaje=float(iva_valor.value.strip()))
            iva.guardar()
            iva_nombre.value = ""
            iva_valor.value = ""
            actualizar_tabla_iva(buscador_iva.value)

            page.update()
    # ------------------------------------------ Interfaz ------------------------------------------

    formulario = ft.Column([
        nombre_empresa,
        direccion_empresa,
        telefono_empresa,
        moneda,
        ft.Row([btn_editar, btn_guardar], alignment=ft.MainAxisAlignment.CENTER),
        ft.Text("Gestión de Categorías", size=18, weight="bold"),
        ft.Row([
            ft.Column([
                categoria_nombre_input,
                ft.ElevatedButton("Guardar Categoría", on_click=guardar_nueva_categoria),
            ], spacing=10),
            ft.Column([
                buscador_input,
                ft.Text("Categorías registradas:", weight="bold"),
                tabla_categorias
            ], spacing=10, expand=True)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ft.Text("Gestión de IVA", size=18, weight="bold"),
        ft.Row([
            ft.Column([
                iva_nombre,
                iva_valor,
                ft.ElevatedButton("Guardar IVA", on_click=guardar_iva)
            ], spacing=10),
            ft.Column([
                buscador_iva,
                ft.Text("IVA registrados:", weight="bold"),
                tabla_ivas
            ], spacing=10, expand=True)
        ])
        
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=formulario,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    page.title = "Configuración Empresa"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = Constantes.COLOR_FONDO_PRINCIPAL

    return contenedor
