import cv2
import numpy as np
import argparse
import imutils
import time
import os
from imutils.video import VideoStream, FPS

# Обработка аргументов командной строки
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
ap.add_argument("-s", "--source", type=int, default=0, help="video source (default: 0 for webcam)")
args = ap.parse_args()

# Проверка существования файлов
if not os.path.isfile(args.prototxt):
    print(f"Error: Prototxt file '{args.prototxt}' not found.")
    exit(1)

if not os.path.isfile(args.model):
    print(f"Error: Model file '{args.model}' not found.")
    exit(1)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", 
           "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", 
           "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args.prototxt, args.model)

print("[INFO] starting video stream...")
vs = VideoStream(src=args.source).start()
time.sleep(2.0)
fps = FPS().start()

frame_count = 0
frame_interval = 5

try:
    while True:
        frame = vs.read()
        if frame is None:
            print("[ERROR] Failed to capture frame. Exiting...")
            break
        frame_count += 1

        if frame_count % frame_interval == 0:
            frame = imutils.resize(frame, width=1600)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

            net.setInput(blob)
            detections = net.forward()

            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > args.confidence:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            fps.update()

finally:
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    vs.stop()
