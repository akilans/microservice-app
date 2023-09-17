from flask import Flask, request
from auth import access

app = Flask(__name__)

@app.route("/login",methods=["POST"])
def login():
    '''
    Router for basic auth
    Check for Basic Authorzation header
    Validate against auth service
    '''
    # Check authorization header
    auth = request.authorization
    if auth:
        token, err = access.login(auth.username,auth.password)
        if token:
            return token
        else:
            return err
    else:
        return "Missing Authorization header", 401

#Upload video file
@app.route("/upload",methods=["POST"])
def upload():
    """
    Validate token
    Allow upload for valid token
    """
    user_details, err = access.validate_jwt(request)

    if err:
        return err
    else:
        return user_details

# Call main function
if __name__ == "__main__":
    app.run("0.0.0.0", 6000)