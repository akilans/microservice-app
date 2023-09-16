# Flask - Auth Service

- Install MySQL
- Create DB, Table and insert data
- Create venv for auth app
- Login route gives jwt token for valid credentials
- validate route gives valid/invalid jwt token

### Setup

```bash
# Install and Create DB
docker container run -d --name auth-container -e MYSQL_ROOT_PASSWORD=password123 -p 3306:3306 mysql:8.0.34
docker exec -it auth-container bash
mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS auth_db;
USE auth_db;
CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

```bash
# MySQL UI client
docker container run -d --name adminer -p 8080:8080 adminer

# Run Flask app
cd flask-auth
python3 -m venv .venv
source .venv/bin/activate
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install -r requirents.txt
flask run --debug
```
