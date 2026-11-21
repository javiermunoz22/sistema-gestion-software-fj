"""Excepciones personalizadas del sistema Software FJ."""
# Este módulo define la jerarquía de errores propios del sistema.
# Todas las excepciones heredan de SoftwareFJException, de modo que con un
# solo "except SoftwareFJException" se pueden capturar todos los errores del sistema.


class SoftwareFJException(Exception):  # Clase base: hereda de la clase Exception de Python
    """Excepción base para el sistema de Software FJ."""

    def __init__(self, mensaje="Error general en Software FJ"):  # Constructor con mensaje por defecto
        super().__init__(mensaje)  # Pasa el mensaje a la clase Exception para que se muestre al imprimir el error


class ClienteInvalidoError(SoftwareFJException):  # Error específico de datos de cliente
    """Datos del cliente no válidos (nombre vacío, correo mal formado, etc.)."""


class ServicioInvalidoError(SoftwareFJException):  # Error al crear o seleccionar un servicio
    """El servicio no existe o sus parámetros (ej. tarifa) no son válidos."""


class ServicioNoDisponibleError(SoftwareFJException):  # Error por servicio fuera de servicio
    """Se intenta reservar un servicio que no está disponible."""


class DuracionInvalidaError(SoftwareFJException):  # Error de cantidad/duración fuera de rango
    """Cantidad/duración fuera del rango permitido (negativa, cero, excesiva)."""


class ReservaError(SoftwareFJException):  # Error general de la gestión de reservas
    """Fallos en la gestión de reservas (datos faltantes, estado incorrecto)."""


class OperacionNoPermitidaError(ReservaError):  # Hereda de ReservaError: es un tipo de error de reserva
    """Operación incompatible con el estado actual de la reserva."""


class CalculoInconsistenteError(SoftwareFJException):  # Error en el cálculo de costos
    """El cálculo de costos recibió datos inconsistentes o dio un resultado inválido."""
