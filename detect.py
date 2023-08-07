import os
import io
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import tensorflow as tf
import sys
import time
import logging
from error import error_handler

class AutoDetect:
	def __init__(self, motor):
		#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
		self.id = 1
		self.motor = motor
		self.IM_WIDTH = 1280
		self.IM_HEIGHT = 720
		sys.path.append('..')
		self.MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
		self.CWD_PATH = os.getcwd()
		self.PATH_TO_CKPT = os.path.join(self.CWD_PATH,self.MODEL_NAME,'frozen_inference_graph.pb')
		self.PATH_TO_LABELS = os.path.join(self.CWD_PATH,'data','mscoco_label_map.pbtxt')
		self.NUM_CLASSES = 90
		self.packed = self.init_session()
		self.sess = self.packed[0]
		self.detection_graph = self.packed[1]
		self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
		self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
		self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
		self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
		#self.camera = cv2.VideoCapture(1)
		self.stream = io.BytesIO()
		self.camera = PiCamera()
		self.res = (1280, 720)
		self.camera.resolution = self.res
		self.rawCapture = PiRGBArray(self.camera, size=self.res)
		#self.ret = self.camera.set(3, self.IM_WIDTH)
		#self.ret = self.camera.set(4, self.IM_HEIGHT)


	def init_session(self):
		detection_graph = tf.Graph()
		with detection_graph.as_default():
			od_graph_def = tf.compat.v1.GraphDef()
			with tf.io.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')

		return [tf.compat.v1.Session(graph=detection_graph), detection_graph]


	def detect(self):
		error_handler("AI started", "info")
		counter = 0
		while(True):
			rawCapture = PiRGBArray(self.camera, size=self.res)
			self.camera.capture(rawCapture, format="bgr")
			frame = rawCapture.array
			frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame_expanded = np.expand_dims(frame_rgb, axis=0)
#			cv2.imshow("test", frame)
#			cv2.waitKey(0)
			(boxes, scores, classes, num) = self.sess.run(
			[self.detection_boxes, self.detection_scores, self.detection_classes,
			self.num_detections], feed_dict={self.image_tensor: frame_expanded})
			print("Läuft")
			if classes[0][0] == 17:
				counter = counter + 1
#				print("Logging")
				error_handler(f"Cat Detected -- counter: {counter}", "info")
			else:
				counter = 0
#				logging.info("Counter reseted")

			if counter > 4:
				print("Logging")
				error_handler("Starting Motor", "info")
				response = self.motor.claim(self.id)
				if response == 1:
					error_handler("Error, motor already in use", "error")
				else:
					self.motor.start(self.id)
					self.motor.release(self.id)
					time.sleep(10800)

		#self.camera.release()
