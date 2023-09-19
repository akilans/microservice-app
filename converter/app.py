import pika, os, json
from util import to_mp3
from sys import exit

# rabbitmq connection
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USERNAME'), os.environ.get('RABBITMQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('RABBITMQ_HOST'),
    port=os.environ.get('RABBITMQ_PORT'),
    credentials=credentials
    ))
channel = connection.channel()


# callback function to consume message details
def callback(ch, method, properties, body):
    # read message
    message = json.loads(body)
    mp3_id, err = to_mp3.start(message)
    
    if err is None:
        print("Audio saved n DB successfully...")
        print("Time to publish message")

        message["mp3_id"] = mp3_id
            # publish message to rabbitmq
        try:
            # create queue if needed
            channel.queue_declare("audio")
            channel.basic_publish(
                exchange="",
                routing_key="audio",
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as err:
            print(err)
            ch.basic_nack(delivery_tag=method.delivery_tag)
            print("Failed to publish message to audio queue")
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)
        print("Failed to save audio...")

# main function
def main():
    # create queue if needed
    channel.queue_declare("video")

    # consume message
    channel.basic_consume(
        queue="video",
        on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

# call main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        exit(0)