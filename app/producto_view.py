import flet as ft
from backend.servicios.producto_service import crear_tabla_producto, crear_producto, listar_productos, actualizar_producto
from backend.servicios.categoria_service import listar_categorias, crear_categoria
from backend.servicios.iva_service import listar_ivas

crear_tabla_producto()

def producto_view(page: ft.Page):
    # Inputs de producto

        nombre = ft.TextField(label="Nombre")
        precio = ft.TextField(label="Precio")
        categoria_dropdown = ft.Dropdown(label="Categoría")
        iva_dropdown = ft.Dropdown(label="IVA")
        filtro = ft.TextField(label="Buscar producto")
        producto_seleccionado = {"id": None}

        productos = listar_productos()
        categorias = listar_categorias()
        ivas = listar_ivas()
        nueva_categoria_nombre = ft.TextField(label="Nombre nueva categoría")
        nueva_categoria_id = ft.TextField(label="ID nueva categoría")
        categoria_dropdown.options = [
        ft.dropdown.Option(key=c.categoria_id, text=c.nombre) for c in categorias
        ]

        iva_dropdown.options = [
        ft.dropdown.Option(key=i.iva_id, text=f"{i.nombre} ({i.porcentaje}%)") for i in ivas
        ]   
        # DataTable con columnas
        data_table = ft.DataTable(
        expand=True,
        border=ft.border.all(2, "blue"),
        border_radius=10,
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(ft.Text("ID", color="white")),
            ft.DataColumn(ft.Text("Nombre", color="white")),
            ft.DataColumn(ft.Text("Precio", color="white")),
            ft.DataColumn(ft.Text("Categoría ID", color="white")),
            ft.DataColumn(ft.Text("IVA ID", color="white")),
        ],
        rows=[],
    )
        

        def mostrar_productos(productos_mostrar):
            data_table.rows.clear()
            for p in productos_mostrar:
                data_table.rows.append(
                ft.DataRow(
                on_select_changed= get_Index,
                cells=[
                ft.DataCell(ft.Text(p[0])),
                ft.DataCell(ft.Text(p[1])),
                ft.DataCell(ft.Text(str(p[2]))),
                ft.DataCell(ft.Text(p[3])),
                ft.DataCell(ft.Text(p[4])),
            ]
        )
    )

            page.update()

        def get_Index(e):
            if e.control.selected:
                e.control.selected = False
                producto_seleccionado["id"] = None
            else:
                e.control.selected = True
                producto_seleccionado["id"] = e.control.cells[0].content.value
                nombre.value = e.control.cells[1].content.value
                precio.value = e.control.cells[2].content.value
                categoria_dropdown.value = e.control.cells[3].content.value
                iva_dropdown.value = e.control.cells[4].content.value
            page.update()

        def buscar(e):
            texto = filtro.value.lower()
            if texto == "":
                mostrar_productos(productos)
            else:
                filtrados = [p for p in productos if texto in p[1].lower()]
                mostrar_productos(filtrados)

        def agregar(e):
            try:
                crear_producto(
                id="prod_" + nombre.value[:3].lower(),
                nombre=nombre.value,
                precio=float(precio.value),
                categoria_id=categoria_dropdown.value,
                iva_id=iva_dropdown.value
)               

                recargar()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
                page.snack_bar.open = True
                page.update()

        def recargar():
            nonlocal productos
            productos = listar_productos()
            mostrar_productos(productos)

        filtro.on_change = buscar
        mostrar_productos(productos)



        def actualizar(e):
            if producto_seleccionado["id"] is None:
                page.snack_bar = ft.SnackBar(ft.Text("Selecciona un producto para editar"))
                page.snack_bar.open = True
                page.update()
                return

            try:
                actualizar_producto(
                id=producto_seleccionado["id"],
                nombre=nombre.value,
                precio=float(precio.value),
                categoria_id=categoria_dropdown.value,
                iva_id=iva_dropdown.value
                )
                producto_seleccionado["id"] = None
                nombre.value = ""
                precio.value = ""
          
                recargar()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}"))
                page.snack_bar.open = True
                page.update()

        def guardar_categoria(e):
            try:
                crear_categoria(nueva_categoria_id.value, nueva_categoria_nombre.value)
                categoria_dropdown.options.append(
                    ft.dropdown.Option(
                        key=nueva_categoria_id.value,
                        text=nueva_categoria_nombre.value
                    )
                )
                categoria_dropdown.value = nueva_categoria_id.value  # Auto seleccionar
                nueva_categoria_id.value = ""
                nueva_categoria_nombre.value = ""
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al crear categoría: {ex}"))
                page.snack_bar.open = True
                page.update()
        
        #contenedor para la nueva categoria 
        contenedor_nueva_categoria = ft.Column([
            ft.Text("Crear nueva categoría", size=16),
            nueva_categoria_id,
            nueva_categoria_nombre,
            ft.ElevatedButton("Guardar categoría", on_click=guardar_categoria)
        ])

        acciones_iconos = ft.Row(
            controls=[
                ft.IconButton(
                    tooltip="Editar",
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.BLUE,
                    on_click=actualizar
                ),
                ft.IconButton(
                    tooltip="Descargar en PDF",
                    icon=ft.Icons.PICTURE_AS_PDF,
                    icon_color=ft.Colors.RED
                ),
                ft.IconButton(
                    tooltip="Descargar en Excel",
                    icon=ft.Icons.SAVE_ALT,
                    icon_color=ft.Colors.GREEN
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )

        return ft.View(
            route="/productos",
            controls=[
                ft.Text("Gestión de Productos", size=30),
                filtro,
                acciones_iconos,
                ft.Row([
                    ft.Column([
                        nombre,
                        precio,
                        categoria_dropdown,
                        iva_dropdown,
                        
                        ft.ElevatedButton("Agregar", on_click=agregar),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Tabla de Productos", size=20),
                                data_table
                            ]),
                            padding=10,
                            border=ft.border.all(1),
                            border_radius=10,
                            expand=1
                        )
                        
                        
                    ])
                    
                ])
            ]
        )
