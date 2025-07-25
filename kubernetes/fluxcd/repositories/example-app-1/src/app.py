from flask import Flask
import platform
import socket
version = "1.0.0.7"
app = Flask(__name__)

@app.route("/")
def hello():
    return f"Hello World version:{version}, host: {platform.uname()[1]},  IP: {socket.gethostbyname(socket.gethostname())} ! \n"
