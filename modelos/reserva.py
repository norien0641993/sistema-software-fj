# =============================================================================
# Clase Reserva
# =============================================================================

import datetime
from typing import Optional

from modelos.excepciones import (
    SistemaError, ServicioNoDisponibleError, 
    ReservaInvalidaError, CalculoInconsistenteError
)
from modelos.logs import SistemaLogs
from modelos.cliente import Cliente
from modelos.servicio import Servicio

class Reserva:
    """
    Clase que integra cliente, servicio y duración para gestionar una reserva.
    """
    def __init__(self, id_reserva: int, cliente: Cliente, servicio: Servicio, duracion: int,
                 fecha_inicio: Optional[datetime.datetime] = None):
        self.id = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.fecha_inicio = fecha_inicio if fecha_inicio else datetime.datetime.now()
        self.estado = "PENDIENTE"  # PENDIENTE, CONFIRMADA, CANCELADA, COMPLETADA
        self.costo_total = 0.0
        self._log = SistemaLogs()
        self._confirmar_reserva_interna()  # Se confirma automáticamente al crear

    def _confirmar_reserva_interna(self):
        """Método interno que confirma la reserva y calcula el costo."""
        try:
            # Validar que el servicio esté disponible
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible.")

            # Validar parámetros del servicio
            self.servicio.validar_parametros(duracion=self.duracion)

            # Calcular el costo (usando sobrecarga de métodos)
            self.costo_total = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMADA"
            self._log.registrar("INFO", f"Reserva {self.id} confirmada. Cliente: {self.cliente.nombre}, Servicio: {self.servicio.nombre}, Costo: ${self.costo_total:.2f}")

        except (ReservaInvalidaError, ServicioNoDisponibleError, CalculoInconsistenteError) as e:
            self.estado = "FALLIDA"
            self._log.registrar("ERROR", f"Error al confirmar la reserva {self.id}", e)
            raise
        except Exception as e:
            self.estado = "FALLIDA"
            self._log.registrar("ERROR", f"Error inesperado al confirmar la reserva {self.id}", e)
            raise SistemaError("Error inesperado en el proceso de confirmación de reserva.") from e

    def cancelar(self):
        """Cancela la reserva si está en estado CONFIRMADA o PENDIENTE."""
        try:
            if self.estado not in ["CONFIRMADA", "PENDIENTE"]:
                raise ReservaInvalidaError(f"No se puede cancelar una reserva en estado '{self.estado}'.")

            if self.estado == "CONFIRMADA":
                if not self.servicio.disponible:
                    raise ServicioNoDisponibleError("No se puede liberar el servicio porque no estaba disponible.")
                self.estado = "CANCELADA"
                self._log.registrar("INFO", f"Reserva {self.id} cancelada exitosamente.")
            else:
                self.estado = "CANCELADA"
                self._log.registrar("INFO", f"Reserva {self.id} cancelada.")

        except (ReservaInvalidaError, ServicioNoDisponibleError) as e:
            self._log.registrar("ERROR", f"Error al cancelar la reserva {self.id}", e)
            raise
        except Exception as e:
            self._log.registrar("ERROR", f"Error inesperado al cancelar la reserva {self.id}", e)
            raise SistemaError("Error inesperado en el proceso de cancelación de reserva.") from e

    def procesar(self):
        """Simula el procesamiento/ejecución de la reserva."""
        try:
            if self.estado != "CONFIRMADA":
                raise ReservaInvalidaError(f"No se puede procesar una reserva en estado '{self.estado}'.")
            if self.costo_total <= 0:
                raise CalculoInconsistenteError(f"El costo total de la reserva {self.id} es {self.costo_total}, no se puede procesar.")

            self.estado = "COMPLETADA"
            self._log.registrar("INFO", f"Reserva {self.id} procesada/completada exitosamente.")
        except (ReservaInvalidaError, CalculoInconsistenteError) as e:
            self.estado = "FALLIDA"
            self._log.registrar("ERROR", f"Error al procesar la reserva {self.id}", e)
            raise
        except Exception as e:
            self.estado = "FALLIDA"
            self._log.registrar("ERROR", f"Error inesperado al procesar la reserva {self.id}", e)
            raise SistemaError("Error inesperado en el proceso de procesamiento de reserva.") from e

    def __str__(self):
        return (f"Reserva #{self.id} - Cliente: {self.cliente.nombre} - Servicio: {self.servicio.nombre} - "
                f"Estado: {self.estado} - Costo: ${self.costo_total:.2f}")
    
# modelos/reserva.py - Parte del método __str__
from config import config

def __str__(self):
    precio_formateado = config.formatear_precio(self.costo_total)
    return (f"Reserva #{self.id} - Cliente: {self.cliente.nombre} - Servicio: {self.servicio.nombre} - "
            f"Estado: {self.estado} - Costo: {precio_formateado}")