import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
from excepciones import SoftwareFJException
from modelos import Cliente, ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas, Reserva

def ejecutar_simulaciones_logica():
    """Ejecuta las 10 simulaciones obligatorias y retorna los resultados."""
    escenarios = [
        ("C01", "Laura Gómez", "laura@mail.com", "sala", 50000, 3),
        ("C02", "", "sin_nombre@mail.com", "equipo", 80000, 2),
        ("C03", "Carlos Ruiz", "carlos@mail.com", "equipo", 80000, 4),
        ("C04", "Ana Torres", "ana@mail.com", "sala", 50000, -1),
        ("C05", "Luis Pérez", "luis@mail.com", "asesoria", 120000, 2),
        ("C06", "Marta Díaz", "correo_sin_arroba", "sala", 50000, 2),
        ("C07", "Jorge Mora", "jorge@mail.com", "inexistente", 40000, 1),
        ("C08", "Sofía León", "sofia@mail.com", "sala", 60000, 5),
        ("C09", "Pedro Gil", "pedro@mail.com", "reserva_nula", 0, 0),
        ("C10", "Elena Ríos", "elena@mail.com", "asesoria", 150000, 3)
    ]

    resultados_texto = []

    for idx, (cid, nombre, correo, tipo_serv, costo, cantidad) in enumerate(escenarios, start=1):
        try:
            cliente = Cliente(cid, nombre, correo)

            if tipo_serv == "sala":
                servicio = ReservaSalas(costo, cantidad)
            elif tipo_serv == "equipo":
                servicio = AlquilerEquipos(costo, cantidad)
            elif tipo_serv == "asesoria":
                servicio = AsesoriasEspecializadas(costo, cantidad)
            elif tipo_serv == "reserva_nula":
                servicio = None
            else:
                raise ServicioInvalidoError(f"El servicio '{tipo_serv}' no está disponible.")

            reserva = Reserva(cliente, servicio)
            mensaje_exito = reserva.procesar_reserva()

        except SoftwareFJException as err:
            msg = f"[SIMULACIÓN {idx:02d} - ERROR CONTROLADO] {type(err).__name__}: {err}"
            logging.error(msg)
            resultados_texto.append(msg)
        else:
            msg = f"[SIMULACIÓN {idx:02d} - ÉXITO] {mensaje_exito}"
            logging.info(msg)
            resultados_texto.append(msg)
        finally:
            logging.debug(f"Finalizado ciclo de auditoría para simulación {idx:02d}.")

    return resultados_texto


class AppSoftwareFJ:
    def __init__(self, root, resultados_iniciales=None):
        self.root = root
        self.root.title("Sistema de Gestión - Software FJ (Fase 4)")
        self.root.geometry("720x560")

        titulo = tk.Label(root, text="Software FJ - Gestión Integral de Reservas", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        btn_simular = tk.Button(
            root,
            text="Volver a Ejecutar 10 Simulaciones y Registrar Logs",
            bg="#2E7D32",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.ejecutar_desde_gui
        )
        btn_simular.pack(pady=5)

        self.consola = scrolledtext.ScrolledText(root, width=84, height=24, font=("Consolas", 9))
        self.consola.pack(pady=10)

        if resultados_iniciales:
            self.consola.insert(tk.END, "Resultados de la ejecución automática inicial:\n\n")
            for linea in resultados_iniciales:
                self.consola.insert(tk.END, linea + "\n")

    def ejecutar_desde_gui(self):
        self.consola.delete("1.0", tk.END)
        resultados = ejecutar_simulaciones_logica()
        self.consola.insert(tk.END, "Nuevas simulaciones ejecutadas desde la interfaz:\n\n")
        for linea in resultados:
            self.consola.insert(tk.END, linea + "\n")
        messagebox.showinfo("Simulación Completa", "Se ejecutaron las 10 operaciones de prueba y se guardaron en 'eventos_errores.log'.")