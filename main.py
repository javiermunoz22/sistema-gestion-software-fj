"""Punto de entrada: simulación en consola + interfaz gráfica."""
import logging

# Logging a archivo con nivel INFO: guarda eventos exitosos Y errores
logging.basicConfig(
    filename="eventos_errores.log",
    filemode="w",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

from interfaz import AppSoftwareFJ, ejecutar_simulaciones_logica  # noqa: E402


def main():
    print("=" * 65)
    print("INICIO DE LA SIMULACIÓN DE PRUEBAS EN CONSOLA (10 ESCENARIOS)")
    print("=" * 65)

    resultados = ejecutar_simulaciones_logica()
    for res in resultados:
        print(res)

    print("=" * 65)
    print("INICIANDO INTERFAZ GRÁFICA (AppSoftwareFJ)...")
    print("=" * 65)

    try:
        import tkinter as tk
        root = tk.Tk()
        AppSoftwareFJ(root, resultados)  # se pasan los resultados a la ventana
        root.mainloop()
    except Exception as error:  # sin entorno gráfico el programa NO se cae
        logging.error(f"No se pudo iniciar la interfaz gráfica: {error}")
        print(f"(Interfaz gráfica no disponible: {error})")


if __name__ == "__main__":
    main()
