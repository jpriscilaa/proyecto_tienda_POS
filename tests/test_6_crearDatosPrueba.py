from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva
from backend.modelo.Producto import Producto
import random

#PARA LANZAR ESTE TEST LANZAMOS POR TERMINAL ESTE COMANDO:
#python -m tests.test_6_crearDatosPrueba

def poblar_ivas_espana():
    print("Insertando IVAs de España...")
    ivas = [
        {"nombre": "General", "porcentaje": 21},
        {"nombre": "Reducido", "porcentaje": 10},
        {"nombre": "Superreducido", "porcentaje": 4},
        {"nombre": "Exento", "porcentaje": 0},
    ]
    for iva in ivas:
        i = Iva(nombre=iva["nombre"], porcentaje=iva["porcentaje"])
        i.guardar()
    print("IVAs insertados correctamente.")

def poblar_categorias():
    print("Insertando categorías de ejemplo...")
    categorias = [
        "BEBIDAS", "LÁCTEOS", "CARNES", "FRUTAS", "VERDURAS", "PANADERÍA", "SNACKS", "CEREALES", "LEGUMBRES",
        "CONSERVAS", "CONGELADOS", "LIMPIEZA", "HIGIENE", "PAPELERÍA", "JUGUETERÍA", "TEXTIL", "FERRETERÍA",
        "ELECTRÓNICA", "DECORACIÓN", "JARDINERÍA", "HOGAR", "MENAJE", "COCINA", "ILUMINACIÓN"
    ]
    for nombre in categorias:
        c = Categoria(nombre=nombre)
        c.guardar()
    print("Categorías insertadas correctamente.")

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
        print("Primero debes generar categorías e IVAs.")
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

    print(f"Se han generado {len(productos)} productos.")


if __name__ == "__main__":
    poblar_ivas_espana()
    poblar_categorias()
    generar_productos_masivos()