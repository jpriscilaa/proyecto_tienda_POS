import flet as ft
from backend import Constantes
from backend.servicios import config_empr_service

def iniciar_app(page: ft.Page):

    
    page.title = "Primera configuración"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = Constantes.COLOR_FONDO_PRINCIPAL
    empresa = ["Tienda Mari", "Villarrobledo"]
    
    #Creo una lista donde iran todos los elementos, luego si lo guardo en un column se pone en modo vertial, si lo guardo en row se guarda en horizontal
    form_controls = [
        ft.TextField(border=ft.InputBorder.UNDERLINE, label="Nombre empresa", border_radius=9),
        ft.TextField(border=ft.InputBorder.UNDERLINE, label="Nombre usuario", border_radius=9),
        ft.TextField(border=ft.InputBorder.UNDERLINE, label="Contraseña usuario", border_radius=9, password=True, can_reveal_password=True),
        ft.Dropdown(border=ft.InputBorder.UNDERLINE, border_radius=9, label="País", options=[
            ft.dropdown.Option("México"),
            ft.dropdown.Option("Argentina"),
            ft.dropdown.Option("España")
        ]),
        ft.TextField(border=ft.InputBorder.UNDERLINE, label="Dirección empresa", border_radius=9),
        ft.TextField(border=ft.InputBorder.UNDERLINE,label="Teléfono empresa", border_radius=9),
        ft.Dropdown(border=ft.InputBorder.UNDERLINE, border_radius=9, label="Moneda", options=[
            ft.dropdown.Option("EUR€"),
            ft.dropdown.Option("DOLR$")
        ]),
        ft.ElevatedButton(text="Guardar", width=180, height=50, on_click=lambda e: guardarEmpresa())
    ]

    columna_campos = ft.Column(form_controls)

    contenedor = ft.Container(
        expand=False,
        alignment=ft.alignment.center,
        content=columna_campos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    
    return contenedor

def guardarEmpresa():
    empresa = []
    config_empr_service.crearEmpresa(empresa)
    print("Se ha guardado empresa: ")
