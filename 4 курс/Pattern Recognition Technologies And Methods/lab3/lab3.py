from ultralytics import YOLO

# Построить новую модель
#model = YOLO("yolo11n.yaml")
# Загрузить предобученную модель (рекомендуется для дальнейшего обучения)
model = YOLO("yolo11n.pt")
# Обучить модель на данных датасета небольшого COCO8
#results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

# Продемонстрировать обнаружение объекта на изображенях из папки с прошлой лабы
path = "./lab2/image/"
# Продемонстрировать обнаружение объекта на изображенях из папки с прошлой лабы
results = model([path + "0.jpg", path + "2.jpg", path + "3.jpeg", path + "4.jpg",path + "5.jpg",path + "6.jpg",path + "7.jpg",path + "8.jpg",path + "9.jpg",path + "10.jpg",])
for result in results:
  result.show()

#1 новая модель и обучение
#2 предобученая модель
#3 предобученая модель и обучение