import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
import pyttsx3

engine =  pyttsx3.init()
engine. setProperty("rate", 120)

def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)
    cv2.imshow("Gray Scale",gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        data =  str(barcodeData).split(" ")
        data = "_".join(data)
        data =  data.split("/")
        print(data)
        data = "-".join(data)
        print(data)
        data  =  requests.get(f"http://127.0.0.1:5000/PassengerEntryPlatform/{data}/{1}").json()
        print(f"The data is {data}")
        type =  data["Type"]
        if(type == "True"):
            print("Saying")
            engine.say(data["msg"])
            engine.runAndWait()
        elif(type == "False"):
            print("Saying")
            engine.say(data["msg"])
            engine.runAndWait()
        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break