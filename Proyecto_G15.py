from abc import ABC, abstractmethod
from datetime import date, timedelta

class Material(ABC):
    def __init__(self, codigo, autor, titulo, anio, editorial, disponible, cantidad_disponible):
        self.codigo = codigo
        self.autor = autor
        self.titulo = titulo
        self.anio = anio
        self.editorial = editorial
        self.disponible = disponible
        self.cantidad_disponible = cantidad_disponible

    @abstractmethod
    def actualizar_disponibilidad(self, estado):
        pass


class Libro(Material):
    contador_libro = 0

    def __init__(self, codigo, autor, titulo, anio, editorial, disponible, cantidad_disponible, id, tipo_pasta):
        super().__init__(codigo, autor, titulo, anio, editorial, disponible, cantidad_disponible)
        self.id = id
        self.tipo_pasta = tipo_pasta
        Libro.contador_libro += 1

    def actualizar_disponibilidad(self, estado):
        self.disponible = estado


class Revista(Material):
    contador_revista = 0

    def __init__(self, codigo, autor, titulo, anio, editorial, disponible, cantidad_disponible, id, tipo):
        super().__init__(codigo, autor, titulo, anio, editorial, disponible, cantidad_disponible)
        self.id = id
        self.tipo = tipo
        Revista.contador_revista += 1

    def actualizar_disponibilidad(self, estado):
        self.disponible = estado


class Persona(ABC):
    def __init__(self, cedula, nombre, apellido, email, telefono, direccion, numero_libros, activo, carrera):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.numero_libros = numero_libros
        self.activo = activo
        self.carrera = carrera

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @abstractmethod
    def pedir_libro(self):
        pass

    @abstractmethod
    def devolver_libro(self):
        pass


class Estudiante(Persona):
    contador_estudiante = 0

    def __init__(self, cedula, nombre, apellido, email, telefono, direccion, numero_libros, activo, carrera, id, nivel):
        super().__init__(cedula, nombre, apellido, email, telefono, direccion, numero_libros, activo, carrera)
        self.id = id
        self.nivel = nivel
        Estudiante.contador_estudiante += 1

    def pedir_libro(self):
        if self.numero_libros < 3:
            self.numero_libros += 1
            return True
        else:
            return False

    def devolver_libro(self):
        if self.numero_libros > 0:
            self.numero_libros -= 1
            return True
        else:
            return False


class Docente(Persona):
    contador_docente = 0

    def __init__(self, cedula, nombre, apellido, email, telefono, direccion, numero_libros, activo, carrera, id, titulo_3er_nivel, titulo_4to_nivel):
        super().__init__(cedula, nombre, apellido, email, telefono, direccion, numero_libros, activo, carrera)
        self.id = id
        self.titulo_3er_nivel = titulo_3er_nivel
        self.titulo_4to_nivel = titulo_4to_nivel
        Docente.contador_docente += 1

    def pedir_libro(self):
        if self.numero_libros < 5:
            self.numero_libros += 1
            return True
        else:
            return False

    def devolver_libro(self):
        if self.numero_libros > 0:
            self.numero_libros -= 1
            return True
        else:
            return False


class Pedido:
    contador_pedido = 0

    def __init__(self, id, solicitante, lista_material, materia, fecha_prestamo, fecha_devolucion):
        self.id = id
        self.solicitante = solicitante
        self.lista_material = lista_material
        self.materia = materia
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        Pedido.contador_pedido += 1

    def pedir_material(self, list_materia, solicitante, materia):
        for material in list_materia:
            if material.disponible:
                if isinstance(solicitante, Estudiante) and solicitante.pedir_libro():
                    material.actualizar_disponibilidad(False)
                    return True
                elif isinstance(solicitante, Docente) and solicitante.pedir_libro():
                    material.actualizar_disponibilidad(False)
                    return True
        return False

    def devolver_material(self, solicitante):
        if isinstance(solicitante, Estudiante) and solicitante.devolver_libro():
            for material in self.lista_material:
                material.actualizar_disponibilidad(True)
            return True
        elif isinstance(solicitante, Docente) and solicitante.devolver_libro():
            for material in self.lista_material:
                material.actualizar_disponibilidad(True)
            return True
        return False


def main():
    libro = Libro('123', 'Federico Flores', 'La culpa es de la vaca', 2023, 'Santillana', True, 10, 1, 'Dura')
    revista = Revista('456', 'Autor', 'Titulo', 2023, 'Editorial', True, 5, 2, 'Semanal')

    estudiante = Estudiante('1234567890', 'Juan', 'Perez', 'juan.perez@ug.ec', '1234567890', 'Calle Samanes 123', 0, True, 'Ingeniería', 1, 1)
    docente = Docente('0987654321', 'Ana', 'Gomez', 'ana.gomez@ug.edu.ec', '0987654321', 'Avenida Rosales 456', 0, True, 'Matemáticas', 2, 'Licenciatura en Matemáticas', 'Doctorado en Matemáticas')

    pedido = Pedido(1, estudiante, [libro, revista], 'Cálculo', date(2023, 5, 1), date(2023, 5, 8)) # suponiendo que la entrega es el 1 de mayo de 2023 y la devolución es el 8 de mayo de 2023

    print(f"Nombre del estudiante: {estudiante.nombre} {estudiante.apellido}")
    print(f"Correo del estudiante: {estudiante.email}")
    print(f"Nombre del docente: {docente.nombre} {docente.apellido}")
    print(f"Correo del docente: {docente.email}")
    print(f"Nombre del libro: {libro.titulo}")
    print(f"Autor del libro: {libro.autor}")
    print(f"Editorial del libro: {libro.editorial}")
    print(f"Fecha de entrega: {pedido.fecha_prestamo}")
    print(f"Fecha de devolución: {pedido.fecha_devolucion}")
    print("\nGRUPO 15 - INTEGRANRES: KATHERINE SANCHEZ, DARLING MEDINA Y BRYAN REVELO")

    print(pedido.pedir_material([libro, revista], estudiante, 'Cálculo'))
    print(pedido.devolver_material(estudiante))

if __name__ == '__main__':
    main()
