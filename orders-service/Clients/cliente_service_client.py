import logging
import requests
from config import Config

logger = logging.getLogger(__name__)


class ServicioNoDisponibleError(Exception):
    """Se lanza cuando un microservicio dependiente no responde."""

    def __init__(self, servicio, detalle=''):
        self.servicio = servicio
        self.detalle = detalle
        super().__init__(f"Servicio '{servicio}' no disponible: {detalle}")


class ClienteServiceClient:

    def __init__(self, base_url=None, timeout=None):
        self.base_url = base_url or Config.CLIENTES_SERVICE_URL
        self.timeout = timeout or Config.SERVICE_TIMEOUT

    def obtener_cliente(self, cliente_id):
        """
        Consulta un cliente por su ID al microservicio de Clientes.

        Devuelve:
            dict  -> si el cliente existe.
            None  -> si el cliente NO existe (HTTP 404).
        Lanza:
            ServicioNoDisponibleError -> si Clientes no responde.
        """
        url = f"{self.base_url}/api/clientes/{cliente_id}"
        logger.info(f"[inter-servicio] GET Clientes -> {url}")

        try:
            respuesta = requests.get(url, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            logger.error(f"[inter-servicio] Error al contactar Clientes: {e}")
            raise ServicioNoDisponibleError('clientes', str(e))

        if respuesta.status_code == 200:
            logger.info(f"[inter-servicio] Cliente {cliente_id} validado OK")
            return respuesta.json()

        if respuesta.status_code == 404:
            logger.warning(f"[inter-servicio] Cliente {cliente_id} no existe")
            return None

        logger.error(f"[inter-servicio] Clientes respondio {respuesta.status_code}")
        raise ServicioNoDisponibleError('clientes', f"HTTP {respuesta.status_code}")
