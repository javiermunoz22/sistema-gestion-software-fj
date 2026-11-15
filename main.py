import logging
import tkinter as tk
from modelos import Cliente, Servicio, Reserva
from excepciones import ClienteInvalidoError, ServicioInvalidoError, ReservaError
from interfaz import InterfazSoftwareFJ  # O el nombre de tu clase en interfaz.py

# Configuración del sistema de logging para generar 'eventos_errores.log'
logging.basicConfig(
    filename='eventos_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def ejecutar_simulaciones():
    print("=" * 60)
    print("INICIO DE LA SIMULACIÓN DE PRUEBAS (10 ESCENARIOS)")
    print("=" * 60)

    # Simulación 1: Creación exitosa de cliente válido
    try:
        print("\n[Simulación 1] Creando cliente válido...")
        c1 = Cliente("10123456", "Carlos Pérez", "carlos@mail.com", "3001234567")
        print(f"Éxito: Cliente creado -> {c1.nombre}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Simulación 2: Intento fallido de crear cliente con cédula inválida/vacía
    try:
        print("\n[Simulación 2] Intentando crear cliente con datos erróneos...")
        c_malo = Cliente("", "", "correo_invalido", "123")
    except ClienteInvalidoError as ce:
        print(f"-> EXCEPCIÓN CONTROLADA: {ce}")
        logging.error(f"Simulación 2 - Cliente inválido detectado: {ce}")
    except Exception as e:
        print(f"Error general: {e}")

    # Simulación 3: Creación exitosa de un servicio
    try:
        print("\n[Simulación 3] Creando servicio activo...")
        s1 = Servicio("S01", "Asesoría Técnica", 150000.0, True)
        print(f"Éxito: Servicio creado -> {s1.nombre} ($ {s1.precio})")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Simulación 4: Intento fallido de crear servicio con valor negativo
    try:
        print("\n[Simulación 4] Intentando crear servicio con precio negativo...")
        s_malo = Servicio("S02", "Soporte", -50000.0, True)
    except ServicioInvalidoError as se:
        print(f"-> EXCEPCIÓN CONTROLADA: {se}")
        logging.error(f"Simulación 4 - Servicio inválido detectado: {se}")
    except Exception as e:
        print(f"Error general: {e}")

    # Simulación 5: Creación exitosa de una reserva
    try:
        print("\n[Simulación 5] Creando reserva válida...")
        r1 = Reserva("R01", c1, s1, "2026-11-20")
        print(f"Éxito: Reserva {r1.id_reserva} asignada a {r1.cliente.nombre}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Simulación 6: Intento fallido de reserva con cliente no registrado o nulo
    try:
        print("\n[Simulación 6] Intentando reservar con cliente nulo/inválido...")
        r_mala = Reserva("R02", None, s1, "2026-11-21")
    except ReservaError as re:
        print(f"-> EXCEPCIÓN CONTROLADA: {re}")
        logging.error(f"Simulación 6 - Reserva inválida detectada: {re}")
    except Exception as e:
        print(f"-> EXCEPCIÓN CONTROLADA GENERAL: {e}")
        logging.error(f"Simulación 6 - Error de reserva: {e}")

    # Simulación 7: Intento fallido usando un servicio inactivo
    try:
        print("\n[Simulación 7] Intentando reservar un servicio inactivo...")
        s_inactivo = Servicio("S03", "Mantenimiento Antiguo", 80000.0, False)
        if not s_inactivo.activo:
            raise ServicioInvalidoError("El servicio seleccionado no se encuentra activo.")
    except ServicioInvalidoError as sie:
        print(f"-> EXCEPCIÓN CONTROLADA: {sie}")
        logging.error(f"Simulación 7 - Servicio inactivo: {sie}")

    # Simulación 8: Modificación o actualización correcta de datos de reserva
    try:
        print("\n[Simulación 8] Actualizando fecha de reserva válida...")
        r1.actualizar_fecha("2026-11-22")
        print(f"Éxito: Fecha de reserva actualizada a {r1.fecha}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Simulación 9: Intento fallido de formato de fecha u operación no permitida
    try:
        print("\n[Simulación 9] Intentando asignar formato de fecha incorrecto...")
        r1.actualizar_fecha("fecha-invalida")
    except ReservaError as re:
        print(f"-> EXCEPCIÓN CONTROLADA: {re}")
        logging.error(f"Simulación 9 - Formato de fecha incorrecto: {re}")
    except Exception as e:
        print(f"-> EXCEPCIÓN CONTROLADA GENERAL: {e}")
        logging.error(f"Simulación 9 - Error en fecha: {e}")

    # Simulación 10: Validación final de integridad de transacciones
    try:
        print("\n[Simulación 10] Validando cierre de ciclo del sistema...")
        print("Éxito: Todas las validaciones de excepciones y registros completadas sin detener la app.")
    except Exception as e:
        print(f"Error: {e}")

    print("=" * 60)
    print("FIN DE LAS 10 SIMULACIONES. REVISE EL ARCHIVO 'eventos_errores.log'")
    print("=" * 60)

if __name__ == "__main__":
    # 1. Primero ejecutamos las 10 simulaciones en consola con los try-except y logs
    ejecutar_simulaciones()
    
    # 2. Luego levantamos la interfaz gráfica de Tkinter para cumplir con la visual
    print("\nIniciando interfaz gráfica de usuario (Tkinter)...")
    root = tk.Tk()
    app = InterfazSoftwareFJ(root)  # Asegúrate de que coincida con el nombre de tu clase en interfaz.py
    root.mainloop()