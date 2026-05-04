import sys
import cv2
import json
import base64
import argparse
from pathlib import Path
import numpy as np
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--model", default=str(ROOT / "yolov8s.pt"))
parser.add_argument("--confidence", type=float, default=0.5)
args = parser.parse_args()

MODEL_PATH = Path(args.model)
if not MODEL_PATH.is_absolute():
    MODEL_PATH = ROOT / MODEL_PATH

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"YOLO model file was not found: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))
print("READY", flush=True)

while True:
    try:
        line = sys.stdin.readline()

        if not line:
            break

        img_data = base64.b64decode(line)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            print("[]", flush=True)
            continue

        results = model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = box

            if int(class_id) == 0 and score >= args.confidence:
                detections.append({
                    "x": int(x1),
                    "y": int(y1),
                    "w": int(x2 - x1),
                    "h": int(y2 - y1)
                })

        print(json.dumps(detections), flush=True)
    except Exception as ex:
        print(f"YOLO server error: {ex}", file=sys.stderr, flush=True)
        print("[]", flush=True)
