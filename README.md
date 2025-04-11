

# Proyecto de Monitoreo con RabbitMQ y Flask

## Descripción

Este proyecto implementa un sistema de monitoreo distribuido utilizando:

- **RabbitMQ** como broker de mensajes
- **Flask** para servicios web
- **Traefik** como reverse proxy
- Un **panel de monitoreo** basado en HTML/JavaScript

## Componentes

### Cliente (`cliente_app.py`)

- Publica mensajes de tipo "heartbeat" a RabbitMQ cada 10 segundos
- Cada cliente tiene un identificador único (`SERVICE_ID`)

### Registro (`registro_app.py`)

- Consume los mensajes de RabbitMQ
- Expone una API REST para consultar estadísticas

### Panel de monitoreo (`monitor.html`)

- Muestra el estado de los servicios y los eventos recibidos
- Se actualiza automáticamente cada 5 segundos

## Acceso a RabbitMQ

- Interfaz de administración: [http://localhost:15672/#/queues](http://localhost:15672/#/queues)

## Requisitos

- Docker y Docker Compose
- Python 3.8 o superior
- RabbitMQ

## Variables de entorno

| Variable       | Descripción                          | Valor por defecto |
|----------------|--------------------------------------|-------------------|
| `SERVICE_ID`   | Identificador del cliente            | `unknown`         |

## Instrucciones de uso

1. Clonar el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd [DIRECTORIO_DEL_PROYECTO]
   ```

2. Levantar los servicios:
   ```bash
   docker-compose up --build
   ```

3. Acceder a los siguientes servicios desde el navegador:
   - Panel de monitoreo: http://localhost/monitor
   - API de registro: http://localhost/registro
   - Dashboard de Traefik: http://localhost/dashboard

## Autenticación

El endpoint `/registro` está protegido con autenticación básica:

- Usuario: `admin`
- Contraseña: `123`

**Nota:** En producción, se deben usar credenciales seguras.



