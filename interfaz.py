"""Simulaciones (lógica) e interfaz gráfica Tkinter de Software FJ."""
import logging

from excepciones import ServicioInvalidoError, SoftwareFJException
from modelos import (AlquilerEquipos, AsesoriasEspecializadas, Cliente, Reserva,
                     ReservaSalas)

# Fábrica de servicios: asocia el texto del escenario con su clase
FABRICA_SERVICIOS = {
    "sala": ReservaSalas,
    "equipo": AlquilerEquipos,
    "asesoria": AsesoriasEspecializadas,
}


def crear_servicio(tipo_serv, tarifa):
    """Crea un servicio según su tipo. Si no existe, ENCADENA la excepción (raise ... from)."""
    if tipo_serv == "reserva_nula":
        return None  # simula un servicio faltante
    try:
        clase = FABRICA_SERVICIOS[tipo_serv]
    except KeyError as causa:
        raise ServicioInvalidoError(f"El servicio '{tipo_serv}' no está disponible.") from causa
    return clase(tarifa)


def ejecutar_simulaciones_logica():
    """Ejecuta las simulaciones (10 base + 4 de casos inválidos adicionales)."""
    escenarios = [
        ("C01", "Laura Gómez", "laura@mail.com", "sala", 50000, 3, None),          # éxito
        ("C02", "", "sin_nombre@mail.com", "equipo", 80000, 2, None),              # ERROR: sin nombre
        ("C03", "Carlos Ruiz", "carlos@mail.com", "equipo", 80000, 4, None),       # éxito
        ("C04", "Ana Torres", "ana@mail.com", "sala", 50000, -1, None),            # ERROR: duración negativa
        ("C05", "Luis Pérez", "luis@mail.com", "asesoria", 120000, 2, None),       # éxito
        ("C06", "Marta Díaz", "correo_sin_arroba", "sala", 50000, 2, None),        # ERROR: correo inválido
        ("C07", "Jorge Mora", "jorge@mail.com", "inexistente", 40000, 1, None),    # ERROR: servicio inexistente
        ("C08", "Sofía León", "sofia@mail.com", "sala", 60000, 5, None),           # éxito
        ("C09", "Pedro Gil", "pedro@mail.com", "reserva_nula", 0, 0, None),        # ERROR: reserva sin servicio
        ("C10", "Elena Ríos", "elena@mail.com", "asesoria", 150000, 3, None),      # éxito
        # ---- Casos inválidos adicionales (disparan las demás excepciones) ----
        ("C11", "Diana Soto", "diana@mail.com", "sala", 50000, 15, None),                  # ERROR: duración fuera de rango
        ("C12", "Mario Vega", "mario@mail.com", "equipo", 80000, 2, "no_disponible"),      # ERROR: servicio no disponible
        ("C13", "Paula Cruz", "paula@mail.com", "asesoria", 120000, 2, "cancelar"),        # ERROR: operación no permitida
        ("C14", "Hugo Rojas", "hugo@mail.com", "sala", 50000, 2, "impuesto_texto"),        # ERROR: cálculo inconsistente
    ]

    resultados_texto = []

    for idx, (cid, nombre, correo, tipo_serv, costo, cantidad, variante) in enumerate(escenarios, start=1):
        try:
            cliente = Cliente(cid, nombre, correo)
            servicio = crear_servicio(tipo_serv, costo)
            if variante == "no_disponible":
                servicio.disponible = False  # simula un servicio fuera de servicio
            reserva = Reserva(cliente, servicio, cantidad)
            if variante == "cancelar":
                reserva.cancelar()  # luego confirmar() debe fallar (operación no permitida)
            reserva.confirmar()
            impuesto = "diecinueve" if variante == "impuesto_texto" else 0.19  # texto = dato inconsistente
            mensaje_exito = reserva.procesar_reserva(impuesto=impuesto)

        except SoftwareFJException as err:
            msg = f"[SIMULACIÓN {idx:02d} - ERROR CONTROLADO] {type(err).__name__}: {err}"
            logging.error(msg)
            if err.__cause__ is not None:  # si hubo encadenamiento, registramos la causa
                logging.error(f"   Causa original: {type(err.__cause__).__name__}: {err.__cause__}")
            resultados_texto.append(msg)
        except Exception as err:  # red de seguridad: nada debe detener el programa
            msg = f"[SIMULACIÓN {idx:02d} - ERROR INESPERADO] {type(err).__name__}: {err}"
            logging.critical(msg)
            resultados_texto.append(msg)
        else:
            msg = f"[SIMULACIÓN {idx:02d} - ÉXITO] {mensaje_exito}"
            logging.info(msg)
            resultados_texto.append(msg)
        finally:
            logging.info(f"Finalizado ciclo de auditoría para simulación {idx:02d}.")

    return resultados_texto


class AppSoftwareFJ:
    """Interfaz gráfica sencilla para mostrar las simulaciones."""

    def __init__(self, root, resultados_iniciales=None):
        import tkinter as tk
        from tkinter import scrolledtext
        self.tk = tk
        self.root = root
        self.root.title("Sistema de Gestión - Software FJ (Fase 4)")
        self.root.geometry("720x560")

        titulo = tk.Label(root, text="Software FJ - Gestión Integral de Reservas",
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        btn_simular = tk.Button(
            root, text="Volver a Ejecutar las Simulaciones y Registrar Logs",
            bg="#2E7D32", fg="white", font=("Arial", 10, "bold"),
            command=self.ejecutar_desde_gui)
        btn_simular.pack(pady=5)

        self.consola = scrolledtext.ScrolledText(root, width=84, height=24, font=("Consolas", 9))
        self.consola.pack(pady=10)

        if resultados_iniciales:
            self.consola.insert(tk.END, "Resultados de la ejecución automática inicial:\n\n")
            for linea in resultados_iniciales:
                self.consola.insert(tk.END, linea + "\n")

    def ejecutar_desde_gui(self):
        from tkinter import messagebox
        self.consola.delete("1.0", self.tk.END)
        resultados = ejecutar_simulaciones_logica()
        self.consola.insert(self.tk.END, "Nuevas simulaciones ejecutadas desde la interfaz:\n\n")
        for linea in resultados:
            self.consola.insert(self.tk.END, linea + "\n")
        messagebox.showinfo(
            "Simulación Completa",
            "Se ejecutaron las operaciones de prueba y se guardaron en 'eventos_errores.log'.")
