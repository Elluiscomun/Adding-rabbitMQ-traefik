import pika
import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SERVICE_ID = os.environ.get('SERVICE_ID', 'unknown')

time.sleep(15)  # Esperar a que el servicio de registro esté disponible

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))


def registrar_servicio():
    channel = connection.channel()
    channel.queue_declare(queue=f'client_{SERVICE_ID}')

    try:
       channel.basic_publish(exchange='',
                             routing_key=f'client_{SERVICE_ID}',
                             body='Soy cliente')
       channel.close()
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