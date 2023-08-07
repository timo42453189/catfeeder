import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera


camera = PiCamera()
rawCapture = PiRGBArray(camera)


camera.capture(rawCapture, format="bgr")
frame = rawCapture.array
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

cv2.imshow("test", frame_rgb)
cv2.waitKey(0)

print(frame)
