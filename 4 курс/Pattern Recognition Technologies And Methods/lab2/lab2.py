import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions

IMAGE_DIR = "./lab2/image" 
WINDOW_SIZES = [(96, 96), (128, 128), (160, 160)]  
STEP_SIZE = (32, 32)  
DETECTION_THRESHOLD = 0.1  

GROUND_TRUTH = [(80, 50, 350, 500)]  

def sliding_window(image, window_size, step_size):
    windows = []  
    for y in range(0, image.shape[0] - window_size[1] + 1, step_size[1]):
        for x in range(0, image.shape[1] - window_size[0] + 1, step_size[0]):
            windows.append((x, y, x + window_size[0], y + window_size[1]))
    return windows

def load_images(image_dir):
    images = []  
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_dir, filename)  
            image = cv2.imread(img_path)  
            if image is not None:
                images.append(image)  
    return images

def build_pretrained_model():
    base_model = MobileNetV2(weights='imagenet', include_top=True)  
    return base_model

def classify_windows_pretrained(image, windows, model):
    predictions = []  
    for (x1, y1, x2, y2) in windows:
        window = image[y1:y2, x1:x2]  
        if window.shape[0] == 0 or window.shape[1] == 0:
            continue  

        window_resized = cv2.resize(window, (224, 224))  
        window_array = img_to_array(window_resized) 
        window_array = preprocess_input(window_array)  
        window_array = np.expand_dims(window_array, axis=0)  

        pred = model.predict(window_array)  
        decoded_preds = decode_predictions(pred, top=1)[0][0]  

        label, confidence = decoded_preds[1], decoded_preds[2]  
        if label in ["tabby_cat", "Persian_cat", "Egyptian_cat", "Siamese_cat"]:
            predictions.append((x1, y1, x2, y2, confidence))  
    return predictions

def non_max_suppression(boxes, scores, overlap_thresh=0.3):
    if len(boxes) == 0:
        return []  

    boxes = np.array(boxes) 
    start_x = boxes[:, 0]  
    start_y = boxes[:, 1]  
    end_x = boxes[:, 2]  
    end_y = boxes[:, 3]  

    area = (end_x - start_x + 1) * (end_y - start_y + 1)  
    indices = np.argsort(scores)  

    picked_boxes = []  

    while len(indices) > 0:
        last = len(indices) - 1  
        i = indices[last]  
        picked_boxes.append(i)  

        xx1 = np.maximum(start_x[i], start_x[indices[:last]])
        yy1 = np.maximum(start_y[i], start_y[indices[:last]])
        xx2 = np.minimum(end_x[i], end_x[indices[:last]])
        yy2 = np.minimum(end_y[i], end_y[indices[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)  
        h = np.maximum(0, yy2 - yy1 + 1)  

        overlap = (w * h) / area[indices[:last]]  
        indices = np.delete(indices, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))

    return picked_boxes  

def calculate_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_gt, y1_gt, x2_gt, y2_gt = box2

    inter_x1 = max(x1, x1_gt)  
    inter_y1 = max(y1, y1_gt)  
    inter_x2 = min(x2, x2_gt)  
    inter_y2 = min(y2, y2_gt)  

    inter_area = max(0, inter_x2 - inter_x1 + 1) * max(0, inter_y2 - inter_y1 + 1)  

    box1_area = (x2 - x1 + 1) * (y2 - y1 + 1)  
    box2_area = (x2_gt - x1_gt + 1) * (y2_gt - y1_gt + 1)  

    iou = inter_area / float(box1_area + box2_area - inter_area)  
    return iou

def compute_metrics(predictions, ground_truths, iou_threshold=0.5):
    TP, FP, FN, TN = 0, 0, 0, 0 

    for pred_box in predictions:
        found_match = False  
        for gt_box in ground_truths:
            iou = calculate_iou(pred_box[:4], gt_box)  
            if iou >= iou_threshold:
                TP += 1  
                found_match = True
                break
        if not found_match:
            FP += 1  

    FN = len(ground_truths) - TP  
    TN = len(predictions) - TP - FP  

    return TP, FP, FN, TN  

images = load_images(IMAGE_DIR)  
model = build_pretrained_model()  

for idx, image in enumerate(images):
    all_predictions = []  

    for window_size in WINDOW_SIZES:
        windows = sliding_window(image, window_size, STEP_SIZE)  
        predictions = classify_windows_pretrained(image, windows, model)  
        all_predictions.extend(predictions)  

    if all_predictions:
        boxes = [(x1, y1, x2, y2) for (x1, y1, x2, y2, _) in all_predictions]  
        scores = [score for (_, _, _, _, score) in all_predictions]  
        selected_indices = non_max_suppression(boxes, scores)  

        image_with_windows = image.copy()  
        for (x1, y1, x2, y2) in boxes:
            cv2.rectangle(image_with_windows, (x1, y1), (x2, y2), (0, 255, 0), 1)  

        plt.figure(figsize=(12, 6))  
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(image_with_windows, cv2.COLOR_BGR2RGB)) 
        plt.title(f"Изображение {idx + 1} - Количество гипотез: {len(boxes)}")  
        plt.axis("off")

        if selected_indices:
            x_min = min([boxes[i][0] for i in selected_indices])  
            y_min = min([boxes[i][1] for i in selected_indices])  
            x_max = max([boxes[i][2] for i in selected_indices])  
            y_max = max([boxes[i][3] for i in selected_indices])  

            image_with_detection = image.copy()  
            cv2.rectangle(image_with_detection, (x_min, y_min), (x_max, y_max), (0, 0, 255), 3)  
            print(f"Обнаружен кот: Общая рамка {(x_min, y_min, x_max, y_max)}")  

            plt.subplot(1, 2, 2)
            plt.imshow(cv2.cvtColor(image_with_detection, cv2.COLOR_BGR2RGB))  
            plt.title(f"Изображение {idx + 1} - Обнаруженный объект: {'Да' if selected_indices else 'Нет'}")  
            plt.axis("off")
            plt.show()

        pred_boxes = [(x1, y1, x2, y2) for (x1, y1, x2, y2, _) in all_predictions]  
        TP, FP, FN, TN = compute_metrics(pred_boxes, GROUND_TRUTH) 

        total_population = TP + FP + FN + TN  
        accuracy = (TP + TN) / total_population if total_population > 0 else 0  

        print(f"Изображение {idx + 1} - Метрики обнаружения:")
        print(f"True Positive (TP): {TP}")
        print(f"False Positive (FP): {FP}")
        print(f"False Negative (FN): {FN}")
        print(f"True Negative (TN): {TN}")
        print(f"Accuracy: {accuracy:.2f}")
