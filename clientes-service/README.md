# clientes-service — Microservicio de Clientes

API REST de Clientes con persistencia NoSQL (MongoDB). Permite registrar, listar, obtener, actualizar y eliminar clientes. Es consumido por otros microservicios (como Órdenes) para validar la existencia de clientes antes de crear pedidos.

**Puerto:** `3003`  
**Base de datos:** MongoDB, base `clientes_db`, colección `clientes`  
**Estándar:** RESTful (JSON)

---

## Arquitectura interna (capas)

```
clientes-service/
├── run.py                     # Punto de entrada de la aplicación
├── app/
│   ├── __init__.py           # Fábrica de la aplicación Flask
│   ├── config.py             # Configuración (variables de entorno)
│   ├── models/
│   │   └── cliente.py        # Modelo Cliente (operaciones MongoDB)
│   ├── controllers/
│   │   └── cliente_controller.py  # Lógica de negocio
│   └── routes/
│       └── cliente_routes.py      # Definición de rutas
├── tests/
│   └── test_api.rest         # Pruebas con REST Client
├── .env                       # Variables de entorno
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

---

## Requisitos previos

Para que el microservicio funcione correctamente, debe estar corriendo:

- **MongoDB** en `localhost:27017`
- **Python 3.10+`

---

## Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/clientes-service.git
cd clientes-service
```

### 2. Crear y activar entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
PORT=3003
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=clientes_db
FLASK_ENV=development
DEBUG=True
```

### 5. Ejecutar el microservicio
```bash
python run.py
```

---

## Variables de entorno

| Variable | Por defecto | Descripción |
|----------|-------------|-------------|
| `PORT` | `3003` | Puerto del microservicio |
| `MONGODB_URI` | `mongodb://localhost:27017/` | Conexión a MongoDB |
| `MONGODB_DB` | `clientes_db` | Base de datos |
| `FLASK_ENV` | `production` | Entorno de ejecución |
| `DEBUG` | `False` | Modo debug (True/False) |

---

## Endpoints

**Base URL:** `http://localhost:3003`

---

### GET `/health` — Health Check

Verifica que el servicio está funcionando.

**Respuesta (200 OK):**
```json
{
    "status": "healthy",
    "service": "clientes",
    "version": "1.0.0"
}
```

---

### POST `/api/clientes/registrar` — Registrar cliente

Registra un nuevo cliente en la base de datos. Valida que todos los campos estén presentes y que el email no esté duplicado.

**Body:**
```json
{
    "nombre": "Carlos Rodriguez",
    "email": "carlos@email.com",
    "telefono": "2222-3333",
    "direccion": "Curridabat, San Jose"
}
```

**Respuesta (201 Created):**
```json
{
    "mensaje": "Cliente registrado exitosamente",
    "cliente": {
        "_id": "550e8400-e29b-41d4-a716-446655440000",
        "nombre": "Carlos Rodriguez",
        "email": "carlos@email.com",
        "telefono": "2222-3333",
        "direccion": "Curridabat, San Jose",
        "fechaRegistro": "2024-01-15T10:30:00.123456"
    }
}
```

**Errores:**
- `400 Bad Request`: Campos requeridos faltantes
- `400 Bad Request`: El email ya está registrado
- `500 Internal Server Error`: Error interno del servidor

---

### GET `/api/clientes/listar` — Listar clientes

Lista todos los clientes registrados con soporte de paginación.

**Parámetros de consulta (opcionales):**
- `limite`: Número de clientes por página (default: 100)
- `offset`: Desplazamiento para paginación (default: 0)

**Ejemplo:** `/api/clientes/listar?limite=10&offset=0`

**Respuesta (200 OK):**
```json
{
    "total": 25,
    "offset": 0,
    "limite": 10,
    "clientes": [
        {
            "_id": "550e8400-e29b-41d4-a716-446655440000",
            "nombre": "Carlos Rodriguez",
            "email": "carlos@email.com",
            "telefono": "2222-3333",
            "direccion": "Curridabat, San Jose",
            "fechaRegistro": "2024-01-15T10:30:00.123456"
        }
    ]
}
```

