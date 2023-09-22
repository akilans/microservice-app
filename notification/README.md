# Notification Service

- This service will trigger email once mp3 is ready

### Setup

- Run auth service, Gateway service and converter service
- Run local SMTP server
- Run Mongodb and Rabbitmq and export variables

```bash
python3 -m smtpd -c DebuggingServer -n localhost:1025
export RABBITMQ_HOST=192.168.1.8
export RABBITMQ_PORT=5672
export RABBITMQ_USERNAME=akilan
export RABBITMQ_PASSWORD=akilan
```
