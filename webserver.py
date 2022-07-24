from flask import Flask
from error import error_handler

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
	app.run(port=80, host="192.168.178.46")
