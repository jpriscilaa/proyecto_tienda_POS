import flet as ft
#importando las librerias necesarias
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Iva import Iva
from backend.modelo.Config_Empresa import (crear_tabla_config_empresa,obtener_config_empresa,guardar_config_empresa)

from backend.servicios.config_empr_service import guardar_datos_empresa
from backend.servicios.iva_service import (
    listar_ivas,
    crear_tabla_iva,
    agregar_iva
)

from backend.servicios.categoria_service import (
    crear_categoria)

#creando las tablas necesarias si no existen
crear_tabla_config_empresa()
crear_tabla_iva()



def config_empresa_view(page: ft.Page):
    # introducir informacion de la empresa
    nombre_input = ft.TextField(label="Nombre de la empresa")
    direccion_input = ft.TextField(label="Dirección")
    telefono_input = ft.TextField(label="Teléfono")
    moneda_input = ft.TextField(label="Moneda")
    iva_dropdown = ft.Dropdown(label="IVA")
    

    #introducir informacion de iva
    nombre_iva_input = ft.TextField(label="Nombre IVA")
    porcentaje_input = ft.TextField(label="Porcentaje")
    

    #introducir informacion de categoria   
    nombre_categoria_input = ft.TextField(label="Nombre de la categoría")
    id_categoria_input = ft.TextField(label="ID de la categoría")

    #cargamos las opciones de iva
    def cargar_iva_options():
        iva_dropdown.options = [
            ft.dropdown.Option(iva.iva_id, f"{iva.nombre} ({iva.porcentaje}%)")
            for iva in listar_ivas()
        ]
        page.update()
    #guardamos la informacion de iva
    def guardar_iva(e):
        print("guardando iva")
        try:
            nombre = nombre_iva_input.value
            porcentaje = float(porcentaje_input.value)
            nuevo_id = "iva_" + nombre.lower().replace(" ", "_")[:6]
            nuevo_iva = Iva(iva_id=nuevo_id, nombre=nombre, porcentaje=porcentaje)

            print("leyendo datos")
            agregar_iva(nuevo_iva)
            print("se guardo el iva")
            cargar_iva_options()
            page.snack_bar = ft.SnackBar(ft.Text("IVA agregado correctamente"))
            page.snack_bar.open = True
            nombre_iva_input.value = ""
            porcentaje_input.value = ""
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar IVA: {ex}"))
            page.snack_bar.open = True
            page.update()
    #guardamos la informacion de categoria
    def guardar_categoria(e):
        try:
            nombre = nombre_categoria_input.value
            id_categoria = id_categoria_input.value
            crear_categoria(id_categoria, nombre)
            page.snack_bar = ft.SnackBar(ft.Text("Categoría agregada correctamente"))
            page.snack_bar.open = True
            nombre_categoria_input.value = ""
            id_categoria_input.value = ""
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar categoría: {ex}"))
            page.snack_bar.open = True
            page.update()

    #cargamos los datos de la empresa
    def cargar_datos_empresa():
        datos = obtener_config_empresa()
        if datos:
            nombre_input.value = datos["nombre"]
            direccion_input.value = datos["direccion"]
            telefono_input.value = datos["telefono"]
            moneda_input.value = datos["moneda"]
            iva_dropdown.value = datos["iva_id"]
        page.update()

    
    

    def guardar_click(e):
        try:
            iva_obj = Iva(iva_id=iva_dropdown.value, nombre="", porcentaje=0)  # Solo necesitas el id aquí
            config = Config_Empresa(
                empresa_id="empresa_001",
                nombre=nombre_input.value,
                direccion=direccion_input.value,
                telefono=telefono_input.value,
                iva=iva_obj,
                moneda=moneda_input.value
            )
            guardar_datos_empresa(config)
            page.snack_bar = ft.SnackBar(ft.Text("Configuración guardada correctamente."))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    cargar_iva_options()
    cargar_datos_empresa()

    return ft.Column(
        scroll="auto",  
        expand=True,
        controls=[
            ft.Text("Configuración de la Empresa", size=25, weight="bold"),
            nombre_input,
            direccion_input,
            telefono_input,
            moneda_input,
            ft.Row([iva_dropdown]),
            ft.ElevatedButton("Guardar configuración", on_click=guardar_click),

            # Contenedor para agregar IVA
            ft.Container(
                content=ft.Column([
                    ft.Text("Agregar nuevo IVA", weight="bold", bgcolor="black"),
                    nombre_iva_input,
                    porcentaje_input,
                    ft.ElevatedButton("Guardar IVA", on_click=guardar_iva),
                ]),
                bgcolor=ft.Colors.BLUE_50,
                padding=10,
                border_radius=10,
                margin=10
            ),

            # Contenedor para agregar categoría
            ft.Container(
                content=ft.Column([
                    ft.Text("Agregar nueva Categoría", weight="bold"),
                    id_categoria_input,
                    nombre_categoria_input,
                    ft.ElevatedButton("Guardar Categoría", on_click=guardar_categoria),
                ]),
                bgcolor=ft.Colors.GREEN_50,
                padding=10,
                border_radius=10,
                margin=10
            ),

            ft.ElevatedButton("Volver", on_click=lambda e: page.go("/dashboard")),
        ]
    )