import pika, os, json
# rabbitmq connection
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USERNAME'), os.environ.get('RABBITMQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('RABBITMQ_HOST'),
    port=os.environ.get('RABBITMQ_PORT'),
    credentials=credentials
    ))
channel = connection.channel()
channel.queue_declare("test")

message = {
    "id": 4,
    "name": "Inba",
    "location": "Tenkasi"
}

channel.basic_publish(exchange="",routing_key="test",body=json.dumps(message))

print("Message successfully sent!...")

