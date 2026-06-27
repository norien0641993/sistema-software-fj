# =============================================================================
# config.py - Configuración Centralizada del Sistema
# =============================================================================

class Configuracion:
    """
    Clase singleton que centraliza toda la configuración del sistema.
    """
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Configuracion, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        """Inicializa todas las configuraciones del sistema."""
        
        # =============================================================
        # CONFIGURACIÓN DE MONEDA
        # =============================================================
        self.MONEDA = "COP"              # Código de moneda
        self.SIMBOLO_MONEDA = "$"        # Símbolo
        self.FORMATO_MONEDA = "COP ${:,.0f}"  # Formato completo
        self.SEPARADOR_MILES = ","       # Separador de miles
        self.DECIMALES = 0               # Número de decimales
        
        # =============================================================
        # PRECIOS DE SERVICIOS EN PESOS COLOMBIANOS (COP)
        # =============================================================
        self.PRECIOS = {
            'sala_vip': 200000.0,           # $200,000 COP por hora
            'laptop_gamer': 120000.0,       # $120,000 COP por día
            'asesoria_ia': 320000.0,        # $320,000 COP por hora
            'sala_mantenimiento': 160000.0, # $160,000 COP por hora
        }
        
        # =============================================================
        # DESCRIPCIONES DE SERVICIOS
        # =============================================================
        self.DESCRIPCIONES = {
            'sala_vip': "Sala con capacidad para 10 personas, equipo de videoconferencia",
            'laptop_gamer': "Laptop de alto rendimiento con tarjeta gráfica dedicada",
            'asesoria_ia': "Consultoría avanzada en Inteligencia Artificial",
            'sala_mantenimiento': "Sala en mantenimiento (no disponible temporalmente)",
        }
        
        # =============================================================
        # CONFIGURACIÓN DE LOGS
        # =============================================================
        self.CARPETA_LOGS = "logs"
        self.ARCHIVO_LOG = "sistema.log"
        self.FORMATO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"
        
        # =============================================================
        # CONFIGURACIÓN DE INTERFAZ
        # =============================================================
        self.TITULO_APP = "Sistema Software FJ - Gestión de Reservas"
        self.TAMANO_VENTANA = "1000x700"
        self.FUENTE_LOGS = ("Courier New", 10)
    
    def formatear_precio(self, valor: float) -> str:
        """
        Formatea un valor numérico como precio en la moneda configurada.
        
        Args:
            valor (float): El valor a formatear
            
        Returns:
            str: El precio formateado (ej: "COP $200,000")
        """
        if self.DECIMALES == 0:
            return f"{self.MONEDA} {self.SIMBOLO_MONEDA}{valor:,.0f}"
        else:
            return f"{self.MONEDA} {self.SIMBOLO_MONEDA}{valor:,.{self.DECIMALES}f}"
    
    def obtener_precio(self, clave: str) -> float:
        """
        Obtiene el precio de un servicio por su clave.
        
        Args:
            clave (str): La clave del servicio (ej: 'sala_vip')
            
        Returns:
            float: El precio del servicio
        """
        return self.PRECIOS.get(clave, 0.0)
    
    def obtener_descripcion(self, clave: str) -> str:
        """
        Obtiene la descripción de un servicio por su clave.
        
        Args:
            clave (str): La clave del servicio
            
        Returns:
            str: La descripción del servicio
        """
        return self.DESCRIPCIONES.get(clave, "Sin descripción")


# Crear una instancia global para facilitar el acceso
config = Configuracion()