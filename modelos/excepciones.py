# =============================================================================
# Excepciones Personalizadas del Sistema
# =============================================================================

class SistemaError(Exception):
    """Excepción base para errores del sistema."""
    pass

class ClienteInvalidoError(SistemaError):
    """Se lanza cuando los datos del cliente no son válidos."""
    pass

class ServicioNoDisponibleError(SistemaError):
    """Se lanza cuando el servicio solicitado no está disponible."""
    pass

class ReservaInvalidaError(SistemaError):
    """Se lanza cuando los datos de la reserva son incorrectos."""
    pass

class CalculoInconsistenteError(SistemaError):
    """Se lanza cuando hay un error en los cálculos de costos."""
    pass