# excepciones.py
# Jerarquía de excepciones personalizadas para Software FJ

class SoftwareFJException(Exception):
    """Excepción base para el sistema de Software FJ."""
    def __init__(self, mensaje="Error general en Software FJ"):
        super().__init__(mensaje)


class ClienteInvalidoError(SoftwareFJException):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass


class ServicioInvalidoError(SoftwareFJException):
    """Excepción lanzada cuando el servicio seleccionado no es válido."""
    pass


class ReservaError(SoftwareFJException):
    """Excepción lanzada ante fallos en la gestión de reservas."""
    pass