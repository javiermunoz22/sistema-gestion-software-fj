import datetime
import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext

# ==========================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
logging.basicConfig(
    filename='eventos_errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class SoftwareFJException(Exception):
    """Clase base para excepciones del sistema Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJException):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

class ServicioInvalidoError(SoftwareFJException):
    """Excepción lanzada cuando los parámetros del servicio son incorrectos."""
    pass

class ReservaError(SoftwareFJException):
    """Excepción lanzada durante el proceso de reserva."""
    pass


# ==========================================
# CLASE ABSTRACTA GENERAL
# ==========================================
class EntidadBase:
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    def obtener_detalles(self) -> str:
        raise NotImplementedError("Este método debe ser implementado por la subclase.")


# ==========================================
# CLASE CLIENTE
# ==========================================
class Cliente(EntidadBase):
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre de cliente inválido: '{valor}'. Mínimo 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).isdigit() or len(str(valor)) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'. Solo números, mínimo 7 dígitos.")
        self._telefono = str(valor)

    def obtener_detalles(self) -> str:
        return f"Cliente [ID: {self.identificador}] Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}"


# ==========================================
# CLASE ABSTRACTA SERVICIO Y ESPECIALIZADOS
# ==========================================
class Servicio(EntidadBase):
    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):
        if valor < 0:
            raise ServicioInvalidoError("La tarifa base no puede ser negativa.")
        self._tarifa_base = float(valor)

    def calcular_costo(self, duracion_horas: float, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        raise NotImplementedError("Implementar en subclase.")

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Tarifa Base: ${self.tarifa_base}"


class ReservaSalas(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, capacidad: int):
        super().__init__(identificador, "Reserva de Salas", tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(self, duracion_horas: float, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if duracion_horas <= 0:
            raise ServicioInvalidoError("La duración en horas debe ser mayor a cero.")
        subtotal = self.tarifa_base * duracion_horas
        total_con_desc = subtotal * (1 - descuento)
        return total_con_desc * (1 + impuesto)


class AlquilerEquipos(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(identificador, "Alquiler de Equipos", tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, duracion_horas: float, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if duracion_horas <= 0:
            raise ServicioInvalidoError("La duración del alquiler debe ser mayor a cero.")
        recargo = 1.1 if "avanzado" in self.tipo_equipo.lower() else 1.0
        subtotal = self.tarifa_base * duracion_horas * recargo
        total_con_desc = subtotal * (1 - descuento)
        return total_con_desc * (1 + impuesto)


class AsesoriasEspecializadas(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, especialidad: str):
        super().__init__(identificador, "Asesorías Especializadas", tarifa_base)
        self.especialidad = especialidad

    def calcular_costo(self, duracion_horas: float, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if duracion_horas <= 0:
            raise ServicioInvalidoError("Las horas de asesoría deben ser mayores a cero.")
        subtotal = self.tarifa_base * duracion_horas
        total_con_desc = subtotal * (1 - descuento)
        return total_con_desc * (1 + 0.0)


# ==========================================
# CLASE RESERVA
# ==========================================
class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def procesar_reserva(self, descuento: float = 0.0):
        try:
            self.costo_total = self.servicio.calcular_costo(self.duracion_horas, descuento)
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} procesada con éxito para {self.cliente.nombre}.")
        except Exception as e:
            self.estado = "Fallida"
            logging.error(f"Error al procesar la reserva {self.id_reserva}: {e}")
            raise ReservaError(f"No se pudo completar la reserva {self.id_reserva}") from e


# ==========================================
# INTERFAZ GRÁFICA CON TKINTER
# ==========================================
class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integral de Gestión - Software FJ")
        self.root.geometry("800x600")

        # Título principal
        titulo = tk.Label(root, text="Simulación de Operaciones - Software FJ", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # Botón para ejecutar la simulación
        self.btn_ejecutar = tk.Button(root, text="Ejecutar 10 Simulaciones y Pruebas", font=("Arial", 12), 
                                      bg="#4CAF50", fg="white", command=self.ejecutar_simulacion)
        self.btn_ejecutar.pack(pady=5)

        # Cuadro de texto deslizable para mostrar los resultados en pantalla
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=28, font=("Consolas", 10))
        self.text_area.pack(padx=10, pady=10)

    def log_texto(self, mensaje):
        self.text_area.insert(tk.END, mensaje + "\n")
        self.text_area.see(tk.END)

    def ejecutar_simulacion(self):
        self.text_area.delete(1.0, tk.END)
        self.log_texto("=== INICIANDO SIMULACIÓN DE OPERACIONES EN SOFTWARE FJ ===\n")

        operaciones_simuladas = [
            lambda: Cliente("C001", "Ana María Gómez", "ana.gomez@mail.com", "3104567890"),
            lambda: Cliente("C002", "Jo", "jo@mail.com", "3201234567"), # Error esperado
            lambda: ReservaSalas("S001", 50000.0, 15),
            lambda: AlquilerEquipos("S002", -20000.0, "Proyector"), # Error esperado
            lambda: Reserva("R001", Cliente("C003", "Carlos Pérez", "carlos@mail.com", "3009876543"), 
                            ReservaSalas("S003", 40000.0, 10), 3.0),
            lambda: Reserva("R002", Cliente("C004", "Lucía Torres", "lucia@mail.com", "3112223344"), 
                            AsesoriasEspecializadas("S004", 80000.0, "Software"), -2.0), # Error esperado
            lambda: Cliente("C005", "Pedro Picapiedra", "pedromail.com", "3156789012"), # Error esperado
            lambda: AlquilerEquipos("S005", 30000.0, "Servidor Avanzado"),
            lambda: AsesoriasEspecializadas("S006", 120000.0, "Arquitectura de Software"),
            lambda: Cliente("C006", "María Fernanda", "mafe@mail.com", "318ABC7890") # Error esperado
        ]

        for i, operacion in enumerate(operaciones_simuladas, 1):
            self.log_texto(f"--- Simulando Operación #{i} ---")
            try:
                resultado = operacion()
                if isinstance(resultado, Reserva):
                    resultado.procesar_reserva(descuento=0.05)
                    self.log_texto(f" [ÉXITO] Reserva {resultado.id_reserva} procesada. Costo Total: ${resultado.costo_total:,.2f}")
                else:
                    self.log_texto(f" [ÉXITO] Objeto creado: {resultado.obtener_detalles()}")
            except ClienteInvalidoError as cie:
                self.log_texto(f" ⚠️ [CONTROLADO] Error de Cliente: {cie}")
                logging.warning(f"Operación #{i} falló por ClienteInvalido: {cie}")
            except ServicioInvalidoError as sie:
                self.log_texto(f" ⚠️ [CONTROLADO] Error de Servicio: {sie}")
                logging.warning(f"Operación #{i} falló por ServicioInvalido: {sie}")
            except ReservaError as re:
                self.log_texto(f" ⚠️ [CONTROLADO] Error en Reserva: {re}")
            except Exception as ex:
                self.log_texto(f" ❌ [CONTROLADO] Error inesperado: {ex}")
                logging.error(f"Error general en Operación #{i}: {ex}")
            else:
                self.log_texto(" [ESTADO] Operación ejecutada sin excepciones secundarias.\n")

        self.log_texto("\n=== SIMULACIÓN FINALIZADA. ARCHIVO 'eventos_errores.log' ACTUALIZADO ===")
        messagebox.showinfo("Simulación Completada", "Las 10 operaciones se han ejecutado correctamente con manejo de excepciones.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()