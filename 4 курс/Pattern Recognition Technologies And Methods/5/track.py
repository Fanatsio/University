from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
from ultralytics import YOLO

# Инициализация YOLO модели
model_path = "runs/detect/train3/weights/best.pt"  # Укажите путь к вашей модели
model = YOLO(model_path)

# Инициализация трекера DeepSORT
tracker = DeepSort(max_age=70, n_init=5, max_cosine_distance=0.5, nn_budget=None)

# Открываем видео
video_path = "d7577ff4-VID_20230408_143103.mp4"
output_path = "output_video_3.mp4"
cap = cv2.VideoCapture(video_path)

# Получаем информацию о разрешении и FPS видео
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Сжимаем кадр для обработки YOLO
    resized_frame = cv2.resize(frame, (640, 640))

    # Обработка кадра моделью YOLO
    results = model(resized_frame, conf=0.84, iou=0.7)

    detections = []
    for result in results:
        if len(result.boxes.xyxy) > 0:
            # Преобразуем tензор в numpy для удобства
            boxes = result.boxes.xyxy.cpu().numpy()  # Преобразуем в numpy массив
            conf = float(result.boxes.conf.cpu().numpy()[0])  # Уверенность модели
            cls = int(result.boxes.cls.cpu().numpy()[0])  # Класс объекта
            for box in boxes:
                x1, y1, x2, y2 = box[:4]
                # Масштабируем координаты обратно в оригинальное разрешение
                x1 = int(x1 * (frame_width / 640))
                x2 = int(x2 * (frame_width / 640))
                y1 = int(y1 * (frame_height / 640))
                y2 = int(y2 * (frame_height / 640))
                # Формат для трекера: [x1, y1, width, height, confidence, class_id]
                detections.append([[x1, y1, x2 - x1, y2 - y1], conf, cls])

    # Обновляем трекер
    tracks = tracker.update_tracks(detections, frame=frame)

    # Отображаем треки на кадре
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()
        x1, y1, x2, y2 = map(int, ltrb)

        # Рисуем прямоугольник и ID трека
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"ID {track_id}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Сохраняем обработанный кадр
    out.write(frame)

cap.release()
out.release()
print(f"Обработка завершена, результат сохранён в {output_path}")
