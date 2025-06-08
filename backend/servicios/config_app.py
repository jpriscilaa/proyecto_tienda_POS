import os
from backend import Constantes
import sqlite3
from datetime import datetime, timedelta
from backend.modelo.Categoria import Categoria
from backend.modelo.Cliente import Cliente
from backend.modelo.Iva import Iva
from backend.modelo.Producto import Producto
from backend.modelo.Venta import Venta
import random
import logging
log=logging.getLogger(__name__)

def ruta_ejecucion():
    return os.getcwd()

def crearSQLITE():
    #Crear la ruta de la bd agregando la carpeta conf y bd, uso os.path para que funciona bien en todos los sistemas operativos
    rutaSQLITE=os.path.join(ruta_ejecucion(), Constantes.RUTA_BD)

    log.info("------------------------------------------")
    log.info("La ruta de la BD es: " + rutaSQLITE)
    log.info("------------------------------------------")
    if not os.path.exists(rutaSQLITE):
        conexion=sqlite3.connect(rutaSQLITE)
        cursor=conexion.cursor()

        crearTabla(cursor)

        conexion.commit()
        conexion.close()
        crear_ivas_espana()
        log.info(f"Base de datos '{rutaSQLITE}' creada con éxito.")
        return True
    else:
        log.info(f"La base de datos '{rutaSQLITE}' ya existe.")

        return False
        

def crearTabla(cursor):
        #Cramos las tablas necesarias
        cursor.execute(Constantes.CREATE_TABLA_CATEGORIA)
        cursor.execute(Constantes.CREATE_TABLA_CLIENTE)
        cursor.execute(Constantes.CREATE_TABLA_CONFIGURACION_APP)
        cursor.execute(Constantes.CREATE_TABLA_IVA)
        cursor.execute(Constantes.CREATE_TABLA_PRODUCTO)
        cursor.execute(Constantes.CREATE_TABLA_VENTA)
        cursor.execute(Constantes.CREATE_TABLA_VENTA_LINEA)
        cursor.execute(Constantes.CREATE_TABLA_USUARIO)

def crear_ivas_espana():
    log.info("Insertando IVAs de España...")
    ivas = [
        {"nombre": "General", "porcentaje": 21},
        {"nombre": "Reducido", "porcentaje": 10},
        {"nombre": "Superreducido", "porcentaje": 4},
        {"nombre": "Exento", "porcentaje": 0},
    ]
    for iva in ivas:
        i = Iva(nombre=iva["nombre"], porcentaje=iva["porcentaje"])
        i.guardar()
    log.info("IVAs insertados correctamente.")

def crear_categorias():
    log.info("Insertando categorías de ejemplo...")
    categorias = [
        "BEBIDAS", "LÁCTEOS", "CARNES", "FRUTAS", "VERDURAS", "PANADERÍA", "SNACKS", "CEREALES", "LEGUMBRES",
        "CONSERVAS", "CONGELADOS", "LIMPIEZA", "HIGIENE", "PAPELERÍA", "JUGUETERÍA", "TEXTIL", "FERRETERÍA",
        "ELECTRÓNICA", "DECORACIÓN", "JARDINERÍA", "HOGAR", "MENAJE", "COCINA", "ILUMINACIÓN"
    ]
    for nombre in categorias:
        c = Categoria(nombre=nombre)
        c.guardar()
    log.info("Categorías insertadas correctamente.")

