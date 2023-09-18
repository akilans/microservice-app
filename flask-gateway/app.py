from flask import Flask, request
from auth import access
import json, gridfs, pika, os
from flask_pymongo import PyMongo
from storage import util

app = Flask(__name__)

#mongo db and gridfs connection
mongo_video = PyMongo(app, uri=f"{os.environ.get('MONGO_DB_HOST')}/videos")
mongo_mp3 = PyMongo(app, uri=f"{os.environ.get('MONGO_DB_HOST')}/mp3s")
fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)


# login route
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
        user_details_json = json.loads(user_details)
        if user_details_json["admin"]:
            if len(request.files) != 1:
                return "Allowed file is one", 400
            else:
                for _, file in request.files.items():
                    # upload video to mongodb
                    # publish message to rabbitmq
                    err = util.upload_publish(file,fs_videos,user_details_json["user"])
                if err:
                    return err
                else:
                    return "Success!!!"
                    
        else:
            return "You are not authorized to upload a file", 401

#Download mp3 file
@app.route("/download",methods=["GET"])
def download():
    """
    Validate token
    Allow download for valid token
    """
    user_details, err = access.validate_jwt(request)

    if err:
        return err
    else:
        user_details_json = json.loads(user_details)
        if user_details_json["admin"]:
            return "Download success!"
        else:
            return "You are not authorized to upload a file", 401
        

# Call main function
if __name__ == "__main__":
    app.run("0.0.0.0", 6000)