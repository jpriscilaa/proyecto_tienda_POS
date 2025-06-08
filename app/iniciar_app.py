import flet as ft
from backend import Constantes
from backend.servicios import config_empr_service
from backend.modelo.Config_Empresa import Config_Empresa
from backend.modelo.Usuario import Usuario
from app.login_view import login_view
import logging
log=logging.getLogger(__name__)

def iniciar_app(page: ft.Page):

    page.title="Primera configuración"
    page.horizontal_alignment=ft.MainAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.bgcolor=Constantes.COLOR_FONDO_PRINCIPAL

    #Metodos    
    def guardarEmpresa():
        empresa1=Config_Empresa(
            empresa_id=1,
            nombre=nombre_empresa.value,
            direccion=direccion_empresa.value,
            telefono=telefono_empresa.value,
            moneda=moneda.value
        )
        config_empr_service.crearEmpresa(empresa1)

        #creamos usuario admin
        usuarioAdmin1=Usuario(
        nombre_usuario=nombre_usuario.value,
        contrasena=contrasenna_usuario.value,
        rol=rol_usuario.value
        )
        usuarioAdmin1.guardar()
        
        log.info("Se ha guardado empresa y usuario: ")
        
        page.clean()
        page.add(login_view(page))
    
    #componentes
    nombre_empresa=ft.TextField(border=ft.InputBorder.UNDERLINE, label="Nombre empresa", border_radius=9)
    nombre_usuario=ft.TextField(value="admin", border=ft.InputBorder.UNDERLINE, label="Nombre usuario", border_radius=9)
    contrasenna_usuario=ft.TextField(border=ft.InputBorder.UNDERLINE, label="Contraseña usuario", border_radius=9, password=True, can_reveal_password=True)
    rol_usuario=ft.TextField(value="Administrador",border=ft.InputBorder.UNDERLINE, label="Rol del Usuario", border_radius=9, read_only=True)
    pais_combo=ft.Dropdown(border=ft.InputBorder.UNDERLINE, border_radius=9, label="País", options=[
            ft.dropdown.Option("México"),
            ft.dropdown.Option("Argentina"),
            ft.dropdown.Option("España")
        ])
    direccion_empresa=ft.TextField(border=ft.InputBorder.UNDERLINE, label="Dirección empresa", border_radius=9)
    telefono_empresa=ft.TextField(border=ft.InputBorder.UNDERLINE,label="Teléfono empresa", border_radius=9)
    moneda=ft.Dropdown(border=ft.InputBorder.UNDERLINE, border_radius=9, label="Moneda", options=[
            ft.dropdown.Option("EURO"),
            ft.dropdown.Option("DOLAR")
        ])

    #Creo una lista donde iran todos los elementos, luego si lo guardo en un column se pone en modo vertial, si lo guardo en row se guarda en horizontal
    form_controls=[
        nombre_empresa,
        nombre_usuario,
        contrasenna_usuario,
        rol_usuario,
        pais_combo,
        direccion_empresa,
        telefono_empresa,
        moneda,
        ft.ElevatedButton(text="Guardar", width=180, height=50, on_click=lambda e: guardarEmpresa())
    ]

    columna_campos=ft.Column(form_controls)

    contenedor=ft.Container(
        expand=False,
        alignment=ft.alignment.center,
        content=columna_campos,
        bgcolor=Constantes.COLOR_TARJETA_FONDO,
        padding=20,
        border_radius=15
    )

    return contenedor