def generar_productos_masivos():
    productos = [
        "Leche entera", "Leche desnatada", "Pan de molde", "Pan integral", "Aceite de oliva", "Aceite de girasol",
        "Azúcar blanca", "Azúcar morena", "Sal fina", "Sal marina", "Arroz blanco", "Arroz integral",
        "Fideos gruesos", "Espaguetis", "Lentejas pardinas", "Garbanzos cocidos", "Judías blancas", "Maíz dulce",
        "Atún en lata", "Sardinas en aceite", "Huevos camperos", "Huevos ecológicos", "Mantequilla sin sal",
        "Margarina vegetal", "Queso rallado", "Queso en lonchas", "Yogur natural", "Yogur de fresa",
        "Jamón cocido", "Jamón serrano", "Pechuga de pollo", "Carne picada", "Manzanas rojas", "Manzanas verdes",
        "Plátanos maduros", "Peras conferencia", "Naranjas de zumo", "Mandarinas dulces", "Uvas blancas",
        "Zanahorias frescas", "Tomates pera", "Cebollas dulces", "Pimientos rojos", "Calabacines tiernos",
        "Lechuga romana", "Espinacas frescas", "Patatas nuevas", "Champiñones", "Brócoli fresco",
        "Coliflor blanca", "Vela aromática", "Cuchillo de cocina", "Tijeras multiusos", "Jarra medidora", "Tabla de cortar",
        "Rallador de queso", "Batidor manual", "Abrelatas", "Colador de acero", "Cepillo para verduras",
        "Guantes de limpieza", "Bayeta multiusos", "Esponjas de cocina", "Estropajo metálico", "Cubo de basura",
        "Bolsas de basura", "Cinta adhesiva", "Pegamento universal", "Pilas AA", "Pilas AAA",
        "Bombilla LED", "Lámpara de escritorio", "Regleta eléctrica", "Alargador 3 metros", "Destornillador plano",
        "Destornillador estrella", "Martillo pequeño", "Llave inglesa", "Tornillos variados", "Clavos pequeños",
        "Caja de herramientas", "Linterna portátil", "Paraguas compacto", "Mochila escolar", "Cuaderno de notas",
        "Bolígrafos azules", "Lápices de grafito", "Goma de borrar", "Sacapuntas metálico", "Regla de 30 cm",
        "Tijeras escolares", "Pegamento en barra", "Rotuladores de colores", "Carpeta de anillas", "Archivador A4",
        "Fundas plásticas", "Grapadora pequeña", "Cinta correctora", "Notas adhesivas", "Bloc de notas"
    ]

    categorias = Categoria.obtener_todos()
    ivas = Iva.obtener_todos()

    if not categorias or not ivas:
        log.info("Primero debes generar categorías e IVAs.")
        return

    for i, nombre in enumerate(productos):
        categoria = random.choice(categorias)
        iva = random.choice(ivas)
        precio = round(random.uniform(0.5, 50.0), 2)
        referencia = f"REF-{i+1:04d}"
        producto = Producto(
            precio=precio,
            nombre=nombre,
            n_referencia=referencia,
            categoria=categoria,
            iva=iva
        )
        producto.guardar()

    log.info(f"Se han generado {len(productos)} productos.")

def generar_clientes():
        log.info("Creando clientes de prueba...")
        nombres = ["Ana", "Luis", "Carlos", "Laura", "Elena", "Pedro", "Lucía", "Javier", "María", "Andrés"]
        apellidos = ["Pérez", "Gómez", "López", "Martínez", "Sánchez", "Díaz", "Fernández", "Ruiz", "Torres", "Castillo"]
        clientes = []

        for i in range(10):
            cliente = Cliente(
                cliente_nombre=random.choice(nombres),
                cliente_apellido=random.choice(apellidos),
                cliente_documento=f"{random.randint(10000000,99999999)}X",
                cliente_telefono=f"6{random.randint(10000000, 99999999)}",
                cliente_direccion=f"Calle Falsa {i+1}"
            )
            if cliente.guardar():
                clientes.append(cliente)
                log.info(f"✅ Cliente {cliente.nombre} {cliente.apellido} creado.")
            else:
                log.info(f"❌ Error al guardar cliente {cliente.nombre}")
        return clientes

def generar_ventas():
    log.info("Generando ventas de prueba...")
    tipos_pago = ["EFECTIVO", "TARJETA", "BIZUM", "TRANSFERENCIA"]
    clientes=Cliente.obtener_todos()
    for cliente in clientes:
        num_ventas = random.randint(1, 3)  # 1 a 3 ventas por cliente
        for _ in range(num_ventas):
            fecha = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            pago = random.choice(tipos_pago)
            cantidad = random.randint(1, 10)
            total = round(random.uniform(5.0, 200.0), 2)
            venta = Venta(
                fecha=fecha,
                pago=pago,
                cliente=cliente,
                cantidad_prod=str(cantidad),
                total=total
            )
            if venta.guardar():
                log.info(f"Venta de {total}€ guardada para {cliente.nombre} ({pago})")
            else:
                log.info(f"Error al guardar venta para {cliente.nombre}")

if __name__ == "__main__":
     pass
     