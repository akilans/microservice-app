import pika, os, json
from sys import exit
import smtplib
from email.message import EmailMessage

# rabbitmq connection
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USERNAME'), os.environ.get('RABBITMQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('RABBITMQ_HOST'),
    port=os.environ.get('RABBITMQ_PORT'),
    credentials=credentials
    ))
channel = connection.channel()

#send email
def send_email(body):
    try:
        message = json.loads(body)
        sender_email = "test@localhost.com"
        receiver_email = message["username"]

        msg = f"Download MP3 with id - {message['mp3_id']}"
        # python3 -m smtpd -c DebuggingServer -n localhost:1025
        server = smtplib.SMTP('localhost', 1025)
        server.set_debuglevel(1)
        server.sendmail(sender_email, receiver_email, "Download MP3 with id - "+message['mp3_id'])
        server.quit()
    except Exception as err:
        print(err)
        return err

# callback function to consume message details
def callback(ch, method, properties, body):
    print(f"Consuming message {json.loads(body)}")
    # read message
    err = send_email(body)
    
    if err is None:
        print("Email sent successfully...")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)
        print("Failed to send email...")

# main function
def main():
    # create queue if needed
    channel.queue_declare("audio")

    # consume message
    channel.basic_consume(
        queue="audio",
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