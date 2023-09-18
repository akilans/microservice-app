FROM python:3.10-slim-bullseye

RUN apt update \
    && apt install build-essential pkg-config default-libmysqlclient-dev -y --no-install-recommends --no-install-suggests \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6000

CMD [ "python","app.py" ]