from .login_view import login_view
from .dashboard_view import dashboard_view
from .config_empresa_view import config_empresa_view  # si ya lo tienes

def route_app(page):
    page.bgcolor = "#FFFFFF"  # Cambia el color de fondo de toda la ventana
    page.title = "Tienda"

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(login_view(page))
        elif page.route == "/dashboard":
            page.views.append(dashboard_view(page))
        #elif page.route == "/productos":
            #page.views.append(producto_view(page))
        elif page.route == "/config_empr":
            page.views.append(config_empresa_view(page))
        else:
            page.views.append(login_view(page))  # fallback

        page.update()

    page.on_route_change = route_change
    page.go(page.route)
