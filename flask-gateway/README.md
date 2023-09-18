# Flask - Gateway Service

This service does the following things

- Connect to auth service to authenticate user and get token
- Validate token for every request
- Allows authenticated user to upload video file
- Stores video file to mongodb gridfs
- Publish message to rabbitmq queue

### setup

- Run auth service and AUTH_SVC_URL env variable

```bash
export AUTH_SVC_URL=http://192.168.49.2:32001
export MONGO_DB_HOST=mongodb://192.168.1.8:27017
export RABBITMQ_HOST=192.168.1.8
export RABBITMQ_PORT=5672
export RABBITMQ_USERNAME=akilan
export RABBITMQ_PASSWORD=akilan
```

```bash
cd flask-gateway
python3 -m venv .venv
source .venv/bin/activate
pip install requirements.txt
#install rabbitmq
docker run -d --hostname rabbitmq --name rabbitmq-server -e RABBITMQ_DEFAULT_USER=akilan -e RABBITMQ_DEFAULT_PASS=akilan -p15672:15672 -p 5672:5672 rabbitmq:3.12.4-management
# install mongodb
docker run --name mongo -d -p 27017:27017 mongodb/mongodb-community-server:latest
```
