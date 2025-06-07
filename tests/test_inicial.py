import sys
import os
from backend.servicios import producto_service
from backend.modelo.Categoria import Categoria

def test1 ():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from backend.modelo.Producto import Producto

    from backend.bddTienda import get_connection
    from backend.modelo.Categoria import Categoria
    from backend.modelo.Iva import Iva
    from backend.servicios.categoria_service import listar_categorias
    from backend.servicios.producto_service import  crear_producto, listar_productos
    crear_producto(Producto("0","12345","coca",1.50,Categoria("1","bebidas"),Iva("1","general",21)))
    productos=listar_productos()
    print(productos[0])

def test2():
    pass

def test3():
    #crear categorias
    categoria1=Categoria(
        nombre="Bebidas",
    )
    categoria1.guardar()

    categoria2=Categoria(
    nombre="Comida",
    )
    categoria2.guardar()

    listaDeCats=Categoria.obtener_todos()
    print(len(listaDeCats))
    for cat in listaDeCats:
        print(cat.nombre)

def main():
    # Código principal
    print("Hola desde Python")

if __name__ == "__main__":
    main()