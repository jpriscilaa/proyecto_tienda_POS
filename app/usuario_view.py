import flet as ft
from backend.modelo.Usuario import Usuario
from backend import Constantes
from app import ventana_alerta
import logging

logger = logging.getLogger(__name__)

def usuario_view(page: ft.Page, usuario: Usuario):
    page.clean()
    page.window.width = 1080
    page.window.center = True

    tabla_usuarios = ft.Column()

    # Métodos
    def mostrar_dialogo():
        page.open(ventana_alerta.alerta_error("Error", "Ya existe este usuario"))
        page.update()

    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard = dashboard_view(page, usuario)
        page.add(dashboard)
        page.update()

    def actualizar_tabla(filtro=None):
        lista = [u for u in Usuario.obtener_todos() if u.nombre_usuario.lower() != "admin"]
        if filtro:
            lista = [u for u in lista if filtro.upper() in u.nombre_usuario.upper()]

        def eliminar_usuario(e, usuario_id):
            try:
                Usuario.borrar_por_id(usuario_id)
                page.open(ventana_alerta.barra_info_mensaje("Usuario eliminado"))
                actualizar_tabla(buscador_input.value)
            except Exception:
                logger.error("Error al borrar el usuario")
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
            data_row_color={ft.ControlState.HOVERED: Constantes.COLOR_BORDE_CLARO},
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
            mostrar_dialogo()
        elif not all([nombre_usuario.value, nombre_trabajador.value, apellido.value, ntelefono.value, contrasena_usuario.value, rol_usuario.value]):
            page.open(ventana_alerta.alerta_error("USUARIO", "Debe de rellenar todos los campos"))
        elif len(contrasena_usuario.value) <= 5:
            page.open(ventana_alerta.alerta_error("USUARIO", "La contraseña debe tener más de 5 caracteres"))
        else:
            nuevo_usuario = Usuario(
                nombre_usuario=nombre_usuario.value,
                trabajador=nombre_trabajador.value,
                apellido=apellido.value,
                ntelefono=ntelefono.value,
                contrasena=contrasena_usuario.value,
                rol=rol_usuario.value
            )
            nuevo_usuario.guardar()
            page.open(ventana_alerta.barra_ok_mensaje("Usuario guardado correctamente"))
            limpiar_campos()
            actualizar_tabla()

    def limpiar_campos():
        nombre_usuario.value = None
        contrasena_usuario.value = None
        nombre_trabajador.value = None
        apellido.value = None
        ntelefono.value = None
        rol_usuario.value = None
        page.update()

    # Componentes
    buscador_input = ft.TextField(label="Buscar usuario", prefix_icon=ft.Icons.SEARCH)
    buscador_input.on_change = lambda e: actualizar_tabla(buscador_input.value)

    nombre_usuario = ft.TextField(label="Nombre de usuario", autofocus=True)
    nombre_trabajador = ft.TextField(label="Nombre del trabajador")
    apellido = ft.TextField(label="Apellido del vendedor")
    ntelefono = ft.TextField(label="Número de teléfono")
    contrasena_usuario = ft.TextField(label="Contraseña", password=True)
    rol_usuario = ft.Dropdown(
        label="Rol de usuario",
        options=[
            ft.dropdown.Option("ADMINISTRADOR"),
            ft.dropdown.Option("VENDEDOR")
        ]
    )

    btn_volver_dashboard = ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO
    )

    btn_guardar_usuario = ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Guardar usuario",
        width=80,
        height=80,
        on_click=guardar_usuario
    )

    btn_limpiar_usuario = ft.IconButton(
        icon=ft.Icons.AUTO_DELETE,
        tooltip="Limpiar campos",
        width=80,
        height=80,
        on_click=lambda e: limpiar_campos()
    )

    # Estructura visual
    columna_izquierda = ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        content=ft.Column(
            controls=[
                nombre_usuario,
                nombre_trabajador,
                apellido,
                ntelefono,
                contrasena_usuario,
                rol_usuario,
                ft.Row(controls=[btn_guardar_usuario, btn_limpiar_usuario])
            ]
        )
    )

    columna_derecha = ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        content=ft.Column(
            controls=[
                buscador_input,
                tabla_usuarios
            ]
        )
    )

    fila_superior = ft.Row(
        controls=[btn_volver_dashboard, ft.Text("Gestión de Usuario", size=24)]
    )

    fila_medio = ft.Row(
        controls=[columna_izquierda, columna_derecha],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    datos = ft.Column(controls=[fila_superior, fila_medio])

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
