# =============================================================================
# Clase Cliente
# =============================================================================

from modelos.excepciones import ClienteInvalidoError
from modelos.entidad import Entidad

class Cliente(Entidad):
    """
    Clase que representa a un cliente del sistema con validaciones robustas.
    """
    def __init__(self, id_cliente: int, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente, nombre)
        self._email = None
        self._telefono = None
        # Usamos los setters para aplicar validaciones robustas
        self.email = email
        self.telefono = telefono

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        """Valida el formato del email."""
        if not valor or "@" not in valor:
            raise ClienteInvalidoError(f"Email inválido: '{valor}'. Debe contener '@'.")
        self._email = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Valida que el teléfono tenga al menos 7 dígitos."""
        # Limpiamos el valor de posibles caracteres no numéricos para la validación
        valor_limpio = ''.join(filter(str.isdigit, valor))
        if len(valor_limpio) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'. Debe tener al menos 7 dígitos.")
        # Guardamos el valor original (formato puede ser variado)
        self._telefono = valor

    def obtener_descripcion(self) -> str:
        """Retorna una descripción del cliente."""
        return f"Cliente: {self.nombre} (ID: {self.id}), Email: {self.email}, Tel: {self.telefono}"