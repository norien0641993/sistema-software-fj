# =============================================================================
# Clase Abstracta Servicio
# =============================================================================

from abc import ABC, abstractmethod
from modelos.entidad import Entidad

class Servicio(Entidad, ABC):
    """
    Clase abstracta que define la estructura base para todos los servicios.
    """
    def __init__(self, id_servicio: int, nombre: str, descripcion: str, costo_base: float):
        super().__init__(id_servicio, nombre)
        self._descripcion = descripcion
        self._costo_base = costo_base
        self._disponible = True

    @abstractmethod
    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """
        Método abstracto para calcular el costo del servicio.
        Debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        """
        Método abstracto para validar los parámetros específicos del servicio.
        """
        pass

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = estado

    def obtener_descripcion(self) -> str:
        return f"Servicio: {self.nombre} (ID: {self.id}) - {self._descripcion} (Costo Base: ${self._costo_base:.2f})"

    def __str__(self):
        return self.obtener_descripcion()