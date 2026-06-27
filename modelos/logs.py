# =============================================================================
# Sistema de Logs
# =============================================================================

import datetime
import traceback
import os
from typing import Optional

class SistemaLogs:
    """
    Clase para gestionar el registro de eventos y errores en un archivo de logs.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SistemaLogs, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        """Inicializa la carpeta de logs y el archivo."""
        self.carpeta_logs = "logs"
        if not os.path.exists(self.carpeta_logs):
            os.makedirs(self.carpeta_logs)
        self.archivo_log = os.path.join(self.carpeta_logs, "sistema.log")

    def registrar(self, tipo: str, mensaje: str, excepcion: Optional[Exception] = None):
        """
        Registra un evento en el archivo de logs.
        Args:
            tipo (str): Tipo de evento (INFO, ERROR, WARNING).
            mensaje (str): Descripción del evento.
            excepcion (Exception, optional): Excepción asociada, si existe.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.archivo_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{tipo}]: {mensaje}\n")
            if excepcion:
                # Encadenamiento de excepciones: se registra el traceback completo
                f.write(f"    Detalles de la excepción: {type(excepcion).__name__}: {excepcion}\n")
                f.write(f"    Traceback:\n{traceback.format_exc()}\n")
            f.write("-" * 80 + "\n")

    def leer_logs(self) -> str:
        """Lee y retorna el contenido completo del archivo de logs."""
        try:
            with open(self.archivo_log, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "No hay logs registrados aún."