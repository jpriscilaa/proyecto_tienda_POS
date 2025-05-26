import flet as ft
from backend.servicios import iva_service
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Iva import Iva

def config_empresa_view(page: ft.Page):

    # Cargar configuración empresa (si existe)
    config = Config_Empresa.obtener_config_empresa()
    if config is None:
        config = Config_Empresa("", "", "", "", "")

    # Inputs para empresa
    nombre_input = ft.TextField(label="Nombre empresa", value=config.nombre, disabled=True)
    direccion_input = ft.TextField(label="Dirección", value=config.direccion, disabled=True)
    telefono_input = ft.TextField(label="Teléfono", value=config.telefono, disabled=True)
    moneda_input = ft.TextField(label="Moneda", value=config.moneda, disabled=True)

    # Botones para editar y guardar empresa
    editar_btn = ft.ElevatedButton("Editar datos")
    guardar_btn = ft.ElevatedButton("Guardar datos", disabled=True)

    def on_editar_click(e):
        # Habilita inputs para editar
        nombre_input.disabled = False
        direccion_input.disabled = False
        telefono_input.disabled = False
        moneda_input.disabled = False
        guardar_btn.disabled = False
        editar_btn.disabled = True
        page.update()

    def on_guardar_click(e):
        # Guardar datos empresa en base
        nueva_config = Config_Empresa(
            empresa_id="config1",  # fija un id para la config única
            nombre=nombre_input.value,
            direccion=direccion_input.value,
            telefono=telefono_input.value,
            moneda=moneda_input.value
        )
        Config_Empresa.guardar_config_empresa(nueva_config)
        # Deshabilitar inputs
        nombre_input.disabled = True
        direccion_input.disabled = True
        telefono_input.disabled = True
        moneda_input.disabled = True
        guardar_btn.disabled = True
        editar_btn.disabled = False
        page.update()

    editar_btn.on_click = on_editar_click
    guardar_btn.on_click = on_guardar_click

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
# usamoa UUID para generar nuestro id de iva unico
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

    iva_service.inicializar_iva()
    cargar_ivas()

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
            ivalist_view
        ]
    )
