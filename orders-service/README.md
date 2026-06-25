# orders-service — Microservicio de Órdenes

API REST de Órdenes con persistencia NoSQL (MongoDB) y **comunicación
inter-servicio**: antes de registrar un pedido valida que el **cliente** y el
**producto** existan consultando a sus microservicios, y toma el precio real
desde Productos (no se confía al cuerpo de la petición).

- Puerto: **5002**
- Base de datos: MongoDB, base `ordenes_db`, colección `ordenes`
- Estándar: RESTful (JSON)

## Arquitectura interna (capas)

```
run.py            -> rutas Flask + manejo de errores HTTP
Services/         -> lógica de negocio (orden_service) e interfaz (i_orden_service)
Repository/       -> acceso a MongoDB (orden_repository, db_connection_factory)
Entities/         -> entidad Orden (cálculo del total, (de)serialización)
Clients/          -> clientes HTTP a Clientes y Productos (inter-servicio)
```

## Requisitos previos

Para crear órdenes deben estar corriendo:

- MongoDB en `localhost:27017`
- `clientes-service` en `http://localhost:3003`
- `productos-service` en `http://localhost:3001`

## Instalación y ejecución

```bash
cd orders-service
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Variables de entorno (opcionales)

| Variable                | Por defecto             | Descripción                                |
|-------------------------|-------------------------|--------------------------------------------|
| `PORT`                  | `5002`                  | Puerto del microservicio.                  |
| `MONGODB_URI`           | `mongodb://localhost:27017/` | Conexión a MongoDB.                   |
| `MONGODB_DB`            | `ordenes_db`            | Base de datos.                             |
| `CLIENTES_SERVICE_URL`  | `http://localhost:3003` | Microservicio de Clientes.                 |
| `PRODUCTOS_SERVICE_URL` | `http://localhost:3001` | Microservicio de Productos.                |
| `VALIDAR_CLIENTE`       | `True`                  | Validar existencia del cliente.            |
| `VALIDAR_PRODUCTO`      | `True`                  | Validar producto y tomar su precio real.   |
| `SERVICE_TIMEOUT`       | `5`                     | Timeout (seg) hacia los otros servicios.   |

## Endpoints

Base: `http://localhost:5002`

### `GET /health`
Estado del servicio.

### `POST /api/ordenes/` — Crear orden
Valida campos, consulta Clientes y Productos, calcula el total y persiste.

Body:
```json
{ "cliente_id": "<id de cliente>", "producto_id": "<id de producto>", "cantidad": 2 }
```
Respuesta `201`:
```json
{
  "mensaje": "Orden creada exitosamente",
  "orden": {
    "_id": "uuid",
    "cliente_id": "c1", "cliente_nombre": "Ana Mora",
    "producto_id": "p1", "producto_nombre": "Laptop Lenovo",
    "cantidad": 2, "precio_unitario": 750000.0, "total": 1500000.0,
    "estado": "creada", "fechaCreacion": "..."
  }
}
```
Errores: `400` (campos faltantes / cantidad inválida / stock insuficiente),
`404` (cliente o producto inexistente), `502` (un microservicio no responde).

### `GET /api/ordenes/` — Listar órdenes
Soporta `?limite=` y `?offset=`. Respuesta `200` con `total`, `offset`,
`limite` y `ordenes`.

### `GET /api/ordenes/<id>` — Obtener una orden
`200` con la orden, o `404` si no existe.

### `GET /api/ordenes/resumen/<id>` — Resumen (composición)
Agrega la orden con los datos completos del cliente y del producto en una sola
respuesta (API Composition). `200` o `404`.

### `DELETE /api/ordenes/<id>` — Eliminar una orden
`200` o `404`.

## Comunicación inter-servicio (obligatoria)
Al crear una orden, este servicio hace:
- `GET {CLIENTES_SERVICE_URL}/api/clientes/<cliente_id>` → valida el cliente.
- `GET {PRODUCTOS_SERVICE_URL}/api/productos/<producto_id>` → valida el producto
  y obtiene su precio y stock.

Si alguno no existe, la orden no se crea. Los `Clients/` encapsulan estas
llamadas y lanzan `ServicioNoDisponibleError` si un servicio está caído.

## Pruebas
- `tests/test_api.rest` (extensión REST Client de VS Code).
- `Orders.postman_collection.json` (Postman). Llené `cliente_id` y `producto_id`
  con IDs reales obtenidos de los microservicios de Clientes y Productos.
