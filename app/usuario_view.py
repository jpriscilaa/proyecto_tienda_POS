import flet as ft
from backend.modelo.Usuario import Usuario

def usuario_view(page: ft.Page):
    buscador_input = ft.TextField(label="Buscar usuario", prefix_icon=ft.Icons.SEARCH)
    nombre_usuario = ft.TextField(label="Nombre de usuario", autofocus=True, width=300)
    contrasena_usuario = ft.TextField(label="Contraseña", password=True, width=300)
    rol_usuario = ft.Dropdown(
        label="Rol de usuario",
        options=[
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Vendedor")
        ],
        width=300
    )
    tabla_usuarios = ft.Column()

    def actualizar_tabla(filtro=None):
        lista = Usuario.obtener_todos()
        if filtro:
            lista = [u for u in lista if filtro.upper() in u.nombre_usuario.upper()]

        def eliminar_usuario(e, usuario_id):
            try:
                Usuario.borrar_por_id(usuario_id)
                actualizar_tabla(buscador_input.value)
            except Exception:
                print("Error al borrar")
                page.update()
        filas = []
        for u in lista:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(u.nombre_usuario)),
                    ft.DataCell(ft.Text(u.rol)),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar usuario",
                            on_click=lambda e, usuario_id=u.id: eliminar_usuario(e, usuario_id)
                        )
                    )
                ]
            )
            filas.append(fila)

        data_table = ft.DataTable(
            data_row_color={ft.ControlState.HOVERED: "#e3f2fd"},
            columns=[
                ft.DataColumn(label=ft.Text("Usuario")),
                ft.DataColumn(label=ft.Text("Rol")),
                ft.DataColumn(label=ft.Text("Acciones"))
            ],
            rows=filas
        )

        tabla_usuarios.controls.clear()
        tabla_usuarios.controls.append(
            ft.Container(
                height=400,
                content=ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        )
        page.update()

    def guardar_usuario(e):
        if Usuario.obtener_por_nombre_usuario(nombre_usuario.value):
            print("Ya existe un usuario con ese nombre")
        elif len(contrasena_usuario.value)<5:
            print("minimo 5 digitos")
        elif not nombre_usuario.value or not contrasena_usuario.value or not rol_usuario.value:
            print("todos los campos son obligatorios")
        else:
            nuevo_usuario = Usuario(
                nombre_usuario=nombre_usuario.value,
                contrasena=contrasena_usuario.value,
                rol=rol_usuario.value
            )
            nuevo_usuario.guardar()
            print("Usuario creado correctamente")

        # Limpiar campos
        nombre_usuario.value = ""
        contrasena_usuario.value = ""
        rol_usuario.value = None
        page.update()
        actualizar_tabla()

    buscador_input.on_change = lambda e: actualizar_tabla(buscador_input.value)

    layout = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                buscador_input,
                ft.Row(
                    controls=[
                        nombre_usuario,
                        contrasena_usuario,
                        rol_usuario,
                        ft.ElevatedButton("Guardar", on_click=guardar_usuario),
                    ],
                    spacing=10,
                    wrap=True
                ),
                tabla_usuarios
            ],
            spacing=20
        )
    )

    actualizar_tabla()
    return layout
