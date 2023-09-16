from flask import Flask, request
from flask_mysqldb import MySQL
import os, datetime
import jwt

app = Flask(__name__)

# Required for myql connection
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


mysql = MySQL(app)

# Health check login
@app.route("/health")
def health():
    '''
    Router for checking helath
    '''
    return "healthy"

# login route
@app.route("/login", methods=["POST"])
def login():
    '''
    Router for basic auth
    Check for Basic Authorzation header
    Validate against DB 
    '''
    # Check authorization header
    auth = request.authorization
    if auth:
        # get username and password
        username = auth.username
        password = auth.password

        # check user exists or not
        cur = mysql.connection.cursor()
        result = cur.execute(f"SELECT email,password FROM users WHERE email='{username}'")

        if result > 0:
            # get users data
            user_row = cur.fetchone()
            if password == user_row[1]:
                # generate jwt token
                return generate_jwt(username,True)
            else:
                return "Invalid credentials", 401
        else:
            return "User not found", 401

    else:
        return "Missing Authorization header", 401


# validate route
@app.route("/validate", methods=["POST"])
def validate():
    '''
    Router for jwt token validation
    Check for Basic Authorzation header
    Validate against JWT 
    '''
    # Check authorization header
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"]
        jwt_token = auth.split(" ")[1]

        # validate jwt token
        decoded = validate_jwt(jwt_token)
        if decoded:
            return decoded
        else:
            return "Invalid token", 403
    else:
        return "Missing Authorization header", 401
    

# Generate JWT token
def generate_jwt(username,is_admin):
    '''
    Generate JWT token
    Expires after an hour
    '''
    encoded_jwt_token = jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
            "admin": is_admin
        }, 
        os.environ.get("JWT_SECRET"), 
        algorithm="HS256"
    )
    return encoded_jwt_token

# validate JWT token
def validate_jwt(jwt_token):
    try:
        decoded_token = jwt.decode(jwt_token,os.environ.get("JWT_SECRET"),algorithms=["HS256"])
        return decoded_token
    except:
        return False

# call the main function
if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
