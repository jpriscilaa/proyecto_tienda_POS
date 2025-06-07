import flet as ft
from backend import Constantes

def alerta_login():
    dialogo=ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("Usuario o contraseña incorrectas"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )
    return dialogo

def alerta_error(titulo, texto):
    dialogo=ft.AlertDialog(
        title=ft.Text("Error "+titulo),
        content=ft.Text(texto),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25)
    )
    return dialogo

def barra_error_mensaje(texto):
    barra=ft.SnackBar(ft.Text(texto), bgcolor=Constantes.COLOR_BOTON_ERROR)
    return barra

def barra_ok_mensaje(texto):
    barra=ft.SnackBar(ft.Text(texto), bgcolor=Constantes.COLOR_BOTON_EXITO)
    return barra

def barra_info_mensaje(texto):
    barra=ft.SnackBar(ft.Text(texto), bgcolor=Constantes.COLOR_BORDE_CLARO)
    return barra
