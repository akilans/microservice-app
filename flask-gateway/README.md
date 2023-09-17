# Flask - Gateway Service

This service does the following things

- Connect to auth service to authenticate user and get token
- Validate token for every request
- Allows authenticated user to upload video file
- Stores video file to mongodb gridfs
- Publish message to rabbitmq queue

### setup

- Run auth service and AUTH_SVC_URL env variable
- export AUTH_SVC_URL=http://192.168.49.2:32001

```bash
cd flask-gateway
python3 -m venv .venv
source .venv/bin/activate
pip install requirements.txt
```
