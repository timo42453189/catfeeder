from fastapi import FastAPI
import logging

from error import error_handler


app = FastAPI()

#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
error_handler("API service startet", "info")

@app.get("/start")
async def start():
	with open("servo_control.txt", "w") as f:
		f.write("1")
		f.close()
	return {"Ok": "Starting motor"}
