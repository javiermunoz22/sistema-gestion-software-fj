class Reserva(EntidadBase):
    def __init__(self, identificador, cliente, servicio, horas: int):
        super().__init__(identificador, f"Reserva de {servicio.nombre}")
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"  # Estado inicial de la reserva
        self._costo_total = self.calcular_costo()

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Calcula el costo base y permite sobrecarga con impuesto y descuento opcionales."""
        costo_base = self.servicio.costo * self.horas
        costo_final = costo_base + (costo_base * impuesto) - (costo_base * descuento)
        return max(0.0, costo_final)

    def confirmar(self):
        """Confirma la reserva si está pendiente."""
        if self.estado != "Pendiente":
            raise ReservaError(f"No se puede confirmar la reserva {self.identificador} porque su estado actual es '{self.estado}'.")
        self.estado = "Confirmada"
        logging.info(f"Reserva {self.identificador} confirmada exitosamente.")

    def cancelar(self):
        """Cancela la reserva validando que no esté ya procesada o cancelada."""
        if self.estado in ["Procesada", "Cancelada"]:
            raise ReservaError(f"Operación no permitida: no se puede cancelar la reserva {self.identificador} con estado '{self.estado}'.")
        self.estado = "Cancelada"
        logging.info(f"Reserva {self.identificador} cancelada correctamente.")

    def procesar_reserva(self):
        """Procesa la reserva y cambia su estado."""
        if self.estado == "Cancelada":
            raise ReservaError(f"No se puede procesar la reserva {self.identificador} porque se encuentra cancelada.")
        self.estado = "Procesada"
        logging.info(f"Reserva {self.identificador} procesada con éxito.")

    def obtener_detalle(self):
        return f"Reserva ID: {self.identificador} | Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | Estado: {self.estado} | Costo: ${self._costo_total:.2f}"
