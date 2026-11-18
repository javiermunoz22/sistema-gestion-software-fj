import logging
from excepciones import *

class EntidadBase:
    """Clase base abstracta para las entidades del sistema."""
    def __init__(self, identificador: str, nombre: str):
        self._identificador = identificador
        self._nombre = nombre

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    def obtener_detalle(self):
        pass


class Cliente(EntidadBase):
    def __init__(self, identificador: str, nombre: str, correo: str):
        # Si el nombre viene vacío, le asignamos uno por defecto para que no salga en blanco
        nombre_valido = nombre if nombre and nombre.strip() else "Cliente General"
        super().__init__(identificador, nombre_valido)
        
        if not identificador or not str(identificador).strip():
            raise ClienteInvalidoError("La cédula/identificador del cliente no puede estar vacía.")
        if "@" not in correo:
            raise ClienteInvalidoError("El correo electrónico no es válido.")
        
        self.correo = correo
        logging.info(f"Cliente creado exitosamente: {self.nombre}")

    def obtener_detalle(self):
        return f"Cliente ID: {self._identificador} | Nombre: {self._nombre} | Correo: {self.correo}"


class Servicio(EntidadBase):
    def __init__(self, nombre_servicio: str, costo: float):
        super().__init__("S000", nombre_servicio)
        if costo <= 0:
            raise ServicioInvalidoError("El costo del servicio debe ser mayor a cero.")
        self.costo = costo
        logging.info(f"Servicio creado exitosamente: {self._nombre}")

    def obtener_detalle(self):
        return f"Servicio: {self._nombre} | Costo base: ${self.costo:.2f}"


class Reserva(EntidadBase):
    def __init__(self, cliente: Cliente, servicio: Servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.horas = 1
        
        s_nom = getattr(servicio, 'nombre', 'Servicio')
        super().__init__("R001", f"Reserva de {s_nom}")
        self.estado = "Pendiente"
        self._costo_total = getattr(servicio, 'costo', 0.0)

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Calcula el costo total con soporte de sobrecarga para impuesto y descuento."""
        costo_base = self._costo_total
        costo_final = costo_base + (costo_base * impuesto) - (costo_base * descuento)
        return max(0.0, costo_final)

    def confirmar(self):
        """Confirma la reserva si está pendiente."""
        if self.estado != "Pendiente":
            raise ReservaError("No se puede confirmar la reserva.")
        self.estado = "Confirmada"
        logging.info("Reserva confirmada exitosamente.")

    def cancelar(self):
        """Cancela la reserva validando el estado."""
        if self.estado in ["Procesada", "Cancelada"]:
            raise ReservaError("Operación no permitida.")
        self.estado = "Cancelada"
        logging.info("Reserva cancelada correctamente.")

    def procesar_reserva(self):
        """Procesa la reserva y retorna el texto detallado exacto que espera la interfaz."""
        if self.estado == "Cancelada":
            raise ReservaError("No se puede procesar una reserva cancelada.")
        self.estado = "Procesada"
        
        c_nom = getattr(self.cliente, 'nombre', 'Cliente')
        s_nom = getattr(self.servicio, 'nombre', 'Servicio')
        total = self._costo_total
        
        mensaje = f"Reserva exitosa para {c_nom} ({s_nom}). Total: ${total:,.0f}"
        logging.info(f"Reserva procesada con éxito: {mensaje}")
        return mensaje

    def obtener_detalle(self):
        return self.procesar_reserva()

    def __str__(self):
        return self.obtener_detalle()


# Clases específicas heredando de Servicio
class ReservaSalas(Servicio):
    def __init__(self, costo, cantidad):
        total = costo * max(1, cantidad)
        super().__init__("Reserva de Salas", total)


class AlquilerEquipos(Servicio):
    def __init__(self, costo, cantidad):
        total = costo * max(1, cantidad)
        super().__init__("Alquiler de Equipos", total)


class AsesoriasEspecializadas(Servicio):
    def __init__(self, costo, cantidad):
        total = costo * max(1, cantidad)
        super().__init__("Asesorías Especializadas", total)
