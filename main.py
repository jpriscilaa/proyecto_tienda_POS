import flet as ft
from app.router import route_app

def main(page: ft.Page):
    comprobarConfiguracion()
    route_app(page)

def comprobarConfiguracion():
    ha_sido_inicializado()


def ha_sido_inicializado():
    # Aquí puedes agregar la lógica para verificar si la aplicación ha sido inicializada
    # Por ejemplo, podrías verificar si un archivo de configuración existe o si una base de datos está disponible
    print("Verificando configuración...BD...infoPantalla...datosDeLaEmpresa")  # Placeholder para la lógica de verificación
    # Si no ha sido inicializado, puedes redirigir a una página de configuración o mostrar un mensaje
    # page.go("/configuracion")  # Descomentar y ajustar según sea necesario

if __name__ == "__main__":
    ft.app(target=main)
