import sqlite3
import uuid
import json
from backend import Constantes
from backend.bddTienda import get_connection
from backend.modelo.Categoria import Categoria
from backend.modelo.Iva import Iva

class Producto:
    def __init__(self, precio, nombre, n_referencia, categoria: Categoria, iva: Iva, id=None):
        self.id=id or str(uuid.uuid4())
        self.n_referencia=n_referencia
        self.nombre=nombre.upper()
        self.precio=float(str(precio).replace(",", ".")) if precio else 0.0
        self.categoria=categoria
        self.iva=iva

    def guardar(self):
        try:
            conexion=sqlite3.connect(Constantes.RUTA_BD)
            cursor=conexion.cursor()

            if Producto.existe(self.id):
                cursor.execute(Constantes.UPDATE_PRODUCTO, (self.n_referencia, self.nombre, self.precio, self.categoria.categoria_id, self.iva.iva_id, self.id))
            else:
                cursor.execute(Constantes.INSERT_PRODUCTO, (self.id, self.n_referencia, self.nombre, self.precio, self.categoria.categoria_id, self.iva.iva_id))

            conexion.commit()
            conexion.close()
            return True
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: PRODUCTO.N_REFERENCIA" in str(error):
                print("Ya existe un producto con esa referencia o codigo de barras.")
                return False 
            elif "FOREIGN KEY constraint failed" in str(error):
                print("Error con la CATEGORIA o el IVA seleccionado no existen.")
                return False
        except Exception as e:
            print("Ha dado algún error en el insert del producto" + str(e))
            return False

    def eliminar(self):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM PRODUCTO WHERE PRODUCTO_ID=?", (self.id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(producto_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT PRODUCTO_ID, N_REFERENCIA, NOMBRE, PRECIO, CATEGORIA_ID, IVA_ID FROM PRODUCTO WHERE PRODUCTO_ID=?", (producto_id,))
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            prod_id=fila[0]
            n_ref=fila[1]
            nombre=fila[2]
            precio=fila[3]
            categoria_id=fila[4]
            iva_id=fila[5]

            #Buscar las instancias de Categoria e Iva
            categoria=Categoria.buscar_por_id(categoria_id)
            iva=Iva.buscar_por_id(iva_id)

            return Producto(
                precio=precio,
                nombre=nombre,
                n_referencia=n_ref,
                categoria=categoria,
                iva=iva,
                id=prod_id
            )
        else:
            return None
        
    @staticmethod
    def buscar_por_referencia(n_referencia):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute(
            "SELECT PRODUCTO_ID, N_REFERENCIA, NOMBRE, PRECIO, CATEGORIA_ID, IVA_ID FROM PRODUCTO WHERE N_REFERENCIA=?",
            (n_referencia,))
        fila=cursor.fetchone()
        conexion.close()

        if fila:
            prod_id=fila[0]
            n_ref=fila[1]
            nombre=fila[2]
            precio=fila[3]
            categoria_id=fila[4]
            iva_id=fila[5]

            # Buscar las instancias de Categoria e Iva
            categoria=Categoria.buscar_por_id(categoria_id)
            iva=Iva.buscar_por_id(iva_id)

            return Producto(
                precio=precio,
                nombre=nombre,
                n_referencia=n_ref,
                categoria=categoria,
                iva=iva,
                id=prod_id
            )
        else:
            return None

    @staticmethod
    def existe(producto_id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT 1 FROM PRODUCTO WHERE PRODUCTO_ID=?", (producto_id,))
        resultado=cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    @classmethod
    def borrar_por_id(cls, id):
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute('''DELETE FROM PRODUCTO WHERE PRODUCTO_ID=?''', (id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_todos():
        conexion=sqlite3.connect(Constantes.RUTA_BD)
        cursor=conexion.cursor()
        cursor.execute("SELECT * FROM PRODUCTO")
        filas=cursor.fetchall()
        conexion.close()

        productos=[]
        for fila in filas:
            prod_id=fila[0]
            n_ref=fila[1]
            nombre=fila[2]
            precio=fila[3]
            categoria_id=fila[4]
            iva_id=fila[5]

            # Obtener instancias completas de Categoria e Iva (suponiendo que tenés estos métodos)
            categoria=Categoria.buscar_por_id(categoria_id)
            iva=Iva.buscar_por_id(iva_id)

            producto=Producto(
                precio=precio,
                nombre=nombre,
                n_referencia=n_ref,
                categoria=categoria,
                iva=iva,
                id=prod_id
            )

            productos.append(producto)

        return productos
    
    #Metodo que devuelve el json para poder pintar en cualquier logger texto
    def __str__(self):
        return json.dumps({
            "id": self.id,
            "nombre": self.nombre,
            "referencia": self.n_referencia,
            "precio": self.precio,
            "categoria": self.categoria.nombre if self.categoria else None,
            "iva": self.iva.porcentaje if self.iva else None
        })