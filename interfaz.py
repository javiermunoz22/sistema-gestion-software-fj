"""Simulaciones (lógica) e interfaz gráfica Tkinter de Software FJ."""
import logging  # Para registrar eventos y errores en el log

from excepciones import ServicioInvalidoError, SoftwareFJException  # Excepciones usadas en este módulo
from modelos import (AlquilerEquipos, AsesoriasEspecializadas, Cliente, Reserva,
                     ReservaSalas)  # Clases del sistema

# Fábrica de servicios: asocia el texto del escenario con su clase
FABRICA_SERVICIOS = {
    "sala": ReservaSalas,  # "sala" crea una ReservaSalas
    "equipo": AlquilerEquipos,  # "equipo" crea un AlquilerEquipos
    "asesoria": AsesoriasEspecializadas,  # "asesoria" crea una AsesoriasEspecializadas
}


def crear_servicio(tipo_serv, tarifa):
    """Crea un servicio según su tipo. Si no existe, ENCADENA la excepción (raise ... from)."""
    if tipo_serv == "reserva_nula":  # Caso especial de prueba
        return None  # simula un servicio faltante
    try:  # Busca la clase del servicio en la fábrica
        clase = FABRICA_SERVICIOS[tipo_serv]
    except KeyError as causa:  # Si el tipo no existe, Python lanza KeyError
        # Se convierte en ServicioInvalidoError conservando la causa original con 'from'
        raise ServicioInvalidoError(f"El servicio '{tipo_serv}' no está disponible.") from causa
    return clase(tarifa)  # Crea y devuelve el servicio con su tarifa


def ejecutar_simulaciones_logica():
    """Ejecuta las simulaciones (10 base + 4 de casos inválidos adicionales)."""
    # Cada escenario: (id cliente, nombre, correo, tipo de servicio, tarifa, cantidad, variante)
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

    resultados_texto = []  # Lista donde se guardan los mensajes de cada simulación

    # Recorre los escenarios numerándolos desde 1
    for idx, (cid, nombre, correo, tipo_serv, costo, cantidad, variante) in enumerate(escenarios, start=1):
        try:  # Intenta ejecutar la operación completa; si algo falla, salta al except
            cliente = Cliente(cid, nombre, correo)  # Crea el cliente (valida sus datos)
            servicio = crear_servicio(tipo_serv, costo)  # Crea el servicio según el tipo
            if variante == "no_disponible":  # Caso de prueba: servicio fuera de servicio
                servicio.disponible = False  # simula un servicio fuera de servicio
            reserva = Reserva(cliente, servicio, cantidad)  # Crea la reserva (valida cliente, servicio y duración)
            if variante == "cancelar":  # Caso de prueba: reserva cancelada
                reserva.cancelar()  # luego confirmar() debe fallar (operación no permitida)
            reserva.confirmar()  # Confirma la reserva
            impuesto = "diecinueve" if variante == "impuesto_texto" else 0.19  # texto = dato inconsistente
            mensaje_exito = reserva.procesar_reserva(impuesto=impuesto)  # Calcula el costo con 19% de impuesto

        except SoftwareFJException as err:  # Errores propios del sistema (error controlado)
            msg = f"[SIMULACIÓN {idx:02d} - ERROR CONTROLADO] {type(err).__name__}: {err}"  # Mensaje del error
            logging.error(msg)  # Registra el error en el log
            if err.__cause__ is not None:  # si hubo encadenamiento, registramos la causa
                logging.error(f"   Causa original: {type(err.__cause__).__name__}: {err.__cause__}")
            resultados_texto.append(msg)  # Guarda el mensaje para mostrarlo
        except Exception as err:  # red de seguridad: nada debe detener el programa
            msg = f"[SIMULACIÓN {idx:02d} - ERROR INESPERADO] {type(err).__name__}: {err}"  # Error no previsto
            logging.critical(msg)  # Registra el error como crítico
            resultados_texto.append(msg)  # Guarda el mensaje
        else:  # Se ejecuta solo si NO hubo errores
            msg = f"[SIMULACIÓN {idx:02d} - ÉXITO] {mensaje_exito}"  # Mensaje de éxito
            logging.info(msg)  # Registra el éxito en el log
            resultados_texto.append(msg)  # Guarda el mensaje
        finally:  # Se ejecuta SIEMPRE, haya o no error
            logging.info(f"Finalizado ciclo de auditoría para simulación {idx:02d}.")  # Registro de auditoría

    return resultados_texto  # Devuelve todos los resultados


class AppSoftwareFJ:  # Clase de la interfaz gráfica
    """Interfaz gráfica sencilla para mostrar las simulaciones."""

    def __init__(self, root, resultados_iniciales=None):
        import tkinter as tk  # Librería de interfaces gráficas
        from tkinter import scrolledtext  # Cuadro de texto con barra de desplazamiento
        self.tk = tk  # Guarda tkinter para usarlo en otros métodos
        self.root = root  # Ventana principal
        self.root.title("Sistema de Gestión - Software FJ (Fase 4)")  # Título de la ventana
        self.root.geometry("720x560")  # Tamaño de la ventana

        titulo = tk.Label(root, text="Software FJ - Gestión Integral de Reservas",
                          font=("Arial", 14, "bold"))  # Etiqueta con el título
        titulo.pack(pady=10)  # Ubica el título con margen vertical

        btn_simular = tk.Button(
            root, text="Volver a Ejecutar las Simulaciones y Registrar Logs",
            bg="#2E7D32", fg="white", font=("Arial", 10, "bold"),
            command=self.ejecutar_desde_gui)  # Al hacer clic ejecuta las simulaciones
        btn_simular.pack(pady=5)  # Ubica el botón

        self.consola = scrolledtext.ScrolledText(root, width=84, height=24, font=("Consolas", 9))  # Área de resultados
        self.consola.pack(pady=10)  # Ubica el área de texto

        if resultados_iniciales:  # Si llegaron resultados de la ejecución inicial, se muestran
            self.consola.insert(tk.END, "Resultados de la ejecución automática inicial:\n\n")  # Encabezado
            for linea in resultados_iniciales:  # Recorre cada resultado
                self.consola.insert(tk.END, linea + "\n")  # Lo agrega al área de texto

    def ejecutar_desde_gui(self):  # Se ejecuta al presionar el botón
        from tkinter import messagebox  # Cuadros de mensaje
        self.consola.delete("1.0", self.tk.END)  # Borra el contenido anterior
        resultados = ejecutar_simulaciones_logica()  # Ejecuta de nuevo las simulaciones
        self.consola.insert(self.tk.END, "Nuevas simulaciones ejecutadas desde la interfaz:\n\n")  # Encabezado
        for linea in resultados:  # Recorre cada resultado
            self.consola.insert(self.tk.END, linea + "\n")  # Lo muestra en pantalla
        messagebox.showinfo(  # Avisa que terminó y que se guardó el log
            "Simulación Completa",
            "Se ejecutaron las operaciones de prueba y se guardaron en 'eventos_errores.log'.")

# Fin del archivo interfaz.py
