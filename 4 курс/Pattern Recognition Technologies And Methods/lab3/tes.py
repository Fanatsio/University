from ultralytics import YOLO

# Построить новую модель
#model = YOLO("yolo11n.yaml")
# Загрузить предобученную модель
model = YOLO("yolo11n.pt")

# 1. Обучить модель (раскомментируйте, если хотите обучить)
# results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

# 2. Оценить точность на валидационной выборке
val_results = model.val(data="coco8.yaml")  # Оценка на валидационной выборке
print("Validation mAP@0.5: ", val_results.box.map50)  # Вывод mAP@0.5
print("Validation mAP@0.5:0.95: ", val_results.box.map)  # Вывод mAP@0.5:0.95
 
# 3. Продемонстрировать обнаружение объектов на изображениях
path = "./lab2/image/"
image_list = ["0.jpg", "2.jpg", "3.jpeg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg"]
image_paths = [path + img for img in image_list]
results = model(image_paths)

for result in results:
    result.show()  # Показать результаты детекции