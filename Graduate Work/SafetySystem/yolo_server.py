import sys
import cv2
import json
import base64
import numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

while True:

    line = sys.stdin.readline()

    if not line:
        continue

    img_data = base64.b64decode(line)
    nparr = np.frombuffer(img_data, np.uint8)

    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(frame, verbose=False)[0]

    detections = []

    for box in results.boxes.data.tolist():

        x1, y1, x2, y2, score, class_id = box

        if int(class_id) == 0:
            detections.append({
                "x": int(x1),
                "y": int(y1),
                "w": int(x2 - x1),
                "h": int(y2 - y1)
            })

    print(json.dumps(detections))
    sys.stdout.flush()