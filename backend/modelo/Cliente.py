class Cliente:
    def __init__(self, id, nombre, documento, telefono):
        self.id = id
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre}"
