# MicroServicio de Productos API (MongoDB)

## Descripción
API REST para gestión de productos usando MongoDB.

---

##  Instalación

### 1. Clonar proyecto
```bash
git clone <REPO>
cd <PROYECTO>
```


### 2. Instalar dependencias
```bash
pip install flask flask-cors pymongo python-dotenv
```

---

## Configuración (.env)

Crear archivo `.env`:

```
PORT=3001
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=productos_db
```

---

##  Ejecución

### Python

```bash
python app.py
```

---

## Endpoints

Base:
```
/api/productos
```

- POST /registrar
- GET /listar
- GET /<producto_id>
- PUT /<producto_id>
- DELETE /<producto_id>

---

## Health check
```
GET /health
```

---

## Obtener productos
GET http://localhost:5001/api/productos/

---

## Crear producto
POST http://localhost:5001/api/productos/
Content-Type: application/json

{
    "nombre": "Laptop Lenovo",
    "descripcion": "Core i7 16GB RAM",
    "precio": 750000,
    "stock": 10
}

---

## Obtener por ID
GET http://localhost:5001/api/productos/COLOQUE_ID

---

## Actualizar
PUT http://localhost:5001/api/productos/COLOQUE_ID
Content-Type: application/json

{
    "precio": 800000,
    "stock": 5
}

---

## Eliminar
DELETE http://localhost:5001/api/productos/COLOQUE_ID

---

## Notas
- Base de datos: MongoDB
- Colección: productos
- API usa Blueprint con prefijo /api/productos
