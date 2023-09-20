# Converter

- This app is used to convert video to mp3
- Consume message published by gateway service
- Download the video from mongodb
- Convert the video to mp3 and svae it to mongodb
- publish a message with mp3 details

### Setup

- Run auth service and Gateway service
- Run Mongodb and Rabbitmq and export variables

```bash
export MONGO_DB_HOST=mongodb://192.168.1.8:27017
export RABBITMQ_HOST=192.168.1.8
export RABBITMQ_PORT=5672
export RABBITMQ_USERNAME=akilan
export RABBITMQ_PASSWORD=akilan
```
