# =============================================================================
# Servicios Especializados (Herencia y Polimorfismo)
# =============================================================================

from modelos.excepciones import CalculoInconsistenteError, ReservaInvalidaError
from modelos.servicio import Servicio

class ServicioReservaSala(Servicio):
    """Servicio para reserva de salas."""
    def __init__(self, id_servicio: int, nombre: str, descripcion: str, costo_base: float, capacidad: int):
        super().__init__(id_servicio, nombre, descripcion, costo_base)
        self.capacidad = capacidad

    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """
        Calcula el costo de la reserva de sala.
        Args:
            duracion (int): Duración en horas.
            **kwargs: Puede incluir 'impuesto' (float) o 'descuento' (float).
        """
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración debe ser mayor a 0 horas.")
        costo = self._costo_base * duracion

        # Manejo de parámetros opcionales (sobrecarga simulada)
        impuesto = kwargs.get('impuesto', 0.0)
        descuento = kwargs.get('descuento', 0.0)

        if impuesto < 0 or descuento < 0:
            raise CalculoInconsistenteError("Impuesto y descuento no pueden ser negativos.")

        costo = costo * (1 + impuesto)
        costo = costo * (1 - descuento)
        return max(0, costo)  # El costo no puede ser negativo

    def validar_parametros(self, **kwargs) -> bool:
        """Valida que los parámetros para reservar sala sean correctos."""
        try:
            duracion = kwargs.get('duracion', 0)
            if duracion <= 0:
                raise ReservaInvalidaError("La duración para reservar sala debe ser positiva.")
            return True
        except Exception as e:
            raise ReservaInvalidaError("Parámetros inválidos para ServicioReservaSala.") from e


class ServicioAlquilerEquipo(Servicio):
    """Servicio para alquiler de equipos."""
    def __init__(self, id_servicio: int, nombre: str, descripcion: str, costo_base: float, tipo_equipo: str):
        super().__init__(id_servicio, nombre, descripcion, costo_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """
        Calcula el costo del alquiler de equipo.
        Args:
            duracion (int): Duración en días.
            **kwargs: Puede incluir 'multa' (float) por daños o retraso.
        """
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración del alquiler debe ser mayor a 0 días.")
        costo = self._costo_base * duracion

        multa = kwargs.get('multa', 0.0)
        if multa < 0:
            raise CalculoInconsistenteError("La multa no puede ser negativa.")
        costo += multa

        return max(0, costo)

    def validar_parametros(self, **kwargs) -> bool:
        """Valida que los parámetros para alquilar equipo sean correctos."""
        try:
            duracion = kwargs.get('duracion', 0)
            if duracion <= 0:
                raise ReservaInvalidaError("La duración para alquilar equipo debe ser positiva.")
            return True
        except Exception as e:
            raise ReservaInvalidaError("Parámetros inválidos para ServicioAlquilerEquipo.") from e


class ServicioAsesoriaEspecializada(Servicio):
    """Servicio para asesorías especializadas."""
    def __init__(self, id_servicio: int, nombre: str, descripcion: str, costo_base: float, nivel_experto: str):
        super().__init__(id_servicio, nombre, descripcion, costo_base)
        self.nivel_experto = nivel_experto

    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """
        Calcula el costo de la asesoría.
        Args:
            duracion (int): Duración en horas.
            **kwargs: Puede incluir 'recargo_urgencia' (float).
        """
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración de la asesoría debe ser mayor a 0 horas.")
        costo = self._costo_base * duracion

        recargo = kwargs.get('recargo_urgencia', 0.0)
        if recargo < 0:
            raise CalculoInconsistenteError("El recargo por urgencia no puede ser negativo.")
        costo += recargo

        return max(0, costo)

    def validar_parametros(self, **kwargs) -> bool:
        """Valida que los parámetros para la asesoría sean correctos."""
        try:
            nivel = kwargs.get('nivel_experto', self.nivel_experto)
            if not nivel:
                raise ReservaInvalidaError("El nivel de experto no puede estar vacío.")
            return True
        except Exception as e:
            raise ReservaInvalidaError("Parámetros inválidos para ServicioAsesoriaEspecializada.") from e