---

### GET `/api/clientes/<id>` — Obtener cliente por ID

Obtiene un cliente específico por su ID. Este endpoint es utilizado para comunicación inter-servicio (ej: Servicio de Órdenes valida que el cliente existe).

**Respuesta (200 OK):**
```json
{
    "_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Carlos Rodriguez",
    "email": "carlos@email.com",
    "telefono": "2222-3333",
    "direccion": "Curridabat, San Jose",
    "fechaRegistro": "2024-01-15T10:30:00.123456"
}
```

**Errores:**
- `404 Not Found`: Cliente no encontrado

---

### PUT `/api/clientes/<id>` — Actualizar cliente

Actualiza un cliente existente. Permite actualizar uno o varios campos.

**Body (ejemplo - actualización parcial):**
```json
{
    "nombre": "Carlos Rodriguez Actualizado",
    "telefono": "9999-8888",
    "direccion": "Nueva direccion, San Jose"
}
```

**Respuesta (200 OK):**
```json
{
    "mensaje": "Cliente actualizado exitosamente",
    "cliente": {
        "_id": "550e8400-e29b-41d4-a716-446655440000",
        "nombre": "Carlos Rodriguez Actualizado",
        "email": "carlos@email.com",
        "telefono": "9999-8888",
        "direccion": "Nueva direccion, San Jose",
        "fechaRegistro": "2024-01-15T10:30:00.123456"
    }
}
```

**Errores:**
- `400 Bad Request`: Campos vacíos o email duplicado
- `404 Not Found`: Cliente no encontrado

---

### DELETE `/api/clientes/<id>` — Eliminar cliente

Elimina un cliente de la base de datos.

**Respuesta (200 OK):**
```json
{
    "mensaje": "Cliente eliminado exitosamente",
    "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Errores:**
- `404 Not Found`: Cliente no encontrado

---

## Comunicación inter-servicio

Este microservicio expone el endpoint `GET /api/clientes/<id>` para que otros servicios puedan consultar la existencia de un cliente.

**Ejemplo de consumo desde Servicio de Órdenes:**
```python
import requests

def verificar_cliente(cliente_id):
    url = f"http://localhost:3003/api/clientes/{cliente_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None
```

---

## Pruebas

### REST Client (VS Code)
El archivo `tests/test_api.rest` contiene todas las pruebas para ejecutar con la extensión REST Client de VS Code.

### Postman
Se incluye el archivo `Microservicio_Clientes.postman_collection.json` que puede importarse en Postman para probar todos los endpoints.

---

## Resumen de endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check del servicio |
| POST | `/api/clientes/registrar` | Registrar nuevo cliente |
| GET | `/api/clientes/listar` | Listar todos los clientes |
| GET | `/api/clientes/{id}` | Obtener cliente por ID |
| PUT | `/api/clientes/{id}` | Actualizar cliente |
| DELETE | `/api/clientes/{id}` | Eliminar cliente |

---

## Solución de problemas comunes

### Error: "No module named 'flask_cors'"
```bash
pip install -r requirements.txt
```

### Error: "pymongo.errors.ConnectionFailure"
- Verificar que MongoDB está corriendo: `mongod` o `docker ps`
- Verificar la URI en `.env`

### Error: "Address already in use" (puerto 3003 ocupado)
- Cambiar PORT en `.env`: `PORT=3004`
- O matar el proceso que usa el puerto

### Error: El entorno virtual no se activa
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

## Tecnologías utilizadas

- **Python 3.10+** - Lenguaje de programación
- **Flask 2.3.3** - Framework web
- **PyMongo 4.5.0** - Driver para MongoDB
- **Flask-CORS 4.0.0** - Manejo de CORS
- **python-dotenv 1.0.0** - Variables de entorno
- **MongoDB** - Base de datos NoSQL
