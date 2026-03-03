from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
from ultralytics import YOLO

model_path = "runs/detect/train4/weights/best.pt"  # Укажите путь к вашей модели
model = YOLO(model_path)

tracker = DeepSort(max_age=70, n_init=5, max_cosine_distance=0.5, nn_budget=None)

video_path = "IMG_1922.MOV"
output_path = "output_video_3.mp4"
cap = cv2.VideoCapture(video_path)

fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    
    # Улучшение качества обработки: используем исходное разрешение если возможно
    # или увеличиваем разрешение для YOLO
    h, w = frame.shape[:2]

    inference_size = 832
    resized_frame = cv2.resize(frame, (inference_size, inference_size))

    results = model(resized_frame, conf=0.5, iou=0.45, verbose=False)

    detections = []
    for result in results:
        if len(result.boxes.xyxy) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            
            for box, conf, cls in zip(boxes, confidences, classes):
                x1, y1, x2, y2 = box[:4]
                
                # Масштабируем координаты обратно в оригинальное разрешение
                scale_x = frame_width / inference_size
                scale_y = frame_height / inference_size
                x1 = int(x1 * scale_x)
                x2 = int(x2 * scale_x)
                y1 = int(y1 * scale_y)
                y2 = int(y2 * scale_y)
                
                # Фильтрация по размеру: исключаем слишком маленькие/большие объекты
                width = x2 - x1
                height = y2 - y1
                min_size = 10  # Минимальный размер
                max_size = min(frame_width, frame_height) // 2  # Максимум половины кадра
                
                if min_size <= width <= max_size and min_size <= height <= max_size:
                    # Формат для трекера: [x1, y1, width, height, confidence, class_id]
                    detections.append([[x1, y1, width, height], float(conf), int(cls)])

    tracks = tracker.update_tracks(detections, frame=frame)

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

    out.write(frame)

    if frame_count % 15 == 0:
        print(f"Обработано: {frame_count} кадров, обнаружено объектов: {len(detections)}")

cap.release()
out.release()
print(f"Обработка завершена, результат сохранён в {output_path}")
