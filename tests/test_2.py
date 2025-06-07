import flet as ft

def main(page: ft.Page):

    def validar_campo(e):
        if not campo.value.strip():
            campo.error_text = "Este campo es obligatorio"
        else:
            campo.error_text = None
        page.update()

    campo = ft.TextField(
        label="Nombre",
        hint_text="Ingresa tu nombre",
        on_blur=validar_campo
    )

    page.add(campo)

ft.app(target=main)