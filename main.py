import tkinter as tk
import logging
from interfaz import AppSoftwareFJ, ejecutar_simulaciones_logica

logging.basicConfig(
    filename='eventos_errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("Iniciando las 10 simulaciones obligatorias desde main.py...")
    resultados_arranque = ejecutar_simulaciones_logica()
    print("¡Simulaciones finalizadas y registradas en el log!")

    root = tk.Tk()
    app = AppSoftwareFJ(root, resultados_arranque)
    root.mainloop()