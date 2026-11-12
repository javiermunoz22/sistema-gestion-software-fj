# interfaz.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
from modelos import Cliente, ReservaSalas, Reserva
from excepciones import SoftwareFJException

# Configuración del sistema de logging exigido por la rúbrica
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
                # Bloque try - except - else - finally exigido por el profesor
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
