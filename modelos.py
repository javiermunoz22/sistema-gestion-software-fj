"""Modelos del sistema: clases abstractas, Cliente, servicios y Reserva."""
import itertools  # Para generar números consecutivos (identificadores de reservas)
import logging  # Para registrar eventos y errores en el archivo de log
import re  # Para validar el correo con una expresión regular
from abc import ABC, abstractmethod  # Herramientas para crear clases y métodos abstractos

from excepciones import (  # Se importan las excepciones personalizadas del sistema
    CalculoInconsistenteError,
    ClienteInvalidoError,
    DuracionInvalidaError,
    OperacionNoPermitidaError,
    ReservaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJException,
)


class EntidadBase(ABC):  # Clase ABSTRACTA: no se puede instanciar directamente
    """Clase base ABSTRACTA para las entidades del sistema."""

    def __init__(self, identificador: str, nombre: str):  # Constructor común a todas las entidades
        self._identificador = identificador  # atributo protegido (encapsulación)
        self._nombre = nombre  # Nombre de la entidad (protegido)

    @property  # Permite leer el atributo como si fuera una variable, sin poder modificarlo
    def identificador(self):
        return self._identificador  # Devuelve el identificador

    @property  # Propiedad de solo lectura para el nombre
    def nombre(self):
        return self._nombre  # Devuelve el nombre

    @abstractmethod  # Obliga a las clases hijas a implementar este método
    def obtener_detalle(self) -> str:
        """Toda entidad concreta debe describirse (método abstracto)."""


