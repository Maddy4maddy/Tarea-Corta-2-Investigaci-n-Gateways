#  Servicio de Productos API (Flask + MongoDB)

API REST para la gestión de productos usando Flask y MongoDB.

---

##  Instalación rápida

### 1. Clonar o copiar el proyecto
```bash
git clone <TU_REPO>
cd <TU_PROYECTO>
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

Activar:

**Windows**
```bash
venv\Scripts\activate
```

**Linux/Mac**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install flask flask-cors pymongo python-dotenv
```

---

##  Configurar .env

Crear archivo `.env`:

```
PORT=3001
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=productos_db
```

---

## ▶Ejecutar proyecto

```bash
python app.py
```

---

## URL base
http://localhost:3001/api/productos

---

## Health check
GET /health

---

## Endpoints

- POST /registrar
- GET /listar
- GET /<id>
- PUT /<id>
- DELETE /<id>

---

## Tecnologías
- Flask
- MongoDB
- PyMongo
