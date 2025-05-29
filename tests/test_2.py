from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Modelos
class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    productos = relationship("Producto", back_populates="categoria")

class Precio(Base):
    __tablename__ = 'precios'
    id = Column(Integer, primary_key=True)
    valor = Column(Float, nullable=False)
    impuesto = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    producto = relationship("Producto", back_populates="precio", uselist=False)

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio_id = Column(Integer, ForeignKey('precios.id'))
    categoria_id = Column(Integer, ForeignKey('categorias.id'))

    precio = relationship("Precio", back_populates="producto")
    categoria = relationship("Categoria", back_populates="productos")

# Configuración DB
engine = create_engine('sqlite:///productos.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Funciones CRUD
def crear_producto(nombre, precio, impuesto, categoria_id):
    session = Session()
    total = precio + impuesto
    nuevo_precio = Precio(valor=precio, impuesto=impuesto, total=total)
    session.add(nuevo_precio)
    session.commit()

    nuevo_producto = Producto(nombre=nombre, precio_id=nuevo_precio.id, categoria_id=categoria_id)
    session.add(nuevo_producto)
    session.commit()
    session.close()

def listar_productos():
    session = Session()
    productos = session.query(Producto).all()
    for p in productos:
        print(f"Producto: {p.nombre}, Precio: {p.precio.total}, Categoría: {p.categoria.nombre}")
    session.close()

def eliminar_producto(id_producto):
    session = Session()
    producto = session.query(Producto).get(id_producto)
    if producto:
        session.delete(producto)
        session.commit()
    session.close()

def crear_categoria(nombre, descripcion):
    session = Session()
    categoria = Categoria(nombre=nombre, descripcion=descripcion)
    session.add(categoria)
    session.commit()
    session.close()