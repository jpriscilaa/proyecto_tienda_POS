import flet as ft
from backend import Constantes
from backend.modelo.Cliente import Cliente
from backend.modelo.Venta import Venta

def venta_view(page: ft.Page):

    venta_id_actual = ft.TextField(visible=False)

    fecha = ft.TextField(label="Fecha", disabled=True, value="", expand=True)
    pago = ft.Dropdown(
        label="Método de Pago",
        options=[ft.dropdown.Option("EFECTIVO"), ft.dropdown.Option("TARJETA"), ft.dropdown.Option("TRANSFERENCIA")],
        expand=True
    )

    cliente_dropdown = ft.Dropdown(
        label="Cliente",
        options=[
            ft.dropdown.Option(f"{c.nombre} {c.apellido}", data=c)
            for c in Cliente.obtener_todos()
        ],
        expand=True
    )

    cantidad_prod = ft.TextField(label="Cantidad productos", expand=True)
    total = ft.TextField(label="Total", expand=True)

    btn_guardar = ft.ElevatedButton("Guardar", on_click=lambda e: guardar_venta())
    btn_editar = ft.ElevatedButton("Editar", disabled=True, on_click=lambda e: editar_venta())
    btn_limpiar = ft.OutlinedButton("Limpiar", on_click=lambda e: limpiar_campos())

    columna_izquierda = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                venta_id_actual,
                fecha,
                pago,
                cliente_dropdown,
                cantidad_prod,
                total,
                ft.Row(controls=[btn_guardar, btn_editar, btn_limpiar])
            ]
        )
    )

    # ---------- COLUMNA DERECHA ----------
    buscador_input = ft.TextField(label="Buscar por cliente", on_change=lambda e: actualizar_tabla(buscador_input.value), expand=True)
    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Fecha")),
            ft.DataColumn(label=ft.Text("Pago")),
            ft.DataColumn(label=ft.Text("Cliente")),
            ft.DataColumn(label=ft.Text("Cantidad")),
            ft.DataColumn(label=ft.Text("Total")),
        ],
        rows=[]
    )

    columna_derecha = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                buscador_input,
                tabla_ventas
            ]
        )
    )

    fila_superior = ft.Row(controls=[ft.ElevatedButton("← Volver", on_click=lambda e: page.go("/dashboard")), ft.Text("Gestión de Ventas", size=20)])
    fila_medio = ft.Row(controls=[columna_izquierda, columna_derecha], vertical_alignment=ft.CrossAxisAlignment.START)

    datos = ft.Column(controls=[fila_superior, fila_medio])
    contenedor = ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        content=datos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    # ---------- FUNCIONES ----------
    def actualizar_tabla(filtro=""):
        ventas = Venta.obtener_todos()
        if filtro:
            ventas = [v for v in ventas if filtro.lower() in v.cliente.nombre.lower()]
        
        tabla_ventas.rows.clear()
        for v in ventas:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v.fecha)),
                    ft.DataCell(ft.Text(v.pago)),
                    ft.DataCell(ft.Text(f"{v.cliente.nombre} {v.cliente.apellido}")),
                    ft.DataCell(ft.Text(str(v.cantidad_prod))),
                    ft.DataCell(ft.Text(str(v.total))),
                ]
            )
            tabla_ventas.rows.append(fila)
        page.update()

    def guardar_venta():
        cliente_obj = cliente_dropdown.value.data if cliente_dropdown.value else None
        if not cliente_obj:
            page.snack_bar = ft.SnackBar(ft.Text("Selecciona un cliente válido"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        nueva_venta = Venta(
            fecha=fecha.value,
            pago=pago.value,
            cliente=cliente_obj,
            cantidad_prod=cantidad_prod.value,
            total=total.value
        )
        if nueva_venta.guardar():
            limpiar_campos()
            actualizar_tabla()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al guardar la venta"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    def editar_venta():
        # Esta función se completa si luego implementas doble click o selección de fila
        pass

    def limpiar_campos():
        fecha.value = ""
        pago.value = None
        cliente_dropdown.value = None
        cantidad_prod.value = ""
        total.value = ""
        btn_editar.disabled = True
        page.update()

    # Inicial
    actualizar_tabla()
    limpiar_campos()

    return contenedor
