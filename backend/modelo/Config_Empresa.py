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

def crear_tabla_config_empresa():
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

def guardar_config_empresa(config_empresa):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        REPLACE INTO Config_Empresa 
        (empresa_id, nombre, direccion, telefono, iva_id, moneda)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        config_empresa.empresa_id,
        config_empresa.nombre,
        config_empresa.direccion,
        config_empresa.telefono,
        config_empresa.iva_id.iva_id,  
        config_empresa.moneda
    ))
    conn.commit()
    conn.close()
def obtener_config_empresa():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT empresa_id, nombre, direccion, telefono, iva_id, moneda 
        FROM Config_Empresa 
        WHERE empresa_id = ?
    ''', ("empresa_001",))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "empresa_id": row[0],
            "nombre": row[1],
            "direccion": row[2],
            "telefono": row[3],
            "iva_id": row[4],
            "moneda": row[5]
        }
    return None

    
    #def listarInfoEpresa(id):
        #bd = select * from bd where id = self.id
    
