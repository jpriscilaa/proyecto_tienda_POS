import flet as ft
from backend import Constantes, PDF
from backend.modelo.Cliente import Cliente
from backend.modelo.Venta import Venta

def venta_view(page: ft.Page):
    def seleccionar_venta(venta):
        print("Venta seleccionada:", venta.id)

    tabla_ventas = ft.Column()

    def actualizar_tabla(filtro=None):
        lista = Venta.obtener_todos()
        if filtro:
            palabras = filtro.lower().split()
            lista_filtrada = []

            for v in lista:
                texto_busqueda = f"{v.fecha} {v.pago} {v.cliente.nombre} {v.cliente.apellido}".lower()
                if all(palabra in texto_busqueda for palabra in palabras):
                    lista_filtrada.append(v)

            lista = lista_filtrada 

        filas = []
        for v in lista:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(v.id))),
                    ft.DataCell(ft.Text(v.fecha)),
                    ft.DataCell(ft.Text(v.pago)),
                    ft.DataCell(ft.Text(f"{v.cliente.nombre} {v.cliente.apellido}")),
                    ft.DataCell(ft.Text(str(v.cantidad_prod))),
                    ft.DataCell(ft.Text(str(v.total))),
                ],
                selected=False,
                data=v,
                on_select_changed=lambda e: seleccionar_venta(e.control.data)
            )
            filas.append(fila)

        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Pago")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Total"))
            ],
            rows=filas
        )

        tabla_ventas.controls.clear()
        tabla_ventas.controls.append(
            ft.Container(
                height=400,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()


 # --- Componentes ---
    venta_id = ft.TextField(label="ID Venta", visible=False)
    fecha = ft.TextField(label="Fecha (YYYY-MM-DD)")
    pago = ft.Dropdown(label="Método de pago", options=[
        ft.dropdown.Option("EFECTIVO"),
        ft.dropdown.Option("TARJETA"),
        ft.dropdown.Option("TRANSFERENCIA")
    ])
    cliente_nombre = ft.TextField(label="Nombre Cliente")
    cliente_apellido = ft.TextField(label="Apellido Cliente")
    cantidad_prod = ft.TextField(label="Cantidad de productos")
    total = ft.TextField(label="Total (€)")

    buscador_ventas = ft.TextField(label="Buscar venta", prefix_icon=ft.Icons.SEARCH , on_change = lambda e: actualizar_tabla(buscador_ventas.value))

    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO
    )

    btn_guardar_venta = ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Guardar venta",
        width=80,
        height=80
    )

    btn_editar_venta = ft.IconButton(
        icon=ft.Icons.EDIT,
        tooltip="Editar venta",
        width=80,
        height=80
    )

    btn_limpiar_venta = ft.IconButton(
        icon=ft.Icons.AUTO_DELETE,
        tooltip="Limpiar campos",
        width=80,
        height=80
    )

    def seleccionar_venta(venta):
        venta_id.value = str(venta.id)
        fecha.value = venta.fecha
        pago.value = venta.pago
        cliente_nombre.value = venta.cliente.nombre
        cliente_apellido.value = venta.cliente.apellido
        cantidad_prod.value = str(venta.cantidad_prod)
        total.value = str(venta.total)
        page.update()

    def guardar_pdf (self, e):
        nuevo_pdf = PDF()
        PDF.PDF.add_page
        column_width = [10,40,20,80,40]
        
   

    #meto los textfield en dos columnas
    columna_izquierda = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                venta_id,
                fecha,
                pago,
                cliente_nombre,
                cliente_apellido,
                cantidad_prod,
                total,
                ft.Row(controls=[btn_guardar_venta, btn_editar_venta, btn_limpiar_venta])
            ]
        )
    )

    columna_derecha = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                buscador_ventas,
                tabla_ventas
            ]
        )
    )

    fila_superior = ft.Row(
        controls=[btn_volver_dashboard, ft.Text("Gestión de Ventas")]
    )

    fila_medio = ft.Row(
        controls=[columna_izquierda, columna_derecha],
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    datos = ft.Column(
        controls=[fila_superior, fila_medio]
    )

    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )
    actualizar_tabla()
    return contenedor