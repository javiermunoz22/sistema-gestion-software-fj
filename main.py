import logging
import tkinter as tk
from interfaz import AppSoftwareFJ, ejecutar_simulaciones_logica

# Configuración del sistema de registro (Logging) con nivel INFO según retroalimentación
logging.basicConfig(
    filename="eventos_errores.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    print("=================================================================")
    print("INICIO DE LA SIMULACIÓN DE PRUEBAS EN CONSOLA (10 ESCENARIOS)")
    print("=================================================================")
    
    # Ejecuta las simulaciones lógicas en consola y registra en eventos_errores.log
    resultados = ejecutar_simulaciones_logica()
    for res in resultados:
        print(res)

    print("=================================================================")
    print("INICIANDO INTERFAZ GRÁFICA (AppSoftwareFJ)...")
    print("=================================================================")

    # Inicia la ventana principal de Tkinter
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()

if __name__ == "__main__":
    main()
