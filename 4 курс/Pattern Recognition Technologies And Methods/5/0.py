from ultralytics import YOLO
model = YOLO("yolov8n.pt")
video_path = "d7577ff4-VID_20230408_143103.mp4"  # Замени на свое видео или скачай пример с датасета
model.predict(source=video_path, show=True, save=True, save_txt=True)