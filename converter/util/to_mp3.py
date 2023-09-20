from pymongo import MongoClient
import os, gridfs, tempfile 
from bson.objectid import ObjectId
import moviepy.editor

# MongoDB and gridfs connection
client = MongoClient(os.environ.get("MONGO_DB_HOST"))
fs_videos = gridfs.GridFS(client.videos)
fs_mp3s = gridfs.GridFS(client.mp3s)

# function to convert video to audio
def start(message):
    """
    Convert video to audio
    store audio to db
    remove video and audio from disk
    """
    try:
        # temp file to store video file
        tf = tempfile.NamedTemporaryFile()

        video_id = message["video_id"]
        out = fs_videos.get(ObjectId(video_id))
        tf.write(out.read())

        # covert to audio
        mp3_file = moviepy.editor.VideoFileClip(tf.name).audio
        #close tf file so it will cleanup
        tf.close()

        mp3_file_path = os.path.join(tempfile.gettempdir(),f"{video_id}.mp3")
        mp3_file.write_audiofile(mp3_file_path)

        # store it mongodb
        with open(mp3_file_path,'rb') as f:
            mp3_id = fs_mp3s.put(f.read())

        # remove audio file from disk
        os.remove(mp3_file_path)

        return mp3_id, None
    
    except Exception as err:
        print(err)
        return None, "Failed to store mp3 in DB"


