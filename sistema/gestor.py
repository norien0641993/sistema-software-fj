# =============================================================================
# sistema/gestor.py - Sistema Principal con Configuración Centralizada
# =============================================================================

from typing import List
from config import config  # Importar la configuración

from modelos import (
    Cliente, Servicio, Reserva, SistemaError,
    ReservaInvalidaError, ServicioNoDisponibleError,
    CalculoInconsistenteError, ClienteInvalidoError,
    SistemaLogs,
    ServicioReservaSala, ServicioAlquilerEquipo,
    ServicioAsesoriaEspecializada
)

class SistemaSoftwareFJ:
    """
    Clase principal del sistema que gestiona clientes, servicios y reservas.
    """
    def __init__(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        self._log = SistemaLogs()
        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self):
        """
        Carga datos de ejemplo usando la configuración centralizada.
        """
        # Crear clientes de ejemplo
        self.clientes.append(Cliente(1, "Juan Pérez", "juan@email.com", "3001234567"))
        self.clientes.append(Cliente(2, "María Gómez", "maria.gomez@empresa.com", "3109876543"))
        self.clientes.append(Cliente(3, "Carlos Rodríguez", "carlosr@correo.org", "3155551234"))

        # Crear servicios usando la configuración centralizada
        sala = ServicioReservaSala(
            1, 
            "Reserva Sala VIP", 
            config.obtener_descripcion('sala_vip'),  # Descripción desde config
            config.obtener_precio('sala_vip'),       # Precio desde config
            10
        )
        
        equipo = ServicioAlquilerEquipo(
            2, 
            "Alquiler Laptop Gamer", 
            config.obtener_descripcion('laptop_gamer'),
            config.obtener_precio('laptop_gamer'),
            "Laptop"
        )
        
        asesoria = ServicioAsesoriaEspecializada(
            3, 
            "Asesoría en IA", 
            config.obtener_descripcion('asesoria_ia'),
            config.obtener_precio('asesoria_ia'),
            "Senior"
        )

        # Servicio no disponible
        sala_problema = ServicioReservaSala(
            4, 
            "Sala No Disponible", 
            config.obtener_descripcion('sala_mantenimiento'),
            config.obtener_precio('sala_mantenimiento'),
            5
        )
        sala_problema.disponible = False

        self.servicios.extend([sala, equipo, asesoria, sala_problema])

        # Crear reservas de ejemplo
        try:
            reserva1 = Reserva(1, self.clientes[0], self.servicios[0], 3)
            self.reservas.append(reserva1)

            reserva2 = Reserva(2, self.clientes[1], self.servicios[1], 5)
            self.reservas.append(reserva2)

            reserva3 = Reserva(3, self.clientes[2], self.servicios[3], 2)
            self.reservas.append(reserva3)
        except SistemaError as e:
            self._log.registrar("ERROR", "Error al cargar una reserva de ejemplo", e)

    def _generar_id_cliente(self) -> int:
        """Genera un nuevo ID único para clientes."""
        if not self.clientes:
            return 1
        max_id = max(cliente.id for cliente in self.clientes)
        return max_id + 1

    def _generar_id_reserva(self) -> int:
        """Genera un nuevo ID único para reservas."""
        if not self.reservas:
            return 1
        max_id = max(reserva.id for reserva in self.reservas)
        return max_id + 1

    def registrar_cliente(self, nombre: str, email: str, telefono: str) -> Cliente:
        """Registra un nuevo cliente en el sistema."""
        try:
            nuevo_id = self._generar_id_cliente()
            cliente = Cliente(nuevo_id, nombre, email, telefono)
            self.clientes.append(cliente)
            self._log.registrar("INFO", f"Cliente registrado: {cliente.nombre} (ID: {cliente.id})")
            return cliente
        except ClienteInvalidoError as e:
            self._log.registrar("ERROR", "Intento de registro de cliente inválido", e)
            raise
        except Exception as e:
            self._log.registrar("ERROR", "Error inesperado al registrar cliente", e)
            raise SistemaError("Error inesperado en el registro del cliente.") from e

    def crear_reserva(self, id_cliente: int, id_servicio: int, duracion: int) -> Reserva:
        """Crea una nueva reserva con validación y manejo de excepciones."""
        try:
            cliente = next((c for c in self.clientes if c.id == id_cliente), None)
            if not cliente:
                raise ReservaInvalidaError(f"Cliente con ID {id_cliente} no encontrado.")

            servicio = next((s for s in self.servicios if s.id == id_servicio), None)
            if not servicio:
                raise ReservaInvalidaError(f"Servicio con ID {id_servicio} no encontrado.")

            nuevo_id = self._generar_id_reserva()
            reserva = Reserva(nuevo_id, cliente, servicio, duracion)

            self.reservas.append(reserva)
            self._log.registrar("INFO", f"Reserva creada exitosamente: {reserva}")
            return reserva

        except (ReservaInvalidaError, ServicioNoDisponibleError, CalculoInconsistenteError) as e:
            self._log.registrar("ERROR", f"Error al crear la reserva para cliente {id_cliente} y servicio {id_servicio}", e)
            raise
        except Exception as e:
            self._log.registrar("ERROR", "Error inesperado al crear la reserva", e)
            raise SistemaError("Error inesperado en la creación de la reserva.") from e

    def cancelar_reserva(self, id_reserva: int) -> bool:
        """Cancela una reserva existente por su ID."""
        try:
            reserva = next((r for r in self.reservas if r.id == id_reserva), None)
            if not reserva:
                raise ReservaInvalidaError(f"Reserva con ID {id_reserva} no encontrada.")

            reserva.cancelar()
            return True
        except (ReservaInvalidaError, ServicioNoDisponibleError) as e:
            self._log.registrar("ERROR", f"Error al cancelar la reserva {id_reserva}", e)
            raise
        except Exception as e:
            self._log.registrar("ERROR", f"Error inesperado al cancelar la reserva {id_reserva}", e)
            raise SistemaError("Error inesperado en la cancelación de la reserva.") from e

    def procesar_reserva(self, id_reserva: int) -> bool:
        """Procesa/ejecuta una reserva existente."""
        try:
            reserva = next((r for r in self.reservas if r.id == id_reserva), None)
            if not reserva:
                raise ReservaInvalidaError(f"Reserva con ID {id_reserva} no encontrada.")

            reserva.procesar()
            return True
        except (ReservaInvalidaError, CalculoInconsistenteError) as e:
            self._log.registrar("ERROR", f"Error al procesar la reserva {id_reserva}", e)
            raise
        except Exception as e:
            self._log.registrar("ERROR", f"Error inesperado al procesar la reserva {id_reserva}", e)
            raise SistemaError("Error inesperado en el procesamiento de la reserva.") from e

    def obtener_clientes(self) -> List[Cliente]:
        return self.clientes

    def obtener_servicios(self) -> List[Servicio]:
        return self.servicios

    def obtener_reservas(self) -> List[Reserva]:
        return self.reservas