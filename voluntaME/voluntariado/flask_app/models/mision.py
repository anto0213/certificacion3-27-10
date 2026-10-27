# Modelo Misión
class Mision:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.fecha = data['fecha']
        self.voluntarios_necesarios = data['voluntarios_necesarios']
        self.descripcion = data['descripcion']
        self.lider_id = data['lider_id']
        self.lider_nombre = data.get('lider_nombre')
        self.lider_apellido = data.get('lider_apellido')
        self.inscritos = data.get('inscritos', 0)