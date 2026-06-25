### Microservicio de Órdenes — puerto 5002
@host = http://localhost:5002

### Health
GET {{host}}/health

### Crear orden (cliente_id y producto_id deben EXISTIR en sus microservicios)
POST {{host}}/api/ordenes/  
Content-Type: application/json

{

    "cliente_id": "COLOQUE_ID_CLIENTE",
    "producto_id": "COLOQUE_ID_PRODUCTO",
    "cantidad": 2
}

### Listar órdenes
GET {{host}}/api/ordenes/

### Obtener orden por ID
GET {{host}}/api/ordenes/COLOQUE_ID_ORDEN

### Resumen (orden + cliente + producto)
GET {{host}}/api/ordenes/resumen/COLOQUE_ID_ORDEN

### Crear orden INVÁLIDA (faltan campos)
POST {{host}}/api/ordenes/  
Content-Type: application/json

{ 

"cliente_id": "COLOQUE_ID_CLIENTE" 

}

### Eliminar orden
DELETE {{host}}/api/ordenes/COLOQUE_ID_ORDEN
