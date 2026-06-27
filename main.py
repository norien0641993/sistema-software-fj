#programa:Ingenieria electrónica 
#Fase 4 - Componente práctico - Prácticas simuladas
#Estudiante: Neiron Andrey Rozo Quezada
#Curso: Programación. 

# =============================================================================
# main.py - Archivo Principal
# =============================================================================

import tkinter as tk
import os

from config import config
from sistema import SistemaSoftwareFJ
from gui import AplicacionGUI
from modelos import SistemaLogs

def ejecutar_simulacion():
    """Ejecuta la simulación de más de 10 operaciones completas."""
    print("=" * 80)
    print("SISTEMA SOFTWARE FJ - SIMULACIÓN DE OPERACIONES")
    print(f"MONEDA: {config.MONEDA}")
    print("=" * 80)
    
    sistema_simulacion = SistemaSoftwareFJ()
    logs = SistemaLogs()

    # Operación 1: Registrar cliente válido
    try:
        cliente = sistema_simulacion.registrar_cliente("Ana Martínez", "ana@empresa.com", "3209876543")
        print(f"✅ Cliente registrado exitosamente con ID: {cliente.id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Operación 2: Registrar cliente con email inválido
    try:
        sistema_simulacion.registrar_cliente("Pedro López", "pedrocorreo", "3123456789")
    except Exception as e:
        print(f"❌ Error esperado al registrar cliente: {e}")

    # Operación 3: Registrar cliente con teléfono inválido
    try:
        sistema_simulacion.registrar_cliente("Laura García", "laura@email.com", "123")
    except Exception as e:
        print(f"❌ Error esperado al registrar cliente: {e}")

    # Operación 4: Crear reserva válida
    try:
        reserva = sistema_simulacion.crear_reserva(1, 1, 3)
        print(f"✅ Reserva creada: {reserva}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Operación 5: Crear reserva con servicio no disponible
    try:
        reserva = sistema_simulacion.crear_reserva(2, 4, 2)
        print(f"✅ Reserva creada: {reserva}")
    except Exception as e:
        print(f"❌ Error esperado al crear reserva: {e}")

    # Operación 6: Crear reserva con cliente inexistente
    try:
        reserva = sistema_simulacion.crear_reserva(99, 1, 2)
        print(f"✅ Reserva creada: {reserva}")
    except Exception as e:
        print(f"❌ Error esperado al crear reserva: {e}")

    # Operación 7: Crear reserva con duración inválida
    try:
        reserva = sistema_simulacion.crear_reserva(1, 1, -5)
        print(f"✅ Reserva creada: {reserva}")
    except Exception as e:
        print(f"❌ Error esperado al crear reserva: {e}")

    # Operación 8: Cancelar reserva válida
    try:
        if sistema_simulacion.cancelar_reserva(1):
            print("✅ Reserva cancelada exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Operación 9: Intentar cancelar una reserva que no existe
    try:
        sistema_simulacion.cancelar_reserva(999)
    except Exception as e:
        print(f"❌ Error esperado al cancelar reserva: {e}")

    # Operación 10: Procesar una reserva
    try:
        if sistema_simulacion.procesar_reserva(2):
            print("✅ Reserva procesada exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Operación 11: Procesar una reserva cancelada (debería fallar)
    try:
        sistema_simulacion.procesar_reserva(1)
    except Exception as e:
        print(f"❌ Error esperado al procesar reserva cancelada: {e}")

    print("\n" + "=" * 80)
    print("SIMULACIÓN COMPLETADA. REVISA EL ARCHIVO DE LOGS PARA MÁS DETALLES.")
    print("=" * 80)

if __name__ == "__main__":
    # Crear la carpeta de logs usando configuración
    if not os.path.exists(config.CARPETA_LOGS):
        os.makedirs(config.CARPETA_LOGS)

    # Ejecutar simulación
    ejecutar_simulacion()

    # Iniciar la aplicación GUI
    print("\nIniciando la interfaz gráfica...")
    root = tk.Tk()
    app = AplicacionGUI(root)
    root.mainloop()
