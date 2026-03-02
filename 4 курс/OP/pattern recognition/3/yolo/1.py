import os
import csv
from ultralytics import YOLO

# === Настройки ===
DATASET = "VOC" 
IMG_SIZE = 640
EPOCHS = 100
WORKERS = 0
RESULTS_DIR = "results_output"
os.makedirs(RESULTS_DIR, exist_ok=True)

# === Список моделей ===
MODELS = [
    {"name": "Новая модель", "yaml": "yolo11n.yaml", "pretrained": False},
    {"name": "Предобученная", "yaml": "yolo11n.pt", "pretrained": True, "finetune": False},
    {"name": "Предобученная + дообучение", "yaml": "yolo11n.pt", "pretrained": True, "finetune": True},
]

# === Функция обучения/валидации ===
def run_model(model_info):
    name = model_info["name"]
    yaml_or_pt = model_info["yaml"]
    pretrained = model_info.get("pretrained", False)
    finetune = model_info.get("finetune", False)

    print(f"\n=== Работаем с моделью: {name} ===")
    
    # Создание модели
    model = YOLO(yaml_or_pt)

    # Обучение
    if finetune or (not pretrained):
        print(f"Запуск обучения: {'дообучение' if finetune else 'с нуля'}")
        results = model.train(
            data=DATASET,
            epochs=EPOCHS,
            imgsz=IMG_SIZE,
            workers=WORKERS
        )
        # После обучения делаем валидацию
        val_results = model.val(data=DATASET, workers=WORKERS)
    else:
        # Только валидация для предобученной модели
        val_results = model.val(data=DATASET, workers=WORKERS)

    # Собираем метрики
    metrics = {
        "name": name,
        "mAP@0.5": round(val_results.box.map50, 4),
        "mAP@0.5:0.95": round(val_results.box.map, 4),
        "Precision": round(val_results.box.mp, 4),
        "Recall": round(val_results.box.mr, 4)
    }



    print(f"Метрики модели {name}: {metrics}")
    return metrics

# === Основной цикл ===
all_metrics = []
for model_info in MODELS:
    metrics = run_model(model_info)
    all_metrics.append(metrics)

# === Сохраняем в CSV ===
csv_path = os.path.join(RESULTS_DIR, "results.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "mAP@0.5", "mAP@0.5:0.95", "Precision", "Recall"])
    writer.writeheader()
    for m in all_metrics:
        writer.writerow(m)

print(f"\nCSV сохранён: {csv_path}")

# === Сохраняем в Markdown ===
md_path = os.path.join(RESULTS_DIR, "results.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("| Модель | mAP@0.5 | mAP@0.5:0.95 | Precision | Recall |\n")
    f.write("|-------|---------|--------------|-----------|--------|\n")
    for m in all_metrics:
        f.write(f"| {m['name']} | {m['mAP@0.5']} | {m['mAP@0.5:0.95']} | {m['Precision']} | {m['Recall']} |\n")

print(f"Markdown таблица сохранена: {md_path}")
print("\n=== Скрипт завершён ===")
