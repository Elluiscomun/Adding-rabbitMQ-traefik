import json
import pika
import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SERVICE_ID = os.environ.get('SERVICE_ID', 'unknown')

time.sleep(15)  # Esperar a que el servicio de registro esté disponible

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

channel = connection.channel()

#channel.exchange_declare(exchange='eventos_clientes', exchange_type='direct', durable=True)
channel.queue_declare(queue=f'client_{SERVICE_ID}')
   
#channel.queue_bind(
#    exchange='eventos_clientes',
#    queue=f'client_{SERVICE_ID}',
#    routing_key=f'client_{SERVICE_ID}'  # La misma routing_key usada al publicar
#)

def registrar_servicio():

    
    message = {
        "service_id": SERVICE_ID,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
       channel.basic_publish(exchange='',
                             routing_key=f'client_{SERVICE_ID}',
                             body=json.dumps(message))
       
    except Exception as e:
        print(f"[{SERVICE_ID}] Error: {e}")
        channel.close()
        return {"error": str(e)}

@app.route('/')
def index():
    result = registrar_servicio()
    return jsonify({
        "service": SERVICE_ID,
        "registered": result
    })

if __name__ == "__main__":
    # Registrar periódicamente en segundo plano
    import threading
    def periodic_register():
        while True:
            registrar_servicio()
            time.sleep(10)  # Cada 10 segundos
    
    threading.Thread(target=periodic_register, daemon=True).start()
    
    # Iniciar servidor web
    app.run(host="0.0.0.0", port=5000)