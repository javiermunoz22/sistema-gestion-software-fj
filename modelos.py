# modelos.py
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError, ServicioInvalidoError, ReservaError

class EntidadBase(ABC):
    """Clase abstracta base para las entidades del sistema."""
    def __init__(self, identificador):
        self.identificador = identificador

    @abstractmethod
    def obtener_detalle(self):
        pass


class Cliente(EntidadBase):
    def __init__(self, identificador, nombre, correo):
        super().__init__(identificador)
        if not nombre or not correo:
            raise ClienteInvalidoError("El nombre y el correo del cliente no pueden estar vacíos.")
        self.nombre = nombre
        self.correo = correo

    def obtener_detalle(self):
        return f"Cliente ID: {self.identificador} | Nombre: {self.nombre} | Correo: {self.correo}"


class Servicio(ABC):
    def __init__(self, nombre_servicio, costo):
        self.nombre_servicio = nombre_servicio
        self.costo = costo

    @abstractmethod
    def calcular_costo(self):
        pass


class ReservaSalas(Servicio):
    def __init__(self, costo, horas):
        super().__init__("Reserva de Salas", costo)
        self.horas = horas

    def calcular_costo(self):
        return self.costo * self.horas


class AlquilerEquipos(Servicio):
    def __init__(self, costo, dias):
        super().__init__("Alquiler de Equipos", costo)
        self.dias = dias

    def calcular_costo(self):
        return self.costo * self.dias


class AsesoriasEspecializadas(Servicio):
    def __init__(self, costo, sesiones):
        super().__init__("Asesorías Especializadas", costo)
        self.sesiones = sesiones

    def calcular_costo(self):
        return self.costo * self.sesiones


class Reserva:
    def __init__(self, cliente, servicio):
        if not cliente:
            raise ReservaError("No se puede crear una reserva sin un cliente válido.")
        self.cliente = cliente
        self.servicio = servicio

    def procesar_reserva(self):
        try:
            total = self.servicio.calcular_costo()
            return f"Reserva exitosa para {self.cliente.nombre}. Total a pagar: ${total}"
        except Exception as e:
            raise ReservaError(f"Error procesando el costo del servicio para {self.cliente.nombre}") from e
