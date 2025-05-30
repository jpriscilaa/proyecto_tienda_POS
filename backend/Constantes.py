#Ruta base de datos SQLite
RUTA_BD = "conf/BD_MI_EMPRESA.DB"
RUTA_CARPETA_CONF = "conf"
#Nombre de la app (por ejemplo, para ventanas o logs)
NOMBRE_APP = "P.O.S TIENDA BY PRIS"

#----------------------------------------
#Paleta de colores estilo macOS (modo claro)
#----------------------------------------
# COLOR_FONDO_PRINCIPAL = "#F2F2F7"       # Fondo general de la app
# COLOR_TARJETA_FONDO = "#FFFFFF"         # Fondo para tarjetas, contenedores
# COLOR_TEXTO_PRIMARIO = "#1C1C1E"        # Texto principal
# COLOR_TEXTO_SECUNDARIO = "#3A3A3C"      # Texto secundario, descripciones
# COLOR_BOTON_PRIMARIO = "#007AFF"        # Azul macOS para botones principales
# COLOR_BOTON_EXITO = "#34C759"           # Verde Apple para éxito o confirmación
# COLOR_BOTON_ERROR = "#FF3B30"           # Rojo Apple para errores
# COLOR_BORDE_CLARO = "#D1D1D6"           # Borde o líneas divisorias sutiles

#----------------------------------------
#Paleta de colores estilo macOS (modo oscuro)
#----------------------------------------
COLOR_FONDO_PRINCIPAL = "#1C1C1E"       # Fondo principal (negro suave)
COLOR_TARJETA_FONDO = "#2C2C2E"         # Tarjetas, modales
COLOR_TEXTO_PRIMARIO = "#FFFFFF"        # Texto principal (blanco)
COLOR_TEXTO_SECUNDARIO = "#A1A1A6"      # Texto secundario, etiquetas
COLOR_BOTON_PRIMARIO = "#0A84FF"        # Azul macOS (botones principales)
COLOR_BOTON_EXITO = "#30D158"           # Verde confirmación
COLOR_BOTON_ERROR = "#FF453A"           # Rojo error
COLOR_BORDE_CLARO = "#3A3A3C"           # Bordes, líneas sutiles

#Tabla CATEGORIA
CREATE_TABLA_CATEGORIA = '''CREATE TABLE CATEGORIA (
    CATEGORIA_ID TEXT PRIMARY KEY UNIQUE NOT NULL,
    NOMBRE       TEXT NOT NULL
);'''

#Tabla CLIENTE
CREATE_TABLA_CLIENTE = '''CREATE TABLE CLIENTE (
    CLIENTE_ID TEXT PRIMARY KEY UNIQUE NOT NULL,
    NOMBRE     TEXT NOT NULL,
    DOCUMENTO  TEXT UNIQUE,
    TELEFONO   TEXT,
    DIRECCION  TEXT
);'''

#Tabla CONFIGURACIÓN APP
CREATE_TABLA_CONFIGURACION_APP = '''CREATE TABLE CONFIG_EMPRESA (
    EMPRESA_ID TEXT PRIMARY KEY UNIQUE NOT NULL,
    NOMBRE     TEXT NOT NULL,
    DIRECCION  TEXT,
    TELEFONO   TEXT,
    MONEDA     TEXT
);'''

#Tabla IVA
CREATE_TABLA_IVA = '''CREATE TABLE IVA (
    IVA_ID     TEXT PRIMARY KEY UNIQUE NOT NULL,
    NOMBRE     TEXT NOT NULL,
    PORCENTAJE REAL NOT NULL
);'''

#Tabla PRODUCTO
CREATE_TABLA_PRODUCTO = '''CREATE TABLE PRODUCTO (
    PRODUCTO_ID  TEXT PRIMARY KEY UNIQUE NOT NULL,
    N_REFERENCIA TEXT UNIQUE,
    NOMBRE       TEXT NOT NULL,
    PRECIO       REAL NOT NULL CHECK (PRECIO >= 0),
    CATEGORIA_ID TEXT NOT NULL,
    IVA_ID       TEXT NOT NULL,
    FOREIGN KEY (CATEGORIA_ID) REFERENCES CATEGORIA (CATEGORIA_ID),
    FOREIGN KEY (IVA_ID) REFERENCES IVA (IVA_ID)
);'''

#Tabla VENTA
CREATE_TABLA_VENTA = '''CREATE TABLE VENTA (
    VENTA_ID           TEXT PRIMARY KEY UNIQUE NOT NULL,
    CLIENTE_ID         TEXT REFERENCES CLIENTE (CLIENTE_ID),
    TOTAL              REAL NOT NULL,
    CANTIDAD_PRODUCTOS INTEGER NOT NULL
);'''

#Tabla LINEA_VENTA (relación VENTA PRODUCTO)
CREATE_TABLA_VENTA_LINEA = '''CREATE TABLE LINEA_VENTA (
    LINEA_ID        TEXT PRIMARY KEY UNIQUE NOT NULL,
    VENTA_ID        TEXT NOT NULL,
    PRODUCTO_ID     TEXT NOT NULL,
    CANTIDAD        INTEGER NOT NULL CHECK (CANTIDAD > 0),
    PRECIO_UNITARIO REAL NOT NULL CHECK (PRECIO_UNITARIO >= 0),
    IVA             REAL NOT NULL,
    TOTAL_LINEA     REAL NOT NULL,
    FOREIGN KEY (VENTA_ID) REFERENCES VENTA (VENTA_ID) ON DELETE CASCADE,
    FOREIGN KEY (PRODUCTO_ID) REFERENCES PRODUCTO (PRODUCTO_ID)
);'''

UPDATE_CONFIG_EMPRESA = '''UPDATE CONFIG_EMPRESA
                SET NOMBRE = ?, DIRECCION = ?, TELEFONO = ?, MONEDA = ?
                WHERE EMPRESA_ID = ?'''

INSERT_CONFIG_EMPRESA = '''INSERT INTO CONFIG_EMPRESA (EMPRESA_ID, NOMBRE, DIRECCION, TELEFONO, MONEDA)
                VALUES (?, ?, ?, ?, ?)'''

