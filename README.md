# Microservice Architecture and System Design with Python & Kubernetes

- This microservice application allows authenticated user to upload the video which they want to convert to mp3 format

### Architecture

![Microservice - Architecture](https://github.com/akilans/microservice-app/blob/main/images/app-architecture.png?raw=true)

### Services

- [Auth Service - Python Flask, MySQL](https://github.com/akilans/microservice-app/tree/main/flask-auth)
- [Gateway Service - Python Flask, RabbitMQ, MongoDB](https://github.com/akilans/microservice-app/tree/main/flask-gateway)
- [Converter Service - Python moviepy, RabbitMQ, MongoDB](https://github.com/akilans/microservice-app/tree/main/converter)
- [Notification Service - Python Email, RabbitMQ ](https://github.com/akilans/microservice-app/tree/main/notification)
