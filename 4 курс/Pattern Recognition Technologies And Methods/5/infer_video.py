from ultralytics import YOLO

model = YOLO("runs/detect/train3/weights/best.pt")

video_path = "d7577ff4-VID_20230408_143103.mp4"

model.predict(source=video_path, show=True, save=True)