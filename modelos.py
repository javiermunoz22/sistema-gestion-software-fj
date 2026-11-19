"""Modelos del sistema: clases abstractas, Cliente, servicios y Reserva."""
import itertools
import logging
import re
from abc import ABC, abstractmethod

from excepciones import (
    CalculoInconsistenteError,
    ClienteInvalidoError,
    DuracionInvalidaError,
    OperacionNoPermitidaError,
    ReservaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJException,
)


class EntidadBase(ABC):
    """Clase base ABSTRACTA para las entidades del sistema."""

    def __init__(self, identificador: str, nombre: str):
        self._identificador = identificador  # atributo protegido (encapsulación)
        self._nombre = nombre

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def obtener_detalle(self) -> str:
        """Toda entidad concreta debe describirse (método abstracto)."""


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    PATRON_CORREO = r"^[\w\.\-]+@[\w\-]+(\.[\w\-]+)+$"

    def __init__(self, identificador: str, nombre: str, correo: str):
        # VALIDACIONES: si algo es inválido se lanza excepción (ya no hay "Cliente General")
        if not identificador or not str(identificador).strip():
            raise ClienteInvalidoError("La cédula/identificador del cliente no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError("El nombre del cliente es obligatorio.")
        if not isinstance(correo, str) or not re.match(self.PATRON_CORREO, correo):
            raise ClienteInvalidoError(f"El correo electrónico no es válido: {correo!r}")

        super().__init__(str(identificador).strip(), nombre.strip())
        self.__correo = correo  # atributo privado
        logging.info(f"Cliente creado exitosamente: {self.nombre}")

    @property
    def correo(self):
        return self.__correo

    def obtener_detalle(self):
        return f"Cliente ID: {self._identificador} | Nombre: {self._nombre} | Correo: {self.__correo}"


class Servicio(EntidadBase, ABC):
    """Clase ABSTRACTA Servicio: cada servicio especializado define su propio cálculo."""

    def __init__(self, identificador: str, nombre_servicio: str, tarifa: float):
        super().__init__(identificador, nombre_servicio)
        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ServicioInvalidoError("La tarifa del servicio debe ser un número mayor a cero.")
        self._tarifa = float(tarifa)
        self.disponible = True  # permite simular servicios no disponibles
        logging.info(f"Servicio creado exitosamente: {self._nombre}")

    @property
    def tarifa(self):
        return self._tarifa

    # ---- Métodos abstractos: CADA subclase los sobrescribe (polimorfismo) ----
    @abstractmethod
    def calcular_costo_base(self, cantidad) -> float:
        """Costo sin impuestos ni descuentos; cambia según el tipo de servicio."""

    @abstractmethod
    def validar_parametros(self, cantidad) -> None:
        """Valida la cantidad/duración; lanza DuracionInvalidaError si no es válida."""

    # ---- Método SOBRECARGADO mediante parámetros opcionales ----
    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0) -> float:
        """Variantes: calcular_costo(3) | calcular_costo(3, 0.19) | calcular_costo(3, 0.19, 0.1)
        | calcular_costo(3, descuento=0.1)"""
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError("Impuesto y descuento deben estar entre 0 y 1.")
        self.validar_parametros(cantidad)
        total = self.calcular_costo_base(cantidad) * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo calculado resultó negativo.")
        return round(total, 2)

    @staticmethod
    def _validar_rango(cantidad, maximo, unidad):
        """Utilidad común: número real, > 0 y <= maximo."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
            raise DuracionInvalidaError(f"La cantidad debe ser numérica: {cantidad!r}")
        if cantidad <= 0:
            raise DuracionInvalidaError(f"La cantidad debe ser mayor a 0 {unidad}: {cantidad}")
        if cantidad > maximo:
            raise DuracionInvalidaError(f"El máximo permitido es {maximo} {unidad}: {cantidad}")

    def obtener_detalle(self):
        return f"Servicio: {self._nombre} | Tarifa base: ${self._tarifa:,.2f}"


class ReservaSalas(Servicio):
    """Sala por horas, con recargo del 10% a partir de 4 horas (jornada extendida)."""

    def __init__(self, tarifa):
        super().__init__("S001", "Reserva de Salas", tarifa)

    def validar_parametros(self, cantidad):
        self._validar_rango(cantidad, 12, "horas")

    def calcular_costo_base(self, cantidad):
        recargo = 1.10 if cantidad >= 4 else 1.0
        return self._tarifa * cantidad * recargo


class AlquilerEquipos(Servicio):
    """Equipos por días completos + depósito fijo de garantía."""

    DEPOSITO = 20000.0

    def __init__(self, tarifa):
        super().__init__("S002", "Alquiler de Equipos", tarifa)

    def validar_parametros(self, cantidad):
        self._validar_rango(cantidad, 30, "días")
        if int(cantidad) != cantidad:
            raise DuracionInvalidaError("El alquiler se cobra por días completos.")

    def calcular_costo_base(self, cantidad):
        return self._tarifa * cantidad + self.DEPOSITO


class AsesoriasEspecializadas(Servicio):
    """Asesoría por horas; la tarifa sube 50% si es urgente."""

    def __init__(self, tarifa, urgente=False):
        super().__init__("S003", "Asesorías Especializadas", tarifa)
        self.urgente = urgente

    def validar_parametros(self, cantidad):
        self._validar_rango(cantidad, 8, "horas")

    def calcular_costo_base(self, cantidad):
        return self._tarifa * cantidad * (1.5 if self.urgente else 1.0)


class Reserva(EntidadBase):
    """Integra cliente, servicio, duración y estado."""

    _contador = itertools.count(1)  # genera R001, R002...

    def __init__(self, cliente, servicio, cantidad):
        # VALIDACIONES: una reserva incompleta debe FALLAR, no continuar
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError(f"La reserva requiere un servicio válido (recibido: {servicio!r}).")
        servicio.validar_parametros(cantidad)  # lanza DuracionInvalidaError si es -1, 0, texto...

        super().__init__(f"R{next(Reserva._contador):03d}", f"Reserva de {servicio.nombre}")
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"
        self.costo_total = None

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Delegado al servicio (polimorfismo) con impuesto/descuento opcionales."""
        return self.servicio.calcular_costo(self.cantidad, impuesto, descuento)

    def confirmar(self):
        """Pendiente -> Confirmada (el servicio debe estar disponible)."""
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"'{self.servicio.nombre}' no está disponible.")
        self.estado = "Confirmada"
        logging.info(f"Reserva {self.identificador} confirmada exitosamente.")

    def cancelar(self):
        """Cancela la reserva si no está Procesada ni Cancelada."""
        if self.estado in ("Procesada", "Cancelada"):
            raise OperacionNoPermitidaError(f"Operación no permitida: la reserva está {self.estado}.")
        self.estado = "Cancelada"
        logging.info(f"Reserva {self.identificador} cancelada correctamente.")

    def procesar_reserva(self, impuesto=0.0, descuento=0.0):
        """Procesa la reserva: try/except/else/finally + encadenamiento (raise ... from)."""
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas Confirmadas (estado actual: {self.estado}).")
        try:
            total = self.calcular_costo(impuesto, descuento)
        except SoftwareFJException as causa:
            # Encadenamiento: se conserva el error original con 'from'
            raise ReservaError(f"No se pudo procesar la reserva {self.identificador}.") from causa
        except (TypeError, ValueError) as causa:
            raise CalculoInconsistenteError(
                f"Datos inconsistentes al calcular la reserva {self.identificador}.") from causa
        else:
            # Solo se ejecuta si NO hubo excepción
            self.costo_total = total
            self.estado = "Procesada"
            mensaje = (f"Reserva exitosa para {self.cliente.nombre} "
                       f"({self.servicio.nombre}). Total: ${total:,.0f}")
            logging.info(f"Reserva procesada con éxito: {mensaje}")
            return mensaje
        finally:
            # Se ejecuta SIEMPRE
            logging.info(f"Fin del intento de procesamiento de {self.identificador}.")

    def obtener_detalle(self):
        # Solo describe (antes procesaba la reserva, lo cual era un error)
        total = f"${self.costo_total:,.0f}" if self.costo_total is not None else "sin calcular"
        return (f"Reserva {self.identificador} | {self.cliente.nombre} | "
                f"{self.servicio.nombre} | cantidad {self.cantidad} | {self.estado} | {total}")

    def __str__(self):
        return self.obtener_detalle()
