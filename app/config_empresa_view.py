import flet as ft
from backend import Constantes
from backend.servicios import config_empr_service, iva_service
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Iva import Iva
from backend.servicios.categoria_service import listar_categorias, guardar_categoria
from backend.modelo.Categoria import Categoria
import random
import uuid
from backend.Constantes import NOMBRE_APP

def config_empresa_view(page: ft.Page):
    empresa = Config_Empresa.obtener_config_empresa()
    nombre_empresa = ft.TextField(label="Nombre empresa",value=empresa.nombre,border=ft.InputBorder.UNDERLINE,border_radius=9,disabled=True)
    direccion_empresa = ft.TextField(label="Dirección empresa",value=empresa.direccion,border=ft.InputBorder.UNDERLINE,border_radius=9,disabled=True)
    telefono_empresa = ft.TextField(label="Teléfono empresa",value=empresa.telefono,border=ft.InputBorder.UNDERLINE,border_radius=9,disabled=True)
    moneda = ft.Dropdown(label="Moneda",border=ft.InputBorder.UNDERLINE,border_radius=9,disabled=True,value=empresa.moneda,options=[    ft.dropdown.Option("EUR€"),    ft.dropdown.Option("DOLR$")])
    categoria_nombre_input = ft.TextField(label="Nombre Categoría")

# Apartado Configuración de emresa

    def habilitar_edicion(e):
        nombre_empresa.disabled = False
        direccion_empresa.disabled = False
        telefono_empresa.disabled = False
        moneda.disabled = False
        page.update()

    def guardar_empresa(e):
        empresa_actualizada = Config_Empresa(
            empresa_id=1,
            nombre=nombre_empresa.value,
            direccion=direccion_empresa.value,
            telefono=telefono_empresa.value,
            moneda=moneda.value
        )
        empresa_actualizada.guardar()
        nombre_empresa.disabled = True
        direccion_empresa.disabled = True
        telefono_empresa.disabled = True
        moneda.disabled = True
        page.update()


    page.title = "Configuración Empresa"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = Constantes.COLOR_FONDO_PRINCIPAL

    btn_editar = ft.ElevatedButton(text="Editar", on_click=habilitar_edicion)
    btn_guardar = ft.ElevatedButton(text="Guardar", on_click=guardar_empresa)

    #Apartado Categorías
    def guardar_categoria(e):
        cat = Categoria(nombre=categoria_nombre_input.value)
        cat.guardar()
        categoria_nombre_input.value = ""
        page.update()


    

    formulario = ft.Column([
        nombre_empresa,
        direccion_empresa,
        telefono_empresa,
        moneda,
        ft.Row([btn_editar, btn_guardar], alignment=ft.MainAxisAlignment.CENTER),
        # --- Categoría ---
        ft.Text("Gestión de Categorías", size=18, weight="bold"),
        categoria_nombre_input,
        ft.Row([
            ft.ElevatedButton("Guardar Categoría", on_click=guardar_categoria)
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=30, color="transparent"),
    ], spacing=15)


    contenedor = ft.Container(
        expand=False,
        alignment=ft.alignment.center,
        content=formulario,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    return contenedor
