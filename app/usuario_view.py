import flet as ft
from backend.modelo.Usuario import Usuario
from backend import Constantes
from app import ventana_alerta
from backend.modelo.Usuario import Usuario
import logging
logger=logging.getLogger(__name__)

def usuario_view(page: ft.Page, usuario: Usuario):

    #metodos
    def mostrar_dialogo():
        page.open(ventana_alerta.alerta_error("Error", "Ya existe este usuario"))
        pass

    def volver_al_dashboard(e):
        from app.dashboard_view import dashboard_view
        page.clean()
        dashboard=dashboard_view(page,usuario)
        page.add(dashboard)
        page.update()

    def actualizar_tabla(filtro=None):
        lista=Usuario.obtener_todos()
        if filtro:
            lista=[u for u in lista if filtro.upper() in u.nombre_usuario.upper()]

        def eliminar_usuario(e, usuario_id):
            try:
                Usuario.borrar_por_id(usuario_id)
                actualizar_tabla(buscador_input.value)
            except Exception:
                print("Error al borrar")
                page.update()
        filas=[]
        for u in lista:
            fila=ft.DataRow(
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

        data_table=ft.DataTable(
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
            mostrar_dialogo()
            print("Ya existe un usuario con ese nombre")
        elif not nombre_usuario.value or not nombre_trabajador.value or not apellido.value or not ntelefono.value or not contrasena_usuario.value or not rol_usuario.value:
            print("todos los campos son obligatorios")
            page.open(ventana_alerta.alerta_error("USUARIO", "Debe de rellenar todos los campos"))
        elif len(contrasena_usuario.value)<=5:
            print("Tiene que tener mas de 5 digitos")
            page.open(ventana_alerta.alerta_error("USUARIO", "Tiene que tener mas de 5 digitos"))
        else:
            nuevo_usuario=Usuario(
                nombre_usuario=nombre_usuario.value,
                trabajador=nombre_trabajador.value,
                apellido=apellido.value,
                ntelefono=ntelefono.value,
                contrasena=contrasena_usuario.value,
                rol=rol_usuario.value
            )
            nuevo_usuario.guardar()
            print("Usuario creado correctamente")

    def limpiar_campos():
        #Limpiar campos
        nombre_usuario.value=None
        contrasena_usuario.value=None
        nombre_trabajador.value=None
        apellido.value=None
        ntelefono.value=None
        rol_usuario.value=None
        page.update()
        actualizar_tabla()

    #Componentes
    buscador_input=ft.TextField(label="Buscar usuario", prefix_icon=ft.Icons.SEARCH)
    nombre_usuario=ft.TextField(label="Nombre de usuario", autofocus=True, width=300)
    nombre_trabajador=ft.TextField(label="Nombre del trabajador")
    apellido=ft.TextField(label="Apellido del vendedor")
    ntelefono=ft.TextField(label="Numero de telefono")
    contrasena_usuario=ft.TextField(label="Contraseña", password=True, width=300)
    rol_usuario=ft.Dropdown(
        label="Rol de usuario",
        options=[
            ft.dropdown.Option("ADMINISTRADOR"),
            ft.dropdown.Option("VENDEDOR")
        ],
        width=300
    )
    tabla_usuarios=ft.Column()

    buscador_input.on_change=lambda e: actualizar_tabla(buscador_input.value)
    btn_volver_dashboard=ft.ElevatedButton(
        text="Volver al Dashboard",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver_al_dashboard,
        bgcolor=Constantes.COLOR_FONDO_PRINCIPAL,
        color=Constantes.COLOR_BOTON_PRIMARIO
    )

    layout=ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                buscador_input,
                ft.Row(
                    controls=[
                        btn_volver_dashboard,
                        nombre_usuario,
                        nombre_trabajador,
                        apellido,
                        ntelefono,
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
