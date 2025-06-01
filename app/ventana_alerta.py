import flet as ft

def alerta_login():

    dialogo = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("Usuario o contraseña incorrectas"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )
    return dialogo