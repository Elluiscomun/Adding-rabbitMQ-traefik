from flask import Flask, request, jsonify  # Importa Flask para crear la aplicación web y manejar solicitudes HTTP
from collections import defaultdict  # Importa defaultdict para inicializar automáticamente valores en un diccionario
import pika
import time


registro = [['cliente_app1',0],['cliente_app2',0],['cliente_app3',0]]  # Inicializa un diccionario para almacenar registros de servicios,

time.sleep(15)  # Espera 5 segundos antes de continuar, probablemente para dar tiempo a que otros servicios estén listos
# Establece una conexión con RabbitMQ usando el host 'rabbitmq'
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='client_app1')
channel.queue_declare(queue='client_app2')
channel.queue_declare(queue='client_app3')

# Define una función de callback que se ejecutará cuando se reciba un mensaje
def callback(ch, method, properties, body):
    # Imprime el contenido del mensaje recibido
    print(f" [x] Received {body}")

app = Flask(__name__)  # Crea una instancia de la aplicación Flask

@app.route("/registro", methods=["GET"])  # Define una ruta HTTP GET en "/registro"
def obtener_registro():
    calculateMessages()  # Llama a la función para calcular los mensajes en las colas
    return jsonify(registro)

def calculateMessages():

    # Consume mensajes de la cola 'client_app1'
    while True:
        method_frame, properties, body = channel.basic_get(queue='client_app1', auto_ack=True)
        if method_frame:  # Si hay un mensaje en la cola
            registro[0][1] += 1
            print(f" [x] Consumed from client_app1: {body}")
        else:
            break  # Sal del bucle si no hay más mensajes

    # Consume mensajes de la cola 'client_app2'
    while True:
        method_frame, properties, body = channel.basic_get(queue='client_app2', auto_ack=True)
        if method_frame:  # Si hay un mensaje en la cola
            registro[1][1] += 1
            print(f" [x] Consumed from client_app2: {body}")
        else:
            break  # Sal del bucle si no hay más mensajes

    # Consume mensajes de la cola 'client_app3'
    while True:
        method_frame, properties, body = channel.basic_get(queue='client_app3', auto_ack=True)
        if method_frame:  # Si hay un mensaje en la cola
            registro[2][1] += 1
            print(f" [x] Consumed from client_app3: {body}")
        else:
            break  # Sal del bucle si no hay más mensajes
    

if __name__ == "__main__":  # Punto de entrada principal del script
    # Inicia la aplicación Flask en el host 0.0.0.0 (accesible desde cualquier dirección IP) y en el puerto 5000
    app.run(host="0.0.0.0", port=5000)