class Cliente(EntidadBase):  # Hereda de EntidadBase
    """Cliente con datos personales encapsulados y validados."""

    PATRON_CORREO = r"^[\w\.\-]+@[\w\-]+(\.[\w\-]+)+$"  # Expresión regular para validar el formato del correo

    def __init__(self, identificador: str, nombre: str, correo: str):
        # VALIDACIONES: si algo es inválido se lanza excepción (ya no hay "Cliente General")
        if not identificador or not str(identificador).strip():  # Identificador vacío o solo espacios
            raise ClienteInvalidoError("La cédula/identificador del cliente no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():  # Nombre que no es texto o está vacío
            raise ClienteInvalidoError("El nombre del cliente es obligatorio.")
        if not isinstance(correo, str) or not re.match(self.PATRON_CORREO, correo):  # Correo mal formado
            raise ClienteInvalidoError(f"El correo electrónico no es válido: {correo!r}")

        super().__init__(str(identificador).strip(), nombre.strip())  # Guarda id y nombre limpios en la clase base
        self.__correo = correo  # atributo privado
        logging.info(f"Cliente creado exitosamente: {self.nombre}")  # Registra el evento en el log

    @property  # Acceso de solo lectura al correo privado
    def correo(self):
        return self.__correo  # Devuelve el correo

    def obtener_detalle(self):  # Implementa el método abstracto de EntidadBase
        return f"Cliente ID: {self._identificador} | Nombre: {self._nombre} | Correo: {self.__correo}"


class Servicio(EntidadBase, ABC):  # Clase ABSTRACTA: define lo que todo servicio debe cumplir
    """Clase ABSTRACTA Servicio: cada servicio especializado define su propio cálculo."""

    def __init__(self, identificador: str, nombre_servicio: str, tarifa: float):
        super().__init__(identificador, nombre_servicio)  # Inicializa la parte común (id y nombre)
        # La tarifa debe ser un número (no bool) y mayor que cero
        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ServicioInvalidoError("La tarifa del servicio debe ser un número mayor a cero.")
        self._tarifa = float(tarifa)  # Se guarda como número decimal
        self.disponible = True  # permite simular servicios no disponibles
        logging.info(f"Servicio creado exitosamente: {self._nombre}")  # Registra la creación en el log

    @property  # Acceso de solo lectura a la tarifa
    def tarifa(self):
        return self._tarifa  # Devuelve la tarifa

    # ---- Métodos abstractos: CADA subclase los sobrescribe (polimorfismo) ----
    @abstractmethod  # Cada servicio calcula su costo base de forma distinta
    def calcular_costo_base(self, cantidad) -> float:
        """Costo sin impuestos ni descuentos; cambia según el tipo de servicio."""

    @abstractmethod  # Cada servicio define qué duraciones acepta
    def validar_parametros(self, cantidad) -> None:
        """Valida la cantidad/duración; lanza DuracionInvalidaError si no es válida."""

    # ---- Método SOBRECARGADO mediante parámetros opcionales ----
    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0) -> float:
        """Variantes: calcular_costo(3) | calcular_costo(3, 0.19) | calcular_costo(3, 0.19, 0.1)
        | calcular_costo(3, descuento=0.1)"""
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:  # Impuesto y descuento deben estar entre 0 y 1
            raise CalculoInconsistenteError("Impuesto y descuento deben estar entre 0 y 1.")
        self.validar_parametros(cantidad)  # Valida la duración según el servicio concreto
        total = self.calcular_costo_base(cantidad) * (1 - descuento) * (1 + impuesto)  # Aplica descuento e impuesto
        if total < 0:  # Un costo negativo es inconsistente
            raise CalculoInconsistenteError("El costo calculado resultó negativo.")
        return round(total, 2)  # Devuelve el total redondeado a 2 decimales

    @staticmethod  # Método que no necesita acceder a la instancia
    def _validar_rango(cantidad, maximo, unidad):
        """Utilidad común: número real, > 0 y <= maximo."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):  # Debe ser numérica
            raise DuracionInvalidaError(f"La cantidad debe ser numérica: {cantidad!r}")
        if cantidad <= 0:  # No se aceptan cantidades cero o negativas
            raise DuracionInvalidaError(f"La cantidad debe ser mayor a 0 {unidad}: {cantidad}")
        if cantidad > maximo:  # No se acepta superar el máximo del servicio
            raise DuracionInvalidaError(f"El máximo permitido es {maximo} {unidad}: {cantidad}")

    def obtener_detalle(self):  # Implementa el método abstracto de EntidadBase
        return f"Servicio: {self._nombre} | Tarifa base: ${self._tarifa:,.2f}"


class ReservaSalas(Servicio):  # Servicio especializado 1: hereda de Servicio
    """Sala por horas, con recargo del 10% a partir de 4 horas (jornada extendida)."""

    def __init__(self, tarifa):
        super().__init__("S001", "Reserva de Salas", tarifa)  # Id y nombre fijos de este servicio

    def validar_parametros(self, cantidad):  # Sobrescribe el método abstracto
        self._validar_rango(cantidad, 12, "horas")  # Máximo 12 horas

    def calcular_costo_base(self, cantidad):  # Sobrescribe el método abstracto (polimorfismo)
        recargo = 1.10 if cantidad >= 4 else 1.0  # 10% de recargo desde 4 horas
        return self._tarifa * cantidad * recargo  # Tarifa por hora x horas x recargo


class AlquilerEquipos(Servicio):  # Servicio especializado 2: hereda de Servicio
    """Equipos por días completos + depósito fijo de garantía."""

    DEPOSITO = 20000.0  # Depósito de garantía fijo

    def __init__(self, tarifa):
        super().__init__("S002", "Alquiler de Equipos", tarifa)  # Id y nombre fijos de este servicio

    def validar_parametros(self, cantidad):  # Sobrescribe el método abstracto
        self._validar_rango(cantidad, 30, "días")  # Máximo 30 días
        if int(cantidad) != cantidad:  # Solo se aceptan días completos
            raise DuracionInvalidaError("El alquiler se cobra por días completos.")

    def calcular_costo_base(self, cantidad):  # Sobrescribe el método abstracto (polimorfismo)
        return self._tarifa * cantidad + self.DEPOSITO  # Tarifa por día x días + depósito


class AsesoriasEspecializadas(Servicio):  # Servicio especializado 3: hereda de Servicio
    """Asesoría por horas; la tarifa sube 50% si es urgente."""

    def __init__(self, tarifa, urgente=False):
        super().__init__("S003", "Asesorías Especializadas", tarifa)  # Id y nombre fijos
        self.urgente = urgente  # Indica si la asesoría es urgente

    def validar_parametros(self, cantidad):  # Sobrescribe el método abstracto
        self._validar_rango(cantidad, 8, "horas")  # Máximo 8 horas

    def calcular_costo_base(self, cantidad):  # Sobrescribe el método abstracto (polimorfismo)
        return self._tarifa * cantidad * (1.5 if self.urgente else 1.0)  # 50% más si es urgente


class Reserva(EntidadBase):  # Reserva: integra cliente, servicio, duración y estado
    """Integra cliente, servicio, duración y estado."""

    _contador = itertools.count(1)  # genera R001, R002...

    def __init__(self, cliente, servicio, cantidad):
        # VALIDACIONES: una reserva incompleta debe FALLAR, no continuar
        if not isinstance(cliente, Cliente):  # El cliente debe ser un objeto Cliente
            raise ReservaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):  # El servicio debe ser un objeto Servicio (no None)
            raise ReservaError(f"La reserva requiere un servicio válido (recibido: {servicio!r}).")
        servicio.validar_parametros(cantidad)  # lanza DuracionInvalidaError si es -1, 0, texto...

        super().__init__(f"R{next(Reserva._contador):03d}", f"Reserva de {servicio.nombre}")  # Genera el id R001, R002...
        self.cliente = cliente  # Cliente que hace la reserva
        self.servicio = servicio  # Servicio reservado
        self.cantidad = cantidad  # Duración (horas o días)
        self.estado = "Pendiente"  # Estado inicial
        self.costo_total = None  # Se calcula al procesar la reserva

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Delegado al servicio (polimorfismo) con impuesto/descuento opcionales."""
        return self.servicio.calcular_costo(self.cantidad, impuesto, descuento)  # Cada servicio calcula a su manera

    def confirmar(self):
        """Pendiente -> Confirmada (el servicio debe estar disponible)."""
        if self.estado != "Pendiente":  # Solo se confirman reservas pendientes
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}.")
        if not self.servicio.disponible:  # El servicio debe estar disponible
            raise ServicioNoDisponibleError(f"'{self.servicio.nombre}' no está disponible.")
        self.estado = "Confirmada"  # Cambia el estado
        logging.info(f"Reserva {self.identificador} confirmada exitosamente.")  # Registra el evento

    def cancelar(self):
        """Cancela la reserva si no está Procesada ni Cancelada."""
        if self.estado in ("Procesada", "Cancelada"):  # No se puede cancelar dos veces ni una ya procesada
            raise OperacionNoPermitidaError(f"Operación no permitida: la reserva está {self.estado}.")
        self.estado = "Cancelada"  # Cambia el estado
        logging.info(f"Reserva {self.identificador} cancelada correctamente.")  # Registra el evento

    def procesar_reserva(self, impuesto=0.0, descuento=0.0):
        """Procesa la reserva: try/except/else/finally + encadenamiento (raise ... from)."""
        if self.estado != "Confirmada":  # Solo se procesan reservas confirmadas
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas Confirmadas (estado actual: {self.estado}).")
        try:  # Intenta calcular el costo
            total = self.calcular_costo(impuesto, descuento)
        except SoftwareFJException as causa:  # Error propio del sistema
            # Encadenamiento: se conserva el error original con 'from'
            raise ReservaError(f"No se pudo procesar la reserva {self.identificador}.") from causa
        except (TypeError, ValueError) as causa:  # Datos de tipo incorrecto (ej. impuesto como texto)
            raise CalculoInconsistenteError(
                f"Datos inconsistentes al calcular la reserva {self.identificador}.") from causa
        else:
            # Solo se ejecuta si NO hubo excepción
            self.costo_total = total  # Guarda el costo calculado
            self.estado = "Procesada"  # Cambia el estado
            mensaje = (f"Reserva exitosa para {self.cliente.nombre} "
                       f"({self.servicio.nombre}). Total: ${total:,.0f}")  # Mensaje de éxito
            logging.info(f"Reserva procesada con éxito: {mensaje}")  # Registra el evento
            return mensaje  # Devuelve el mensaje
        finally:
            # Se ejecuta SIEMPRE
            logging.info(f"Fin del intento de procesamiento de {self.identificador}.")  # Registro de auditoría

    def obtener_detalle(self):  # Implementa el método abstracto de EntidadBase
        # Solo describe (antes procesaba la reserva, lo cual era un error)
        total = f"${self.costo_total:,.0f}" if self.costo_total is not None else "sin calcular"  # Formato del total
        return (f"Reserva {self.identificador} | {self.cliente.nombre} | "
                f"{self.servicio.nombre} | cantidad {self.cantidad} | {self.estado} | {total}")

    def __str__(self):  # Texto que se muestra al imprimir la reserva
        return self.obtener_detalle()
