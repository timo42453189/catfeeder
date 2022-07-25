from flask import Flask
import socket
from error import error_handler

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_addres = s.getsockname()[0]
s.close()

app = Flask(__name__)

@app.route("/")
def home():
	content = ""
	with open("app.log", "r") as f:
		c = f.readlines()
		for i in c:
			content += i
			content += "<br>"
	return content

def start():
	error_handler("WebServer service started", "info")
	app.run(port=80, host=IP_addres)
