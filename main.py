"""Punto de entrada: simulación en consola + interfaz gráfica."""
import logging  # Módulo estándar de Python para registrar eventos

# Logging a archivo con nivel INFO: guarda eventos exitosos Y errores
logging.basicConfig(
    filename="eventos_errores.log",  # Archivo donde se guarda el registro
    filemode="w",  # "w" reescribe el archivo en cada ejecución
    encoding="utf-8",  # Codificación que conserva las tildes
    level=logging.INFO,  # Nivel INFO: registra eventos exitosos y errores
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato: fecha y hora - nivel - mensaje
)

from interfaz import AppSoftwareFJ, ejecutar_simulaciones_logica  # noqa: E402  (se importa después de configurar el log)


def main():  # Función principal del programa
    print("=" * 65)  # Línea decorativa
    print("INICIO DE LA SIMULACIÓN DE PRUEBAS EN CONSOLA (14 ESCENARIOS)")  # Encabezado en consola
    print("=" * 65)  # Línea decorativa

    resultados = ejecutar_simulaciones_logica()  # Ejecuta las 14 simulaciones y guarda los resultados
    for res in resultados:  # Recorre cada resultado
        print(res)  # Lo muestra en la consola

    print("=" * 65)  # Línea decorativa
    print("INICIANDO INTERFAZ GRÁFICA (AppSoftwareFJ)...")  # Aviso de inicio de la interfaz
    print("=" * 65)  # Línea decorativa

    try:  # Intenta abrir la interfaz gráfica
        import tkinter as tk  # Librería de interfaces gráficas
        root = tk.Tk()  # Crea la ventana principal
        AppSoftwareFJ(root, resultados)  # se pasan los resultados a la ventana
        root.mainloop()  # Mantiene la ventana abierta hasta que se cierre
    except Exception as error:  # sin entorno gráfico el programa NO se cae
        logging.error(f"No se pudo iniciar la interfaz gráfica: {error}")  # Registra el error
        print(f"(Interfaz gráfica no disponible: {error})")  # Avisa en consola


if __name__ == "__main__":  # Solo se ejecuta si el archivo se corre directamente
    main()  # Llama a la función principal
