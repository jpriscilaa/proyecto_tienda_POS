import flet as ft
from backend.servicios import iva_service
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Iva import Iva
from backend.servicios.categoria_service import listar_categorias, guardar_categoria
from backend.modelo.Categoria import Categoria
import random
import uuid
from backend.Constantes import NOMBRE_APP

def config_empresa_view(page: ft.Page):
    def mostrar_dialogo(texto, titulo="Mensaje", color=ft.Colors.PRIMARY):
        def cerrar(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(texto),
            actions=[ft.TextButton("Cerrar", on_click=cerrar)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    categoria_nombre_input = ft.TextField(label="Nombre nueva categoría")
    filtro_categoria = ft.TextField(label="Buscar categoría")

    categoria_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
        ],
        rows=[]
    )
    categorias = listar_categorias()

    config = Config_Empresa.obtener_config_empresa()
    if config is None:
        config = Config_Empresa("", "", "", "", "")
    Config_Empresa.crear_tabla_config_empresa()

    nombre_input = ft.TextField(label="Nombre", value=config.nombre, disabled=True)
    direccion_input = ft.TextField(label="Dirección", value=config.direccion, disabled=True)
    telefono_input = ft.TextField(label="Teléfono", value=config.telefono, disabled=True)
    moneda_input = ft.TextField(label="Moneda", value=config.moneda, disabled=True)

    def editar_click(e):
        nombre_input.disabled = False
        direccion_input.disabled = False
        telefono_input.disabled = False
        moneda_input.disabled = False
        page.update()

    def guardar_click(e):
        nueva_config = Config_Empresa(
            empresa_id="1",
            nombre=nombre_input.value,
            direccion=direccion_input.value,
            telefono=telefono_input.value,
            moneda=moneda_input.value
        )
        Config_Empresa.guardar_config_empresa(nueva_config)
        nombre_input.disabled = True
        direccion_input.disabled = True
        telefono_input.disabled = True
        moneda_input.disabled = True
        page.update()
        mostrar_dialogo("Configuración guardada correctamente", "Éxito", ft.Colors.GREEN)

    editar_btn = ft.ElevatedButton(text="Editar datos", on_click=editar_click)
    guardar_btn = ft.ElevatedButton(text="Guardar", on_click=guardar_click)

    iva_nombre_input = ft.TextField(label="Nombre IVA")
    iva_porcentaje_input = ft.TextField(label="Porcentaje IVA (%)", keyboard_type=ft.KeyboardType.NUMBER)

    iva_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Porcentaje")),
            ft.DataColumn(label=ft.Text("ID")),
        ],
        rows=[]
    )

    def cargar_ivas():
        iva_table.rows.clear()
        for iva in iva_service.listar_ivas():
            iva_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(iva.nombre)),
                ft.DataCell(ft.Text(f"{iva.porcentaje}%")),
                ft.DataCell(ft.Text(iva.iva_id)),
            ]))
        page.update()

    def on_agregar_iva(e):
        nombre = iva_nombre_input.value.strip()
        try:
            porcentaje = float(iva_porcentaje_input.value.strip())
        except:
            porcentaje = None

        if not nombre or porcentaje is None:
            mostrar_dialogo("Introduce nombre y porcentaje válidos", "Error", ft.Colors.RED)
            return

        nuevo_iva = Iva(str(uuid.uuid4()), nombre, porcentaje)
        if iva_service.crear_iva(nuevo_iva):
            iva_nombre_input.value = ""
            iva_porcentaje_input.value = ""
            cargar_ivas()
            mostrar_dialogo("IVA creado correctamente", "Éxito", ft.Colors.GREEN)
        else:
            mostrar_dialogo("Error al crear IVA", "Error", ft.Colors.RED)

    agregar_iva_btn = ft.ElevatedButton("Agregar IVA", on_click=on_agregar_iva)

    iva_service.inicializar_iva()
    cargar_ivas()

    def mostrar_categorias(lista):
        categoria_table.rows.clear()
        for c in lista:
            categoria_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c.categoria_id)),
                    ft.DataCell(ft.Text(c.nombre)),
                ])
            )
        page.update()

    mostrar_categorias(categorias)

    def buscar_categoria(e):
        texto = filtro_categoria.value.lower()
        if texto == "":
            mostrar_categorias(categorias)
        else:
            filtradas = [c for c in categorias if texto in c.nombre.lower()]
            mostrar_categorias(filtradas)

    def generar_id_unico(categorias_existentes):
        ids_existentes = {c.categoria_id for c in categorias_existentes}
        while True:
            nuevo_id = str(random.randint(1000, 9999))
            if nuevo_id not in ids_existentes:
                return nuevo_id

    def guardar_nueva_categoria(e):
        nombre = categoria_nombre_input.value.strip()

        if not nombre:
            mostrar_dialogo("El nombre de la categoría no puede estar vacío", "Error", ft.Colors.RED)
            return

        if any(nombre.lower() == c.nombre.lower() for c in categorias):
            mostrar_dialogo("Ya existe una categoría con ese nombre", "Error", ft.Colors.RED)
            return

        nuevo_id = generar_id_unico(categorias)

        try:
            nueva = Categoria(categoria_id=nuevo_id, nombre=nombre)
            guardar_categoria(nueva)
            categorias.append(nueva)
            mostrar_categorias(categorias)

            categoria_nombre_input.value = ""
            mostrar_dialogo("Categoría guardada correctamente", "Éxito", ft.Colors.GREEN)
        except Exception as ex:
            mostrar_dialogo(f"Error al guardar categoría: {ex}", "Error", ft.Colors.RED)

    return ft.View(
        route="/config",
        controls=[
            ft.Container(
            expand=True,

                content=ft.Column(
                    scroll=True,
                    controls=[
                        ft.Text(NOMBRE_APP, size=25, weight=ft.FontWeight.BOLD),

                        ft.Row([
                            ft.Container(nombre_input, width=300),
                            ft.Container(direccion_input, width=300),
                        ], spacing=10),

                        ft.Row([
                            ft.Container(telefono_input, width=300),
                            ft.Container(moneda_input, width=300),
                        ], spacing=10),

                        ft.Row([editar_btn, guardar_btn], spacing=10),

                        ft.Divider(),

                        ft.Text("Gestión de Tipos de IVA", size=20, weight=ft.FontWeight.BOLD),

                        ft.Row([
                            ft.Column([
                                ft.Container(iva_nombre_input, width=250),
                                ft.Container(iva_porcentaje_input, width=250),
                                agregar_iva_btn,
                            ], spacing=10),
                            ft.Container(iva_table, expand=True, padding=10)
                        ], spacing=20),

                        ft.Divider(),

                        ft.Text("Gestión de Categorías", size=20, weight=ft.FontWeight.BOLD),

                        ft.Row([
                            ft.Column([
                                ft.Container(categoria_nombre_input, width=200),
                                ft.ElevatedButton("Guardar nueva categoría", on_click=guardar_nueva_categoria),
                                filtro_categoria,
                                ft.ElevatedButton("Buscar", on_click=buscar_categoria),  # 👈 este botón

                            ], spacing=10),
                            ft.Container(categoria_table, expand=True, padding=10)
                        ], spacing=20),

                        ft.Divider(),

                        ft.ElevatedButton("Volver al Dashboard", on_click=lambda e: page.go("/dashboard"))
                    ]
                ),
                padding=20,
                alignment=ft.alignment.top_center
            )
        ]
    )
