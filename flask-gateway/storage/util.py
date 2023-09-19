import pika, json, os

# rabbitmq connection
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USERNAME'), os.environ.get('RABBITMQ_PASSWORD'))
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('RABBITMQ_HOST'),
    port=os.environ.get('RABBITMQ_PORT'),
    credentials=credentials
    ))
channel = connection.channel()

"""
Function is used to
Upload video file to mongodb gridfs
Push message to rabbitmq with message
"""

def upload_publish(f,fs,username):
    #upload to mongodb video db
    try:
        video_id = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error while uploading video",500
        
    #message to rabbitmq
    message = {
        "video_id": str(video_id),
        "mp3_id": None,
        "username": username
    }       


    # publish message to rabbitmq
    try:
        # create queue if needed
        channel.queue_declare("video")
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        print(err)
        fs.delete(video_id)
        return "internal server error while publishing message",500
