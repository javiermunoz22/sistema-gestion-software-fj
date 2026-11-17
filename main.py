import logging
import tkinter as tk
from interfaz import AppSoftwareFJ, ejecutar_simulaciones_logica

logging.basicConfig(
    filename="eventos_errores.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def main():
    print("=" * 65)
    print("INICIO DE LA SIMULACIÓN DE PRUEBAS EN CONSOLA (10 ESCENARIOS)")
    print("=" * 65)

    resultados = ejecutar_simulaciones_logica()
    for linea in resultados:
        print(linea)

    print("=" * 65)
    print("FIN DE SIMULACIONES. ABRIENDO INTERFAZ GRÁFICA (AppSoftwareFJ)...")
    print("=" * 65)

    root = tk.Tk()
    app = AppSoftwareFJ(root, resultados_iniciales=resultados)
    root.mainloop()


if __name__ == "__main__":
    main()