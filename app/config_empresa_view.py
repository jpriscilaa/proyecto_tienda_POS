import flet as ft
from backend.servicios import iva_service
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Iva import Iva
from backend.servicios.categoria_service import listar_categorias, guardar_categoria
from backend.modelo.Categoria import Categoria

def config_empresa_view(page: ft.Page):

    categoria_id_input = ft.TextField(label="ID nueva categoría")
    categoria_nombre_input = ft.TextField(label="Nombre nueva categoría")
    filtro_categoria = ft.TextField(label="Buscar categoría")

    lista_categorias = ft.ListView(expand=True, spacing=5, height=150, padding=10)

    categorias = listar_categorias()

    # Cargar configuración empresa (si existe)
    config = Config_Empresa.obtener_config_empresa()
    if config is None:
        config = Config_Empresa("", "", "", "", "")

    Config_Empresa.crear_tabla_config_empresa()

      
    config = Config_Empresa.obtener_config_empresa()

    nombre_input = ft.TextField(label="Nombre", value=config.nombre if config else "", disabled=True)
    direccion_input = ft.TextField(label="Dirección", value=config.direccion if config else "", disabled=True)
    telefono_input = ft.TextField(label="Teléfono", value=config.telefono if config else "", disabled=True)
    moneda_input = ft.TextField(label="Moneda", value=config.moneda if config else "", disabled=True)

    def editar_click(e):
        nombre_input.disabled = False
        direccion_input.disabled = False
        telefono_input.disabled = False
        moneda_input.disabled = False
        page.update()

    # Función para guardar datos
    def guardar_click(e):
        # Crear objeto Config_Empresa (usa un id fijo si solo habrá uno)
        nueva_config = Config_Empresa(
            empresa_id="1",
            nombre=nombre_input.value,
            direccion=direccion_input.value,
            telefono=telefono_input.value,
            moneda=moneda_input.value
        )
        Config_Empresa.guardar_config_empresa(nueva_config)
        # Volver a deshabilitar inputs
        nombre_input.disabled = True
        direccion_input.disabled = True
        telefono_input.disabled = True
        moneda_input.disabled = True
        page.update()

    editar_btn = ft.ElevatedButton(text="Editar datos", on_click=editar_click)
    guardar_btn = ft.ElevatedButton(text="Guardar", on_click=guardar_click)

    # --- Sección IVA ---

    # Inputs para IVA
    iva_nombre_input = ft.TextField(label="Nombre IVA")
    iva_porcentaje_input = ft.TextField(label="Porcentaje IVA (%)", keyboard_type=ft.KeyboardType.NUMBER)

    # Lista para mostrar IVAs existentes
    ivalist_view = ft.ListView(expand=True, spacing=5, padding=10)

    def cargar_ivas():
        ivalist_view.controls.clear()
        ivas = iva_service.listar_ivas()
        for iva in ivas:
            ivalist_view.controls.append(
                ft.Text(f"{iva.nombre} - {iva.porcentaje}% (ID: {iva.iva_id})")
            )
        page.update()

    def on_agregar_iva(e):
        nombre = iva_nombre_input.value.strip()
        try:
            porcentaje = float(iva_porcentaje_input.value.strip())
        except:
            porcentaje = None

        if not nombre or porcentaje is None:
            page.snack_bar = ft.SnackBar(ft.Text("Introduce nombre y porcentaje válidos"))
            page.snack_bar.open = True
            page.update()
            return

        import uuid
        nuevo_iva = Iva(str(uuid.uuid4()), nombre, porcentaje)

        if iva_service.crear_iva(nuevo_iva):
            iva_nombre_input.value = ""
            iva_porcentaje_input.value = ""
            cargar_ivas()
            page.snack_bar = ft.SnackBar(ft.Text("IVA creado correctamente"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al crear IVA"))

        page.snack_bar.open = True
        page.update()

    agregar_iva_btn = ft.ElevatedButton("Agregar IVA", on_click=on_agregar_iva)

    # Crear tabla IVA si no existe (al iniciar vista)
    iva_service.inicializar_iva()
    cargar_ivas()


    # --- Sección Categorías ---
    def mostrar_categorias(lista):
        lista_categorias.controls.clear()
        for c in lista:
            lista_categorias.controls.append(ft.Text(f"{c.categoria_id} - {c.nombre}"))
        page.update()

    def buscar_categoria(e):
        texto = filtro_categoria.value.lower()
        if texto == "":
            mostrar_categorias(categorias)
        else:
            filtradas = [c for c in categorias if texto in c.nombre.lower()]
            mostrar_categorias(filtradas)

    def guardar_nueva_categoria(e):
        try:
            nueva = Categoria(
                categoria_id=categoria_id_input.value,
                nombre=categoria_nombre_input.value
            )
            guardar_categoria(nueva)
            categorias.append(nueva)
            mostrar_categorias(categorias)
            categoria_id_input.value = ""
            categoria_nombre_input.value = ""
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar categoría: {ex}"))
            page.snack_bar.open = True
            page.update()

    filtro_categoria.on_change = buscar_categoria
    mostrar_categorias(categorias)

    # Construir vista completa
    return ft.View(
        route="/config",
        controls=[
            ft.Text("Configuración Empresa", size=25, weight=ft.FontWeight.BOLD),
            nombre_input,
            direccion_input,
            telefono_input,
            moneda_input,
            ft.Row([editar_btn, guardar_btn], spacing=10),

            ft.Divider(),

            ft.Text("Gestión de Tipos de IVA", size=20, weight=ft.FontWeight.BOLD),
            iva_nombre_input,
            iva_porcentaje_input,
            agregar_iva_btn,
            ivalist_view,

            ft.Divider(),

            ft.Text("Gestión de Categorías", size=20, weight=ft.FontWeight.BOLD),
            categoria_id_input,
            categoria_nombre_input,
            ft.ElevatedButton("Guardar nueva categoría", on_click=guardar_nueva_categoria),
            filtro_categoria,
            lista_categorias
        ]
    )
