"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJException(Exception):
    """Excepción base para el sistema de Software FJ."""

    def __init__(self, mensaje="Error general en Software FJ"):
        super().__init__(mensaje)


class ClienteInvalidoError(SoftwareFJException):
    """Datos del cliente no válidos (nombre vacío, correo mal formado, etc.)."""


class ServicioInvalidoError(SoftwareFJException):
    """El servicio no existe o sus parámetros (ej. tarifa) no son válidos."""


class ServicioNoDisponibleError(SoftwareFJException):
    """Se intenta reservar un servicio que no está disponible."""


class DuracionInvalidaError(SoftwareFJException):
    """Cantidad/duración fuera del rango permitido (negativa, cero, excesiva)."""


class ReservaError(SoftwareFJException):
    """Fallos en la gestión de reservas (datos faltantes, estado incorrecto)."""


class OperacionNoPermitidaError(ReservaError):
    """Operación incompatible con el estado actual de la reserva."""


class CalculoInconsistenteError(SoftwareFJException):
    """El cálculo de costos recibió datos inconsistentes o dio un resultado inválido."""
