import flet as ft
from backend import Constantes
import logging
logger=logging.getLogger(__name__)

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

def finalizar_venta(page):
    def guardar_venta(e):
        logger.info("FINALIZAMOS VENTA")
        pass
    def borrar_venta(e):
        page.close(fin_venta)
        logger.info("CANCELAMOS VENTA")
        
        pass

    action_sheet = ft.CupertinoActionSheet(
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
                on_click=guardar_venta,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("EFECTIVO"),
                on_click=guardar_venta,
            )
        ],
    )
    fin_venta=ft.CupertinoBottomSheet(action_sheet)
    return fin_venta
