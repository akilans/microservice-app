import pika, os, json

def print_message(ch, method, properties,body):
    print(f"{json.loads(body)}")
# rabbitmq connection
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USERNAME'), os.environ.get('RABBITMQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('RABBITMQ_HOST'),
    port=os.environ.get('RABBITMQ_PORT'),
    credentials=credentials
    ))
channel = connection.channel()
channel.queue_declare("test")

channel.basic_consume(queue="test",auto_ack=True,on_message_callback=print_message)

print("Start consuming....")
channel.start_consuming()