import flet as ft
from backend.modelo.Config_Empresa import Config_Empresa


def config_empresa_view(page: ft.Page):
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

    iva_container = ft.Container(content=ft.Text("Gestión de tipos de IVA aquí"))

    return ft.View(
        route="/config",
        controls=[
            ft.Column([
                nombre_input,
                direccion_input,
                telefono_input,
                moneda_input,
                ft.Row([editar_btn, guardar_btn]),
                iva_container
            ])
        ]
    )