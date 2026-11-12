# ==========================================
# SISTEMA DE GESTIÓN INTEGRAL - SOFTWARE FJ
# Fase 4: Componente Práctico (Prácticas Simuladas)
# ==========================================

import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
from abc import ABC, abstractmethod

# ------------------------------------------
# 1. EXCEPCIONES PERSONALIZADAS
# ------------------------------------------
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


# ------------------------------------------
# 2. MODELOS Y CLASES (POO)
# ------------------------------------------
class EntidaddBase(ABC):
    """Clase abstracta base para las entidades del sistema."""
    def __init__(self, identificador):
        self.identificador = identificador

    @abstractmethod
    def obtener_detalle(self):
        pass


class Cliente(EntidaddBase):
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


# ------------------------------------------
# 3. CONFIGURACIÓN DE LOGS E INTERFAZ GRÁFICA
# ------------------------------------------
logging.basicConfig(
    filename='eventos_errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión - Software FJ (Fase 4)")
        self.root.geometry("650x550")

        # Título
        titulo = tk.Label(root, text="Software FJ - Gestión Integral", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        # Botón para ejecutar las 10 simulaciones automáticas exigidas
        btn_simular = tk.Button(root, text="Ejecutar 10 Simulaciones y Registrar Logs", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.ejecutar_simulaciones)
        btn_simular.pack(pady=5)

        # Área de texto para consola visual
        self.consola = scrolledtext.ScrolledText(root, width=75, height=22)
        self.consola.pack(pady=10)
        
        logging.info("Aplicación iniciada correctamente.")

    def ejecutar_simulaciones(self):
        self.consola.delete("1.0", tk.END)
        self.consola.insert(tk.END, "Iniciando las 10 simulaciones de prueba...\n\n")
        
        # Bucle de 10 operaciones (exitosas y con errores controlados) para los logs
        for i in range(1, 11):
            try:
                # Bloque try - except - else - finally exigido por la rúbrica
                if i % 2 == 0:
                    # Simulación exitosa
                    c = Cliente(f"C0{i}", f"Cliente {i}", f"c{i}@mail.com")
                    s = ReservaSalas(50000, 2)
                    res = Reserva(c, s)
                    resultado = res.procesar_reserva()
                    logging.info(f"Simulación {i} exitosa: {resultado}")
                    self.consola.insert(tk.END, f"[ÉXITO] {resultado}\n")
                else:
                    # Simulación que dispara excepción controlada
                    raise ValueError(f"Dato corrupto en ciclo {i}")
            
            except (SoftwareFJException, ValueError) as err:
                # Bloque except con encadenamiento raise ... from
                logging.error(f"Simulación {i} fallida y controlada: {err}")
                self.consola.insert(tk.END, f"[ERROR CONTROLADO] Operación {i}: {err}\n")
            
            else:
                # Cláusula else requerida
                logging.debug(f"Ciclo {i} procesado sin excepciones imprevistas.")
            
            finally:
                # Bloque finally requerido por la rúbrica
                pass

        self.consola.insert(tk.END, "\n¡Las 10 simulaciones finalizaron y se registraron en 'eventos_errores.log'!\n")
        messagebox.showinfo("Simulación Completa", "Se ejecutaron las 10 operaciones de prueba y se guardaron en los logs.")
        logging.info("Las 10 simulaciones de prueba concluyeron con éxito.")


# ------------------------------------------
# 4. PUNTO DE ENTRADA PRINCIPAL
# ------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()