import flet as ft

from backend.modelo import Usuario

def usuario_view(page: ft.Page):
	nombre_usuario = ft.TextField(label="Nombre de usuario", autofocus=True, width=300)
	contrasena_usuario = ft.TextField(label="Contraseña", password=True, width=300)
	rol_usuario = ft.Dropdown(
		label="Rol de usuario",
		options=[
			ft.dropdown.Option("Administrador"),
			ft.dropdown.Option("Vendedor")		
			],
		width=300
	)

	def crear_usuario(e):
		usuario = Usuario (
			nombre=nombre_usuario.value,
			contrasena=contrasena_usuario.value,
			rol=rol_usuario.value
		)
		# Aquí iría la lógica para crear un usuario
		print(f"Usuario creado: {nombre_usuario.value}, Rol: {rol_usuario.value}")
		nombre_usuario.value = ""
		contrasena_usuario.value = ""
		rol_usuario.value = None
		page.update()

	pass

