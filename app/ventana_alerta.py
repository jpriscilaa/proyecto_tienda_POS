import flet as ft
from backend import Constantes
from backend.servicios import config_app
import logging
log=logging.getLogger(__name__)

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

def finalizar_venta(page: ft.Page, metodo: ft.Text, on_finalizar):
    def metodo_efectivo(e):
        metodo.value="EFECTIVO"
        log.info("METODO SELECCIONADO ES EFECTIVO")
        page.close(fin_venta)
        on_finalizar()

    def metodo_tarjeta(e):
        metodo.value="TARJETA"
        log.info("METODO SELECCIONADO ES TARJETA")
        page.close(fin_venta)
        on_finalizar()

    def borrar_venta(e):
        page.close(fin_venta)
        log.info("CANCELAMOS VENTA")

    action_sheet=ft.CupertinoActionSheet(
        title=ft.Row(
            [ft.Text("Completar venta"), ft.Icon(ft.Icons.DONE_OUTLINE)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        message=ft.Row(
            [ft.Text("Seleccione método de pago"), ft.Icon(ft.Icons.PAYMENT)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        cancel=ft.CupertinoActionSheetAction(
            content=ft.Text("CANCELAR"),
            on_click=borrar_venta,
        ),
        actions=[
            ft.CupertinoActionSheetAction(
                content=ft.Text("TARJETA"),
                is_default_action=True,
                on_click=metodo_tarjeta,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("EFECTIVO"),
                on_click=metodo_efectivo,
            )
        ],
    )
    fin_venta=ft.CupertinoBottomSheet(action_sheet)
    return fin_venta


def confirmar_accion(page: ft.Page, titulo, mensaje):
    def cerrar_dialogo(e):
        dialogo.open=False
        page.update()

    def accion_si(e):
        cerrar_dialogo(e)
        config_app.crear_categorias()
        config_app.generar_productos_masivos()
        config_app.generar_clientes()
        config_app.generar_ventas()
        log.info("Se han creado datos de prueba")
        page.update()

    def accion_no(e):
        cerrar_dialogo(e)

    dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text(titulo),
        content=ft.Text(mensaje),
        actions=[
            ft.TextButton("No", on_click=accion_no),
            ft.ElevatedButton("Sí", on_click=accion_si),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dialogo.open=True
    page.open(dialogo)
    page.update()