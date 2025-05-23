class Iva:
    def __init__(self, iva_id, nombre, porcentaje):
        self.iva_id = iva_id
        self.nombre = nombre
        self.porcentaje = porcentaje

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"
