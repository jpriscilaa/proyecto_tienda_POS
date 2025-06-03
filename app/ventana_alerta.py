import flet as ft

def alerta_login():

    dialogo = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("Usuario o contraseña incorrectas"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )
    return dialogo

def alerta_validacion_usuario_existe():
    dialogo = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("Ya existe ese usuario"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25)

    )
    return dialogo

def alerta_validacion_usuario_digitos():
    dialogo = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("Minimo 5 digitos"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25)

    )
    return dialogo