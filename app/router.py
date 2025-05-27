from app.clientes_view import clientes_view
from .login_view import login_view
from .dashboard_view import dashboard_view
from .config_empresa_view import config_empresa_view  # si ya lo tienes
from app.producto_view import producto_view
from .tpv_view import venta_line_view  # Asegúrate de importar la vista de TPV

def route_app(page):
    page.bgcolor = "#FFFFFF"  # Cambia el color de fondo de toda la ventana
    page.title = "Tienda"

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(login_view(page))
        elif page.route == "/dashboard":
            page.views.append(dashboard_view(page))
        elif page.route == "/productos":
            page.views.append(producto_view(page))
        elif page.route == "/config":
            page.views.append(config_empresa_view(page))
        elif page.route == "/clientes":
            page.views.append(clientes_view(page))  # Asegúrate de importar clientes_view
        elif page.route == "/venta_line":
            page.views.append(venta_line_view(page))  # Asegúrate de importar venta_line_view
        else:
            page.views.append(login_view(page))  # fallback

        page.update()

    page.on_route_change = route_change
    page.go(page.route)
