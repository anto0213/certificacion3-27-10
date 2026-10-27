# Modelo Voluntario (tabla intermedia)
class Voluntario:
    def __init__(self, data):
        self.id = data['id']
        self.usuario_id = data['usuario_id']
        self.mision_id = data['mision_id']
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')