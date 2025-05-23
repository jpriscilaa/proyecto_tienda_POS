from backend.modelo.Iva import Iva
from backend.bddTienda import get_connection

class Config_Empresa:
    def __init__(self, empresa_id, nombre,direccion,telefono, iva: Iva, moneda):
        self.empresa_id = empresa_id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.iva_id = iva  
        self.moneda = moneda

    def __str__(self):
        return self.nombre

def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''REPLACE INTO Config_Empresa
               (empresa_id, nombre, direccion, telefono, iva_id, moneda)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (self.empresa_id, self.nombre, self.direccion, self.telefono, self.iva.iva_id, self.moneda)
        )
        conn.commit()
        conn.close()

@classmethod
def crear_tabla(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Config_Empresa (
                empresa_id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                iva_id TEXT NOT NULL,
                moneda TEXT NOT NULL,
                FOREIGN KEY (iva_id) REFERENCES Iva(iva_id)
            )
        ''')
        conn.commit()
        conn.close()

@classmethod
def obtener(cls, empresa_id="empresa_001"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Config_Empresa WHERE empresa_id = ?", (empresa_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            iva_obj = Iva(row[4], "", 0)  # puedes completar los datos con una búsqueda si lo prefieres
            return cls(row[0], row[1], row[2], row[3], iva_obj, row[5])
        return None
    #def listarInfoEpresa(id):
        #bd = select * from bd where id = self.id
    
