# =============================================================================
# Clase Abstracta Entidad
# =============================================================================

from abc import ABC, abstractmethod

class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    """
    def __init__(self, id_entidad: int, nombre: str):
        self._id = id_entidad
        self._nombre = nombre

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Método abstracto para obtener una descripción de la entidad."""
        pass

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre