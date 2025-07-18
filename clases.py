class Estudiante:
    def __init__(self, nombre, edad, carrera, notas):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.notas = notas
        self.tiene_beca = False

    def calcular_promedio(self):
        return sum(self.notas) / len(self.notas)

    def es_aprobado(self):
        return self.calcular_promedio() >= 13

    def mostrar_datos(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'carrera': self.carrera,
            'notas': self.notas,
            'promedio': self.calcular_promedio(),
            'aprobado': self.es_aprobado(),
            'tiene_beca': self.tiene_beca
        }

class Becado(Estudiante):
    def __init__(self, nombre, edad, carrera, notas):
        super().__init__(nombre, edad, carrera, notas)
        self.tiene_beca = True

    def mostrar_datos(self):
        datos = super().mostrar_datos()
        datos['tipo_beca'] = 'Completa'  # Podría ser un atributo adicional
        return datos 