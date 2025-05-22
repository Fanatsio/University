import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import logging
from typing import List, Tuple, Optional
import tensorflow as tf

# Configuration
IMAGE_DIR = "./lab2/image"
WINDOW_SIZES = [(96, 96), (128, 128), (160, 160)]
STEP_SIZE = (32, 32)
DETECTION_THRESHOLD = 0.1
IOU_THRESHOLD = 0.5
OVERLAP_THRESHOLD = 0.3
CAT_CLASSES = ["tabby_cat", "Persian_cat", "Egyptian_cat", "Siamese_cat"]
GROUND_TRUTH = [(80, 50, 350, 500)]

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sliding_window(image: np.ndarray, window_size: Tuple[int, int], 
                 step_size: Tuple[int, int]) -> List[Tuple[int, int, int, int]]:
    """Generate sliding windows across an image."""
    windows = []
    h, w = image.shape[:2]
    win_w, win_h = window_size
    
    for y in range(0, h - win_h + 1, step_size[1]):
        for x in range(0, w - win_w + 1, step_size[0]):
            windows.append((x, y, x + win_w, y + win_h))
    return windows

def load_images(image_dir: str) -> List[np.ndarray]:
    """Load images from directory with error handling."""
    images = []
    if not os.path.exists(image_dir):
        logger.error(f"Directory {image_dir} does not exist")
        return images
    
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img_path = os.path.join(image_dir, filename)
                image = cv2.imread(img_path)
                if image is None:
                    logger.warning(f"Failed to load image: {img_path}")
                    continue
                images.append(image)
                logger.info(f"Loaded image: {img_path}")
            except Exception as e:
                logger.error(f"Error loading {img_path}: {str(e)}")
    
    return images

def build_pretrained_model() -> MobileNetV2:
    """Initialize MobileNetV2 model with error handling."""
    try:
        model = MobileNetV2(weights='imagenet', include_top=True)
        # Optimize model for inference
        model = tf.keras.models.Model(
            inputs=model.input,
            outputs=model.output
        )
        return model
    except Exception as e:
        logger.error(f"Error building model: {str(e)}")
        raise

def classify_windows_pretrained(image: np.ndarray, windows: List[Tuple[int, int, int, int]], 
                              model: MobileNetV2) -> List[Tuple[int, int, int, int, float]]:
    """Classify windows using MobileNetV2 in batches."""
    predictions = []
    batch_size = 32
    window_batch = []
    
    for (x1, y1, x2, y2) in windows:
        try:
            window = image[y1:y2, x1:x2]
            if window.shape[0] == 0 or window.shape[1] == 0:
                continue
                
            window_resized = cv2.resize(window, (224, 224))
            window_array = img_to_array(window_resized)
            window_array = preprocess_input(window_array)
            window_batch.append((window_array, (x1, y1, x2, y2)))
            
            # Process batch when full
            if len(window_batch) >= batch_size:
                batch_arrays = np.array([w[0] for w in window_batch])
                preds = model.predict(batch_arrays, verbose=0)
                
                for i, pred in enumerate(preds):
                    decoded_preds = decode_predictions(np.expand_dims(pred, 0), top=1)[0][0]
                    label, confidence = decoded_preds[1], decoded_preds[2]
                    if label in CAT_CLASSES and confidence > DETECTION_THRESHOLD:
                        x1, y1, x2, y2 = window_batch[i][1]
                        predictions.append((x1, y1, x2, y2, confidence))
                window_batch = []
                
        except Exception as e:
            logger.warning(f"Error processing window ({x1}, {y1}, {x2}, {y2}): {str(e)}")
    
    # Process remaining windows
    if window_batch:
        batch_arrays = np.array([w[0] for w in window_batch])
        preds = model.predict(batch_arrays, verbose=0)
        
        for i, pred in enumerate(preds):
            decoded_preds = decode_predictions(np.expand_dims(pred, 0), top=1)[0][0]
            label, confidence = decoded_preds[1], decoded_preds[2]
            if label in CAT_CLASSES and confidence > DETECTION_THRESHOLD:
                x1, y1, x2, y2 = window_batch[i][1]
                predictions.append((x1, y1, x2, y2, confidence))
    
    return predictions

def non_max_suppression(boxes: List[Tuple[int, int, int, int]], 
                       scores: List[float], 
                       overlap_thresh: float = 0.3) -> List[int]:
    """Apply Non-Maximum Suppression to filter overlapping boxes."""
    if not boxes:
        return []
        
    boxes = np.array(boxes)
    scores = np.array(scores)
    
    start_x, start_y = boxes[:, 0], boxes[:, 1]
    end_x, end_y = boxes[:, 2], boxes[:, 3]
    
    area = (end_x - start_x + 1) * (end_y - start_y + 1)
    indices = np.argsort(scores)
    picked = []
    
    while indices.size > 0:
        i = indices[-1]
        picked.append(i)
        
        xx1 = np.maximum(start_x[i], start_x[indices[:-1]])
        yy1 = np.maximum(start_y[i], start_y[indices[:-1]])
        xx2 = np.minimum(end_x[i], end_x[indices[:-1]])
        yy2 = np.minimum(end_y[i], end_y[indices[:-1]])
        
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        
        overlap = (w * h) / area[indices[:-1]]
        indices = np.delete(indices, np.concatenate(([len(indices)-1], 
                                                    np.where(overlap > overlap_thresh)[0])))
    
    return picked

def calculate_iou(box1: Tuple[int, int, int, int], 
                 box2: Tuple[int, int, int, int]) -> float:
    """Calculate Intersection over Union (IoU) for two boxes."""
    x1, y1, x2, y2 = box1
    x1_gt, y1_gt, x2_gt, y2_gt = box2
    
    inter_x1 = max(x1, x1_gt)
    inter_y1 = max(y1, y1_gt)
    inter_x2 = min(x2, x2_gt)
    inter_y2 = min(y2, y2_gt)
    
    inter_area = max(0, inter_x2 - inter_x1 + 1) * max(0, inter_y2 - inter_y1 + 1)
    
    box1_area = (x2 - x1 + 1) * (y2 - y1 + 1)
    box2_area = (x2_gt - x1_gt + 1) * (y2_gt - y1_gt + 1)
    
    return inter_area / (box1_area + box2_area - inter_area)

def compute_metrics(predictions: List[Tuple[int, int, int, int]], 
                   ground_truths: List[Tuple[int, int, int, int]], 
                   iou_threshold: float = 0.5) -> Tuple[int, int, int, int]:
    """Compute detection metrics (TP, FP, FN, TN)."""
    TP, FP, FN = 0, 0, len(ground_truths)
    matched_gt = set()
    
    for pred_box in predictions:
        found_match = False
        for i, gt_box in enumerate(ground_truths):
            if i in matched_gt:
                continue
            if calculate_iou(pred_box, gt_box) >= iou_threshold:
                TP += 1
                FN -= 1
                matched_gt.add(i)
                found_match = True
                break
        if not found_match:
            FP += 1
    
    # TN is typically not meaningful in object detection, set to 0
    TN = 0
    return TP, FP, FN, TN

def main():
    """Main function to run cat detection pipeline."""
    try:
        images = load_images(IMAGE_DIR)
        if not images:
            logger.error("No valid images found")
            return
            
        model = build_pretrained_model()
        
        for idx, image in enumerate(images):
            logger.info(f"Processing image {idx + 1}")
            all_predictions = []
            
            for window_size in WINDOW_SIZES:
                windows = sliding_window(image, window_size, STEP_SIZE)
                predictions = classify_windows_pretrained(image, windows, model)
                all_predictions.extend(predictions)
            
            if not all_predictions:
                logger.info(f"No cat detections in image {idx + 1}")
                continue
                
            boxes = [(x1, y1, x2, y2) for x1, y1, x2, y2, _ in all_predictions]
            scores = [score for _, _, _, _, score in all_predictions]
            selected_indices = non_max_suppression(boxes, scores, OVERLAP_THRESHOLD)
            
            # Visualize all proposals
            image_with_windows = image.copy()
            for x1, y1, x2, y2 in boxes:
                cv2.rectangle(image_with_windows, (x1, y1), (x2, y2), (0, 255, 0), 1)
            
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.imshow(cv2.cvtColor(image_with_windows, cv2.COLOR_BGR2RGB))
            plt.title(f"Image {idx + 1} - Proposals: {len(boxes)}")
            plt.axis("off")
            
            # Visualize final detection
            if selected_indices:
                x_min = min(boxes[i][0] for i in selected_indices)
                y_min = min(boxes[i][1] for i in selected_indices)
                x_max = max(boxes[i][2] for i in selected_indices)
                y_max = max(boxes[i][3] for i in selected_indices)
                
                image_with_detection = image.copy()
                cv2.rectangle(image_with_detection, (x_min, y_min), 
                            (x_max, y_max), (0, 0, 255), 3)
                
                logger.info(f"Cat detected in image {idx + 1}: "
                           f"Bounding box {(x_min, y_min, x_max, y_max)}")
                
                plt.subplot(1, 2, 2)
                plt.imshow(cv2.cvtColor(image_with_detection, cv2.COLOR_BGR2RGB))
                plt.title(f"Image {idx + 1} - Detected: {'Yes' if selected_indices else 'No'}")
                plt.axis("off")
            
            plt.tight_layout()
            plt.savefig(f'detection_result_{idx + 1}.png')
            plt.close()
            
            # Compute and log metrics
            pred_boxes = [(x1, y1, x2, y2) for x1, y1, x2, y2, _ in all_predictions]
            TP, FP, FN, TN = compute_metrics(pred_boxes, GROUND_TRUTH, IOU_THRESHOLD)
            
            total = TP + FP + FN + TN
            accuracy = (TP + TN) / total if total > 0 else 0
            precision = TP / (TP + FP) if TP + FP > 0 else 0
            recall = TP / (TP + FN) if TP + FN > 0 else 0
            
            logger.info(f"Image {idx + 1} - Detection Metrics:")
            logger.info(f"True Positive (TP): {TP}")
            logger.info(f"False Positive (FP): {FP}")
            logger.info(f"False Negative (FN): {FN}")
            logger.info(f"True Negative (TN): {TN}")
            logger.info(f"Accuracy: {accuracy:.2f}")
            logger.info(f"Precision: {precision:.2f}")
            logger.info(f"Recall: {recall:.2f}")
            
    except Exception as e:
        logger.error(f"Error in main pipeline: {str(e)}")
        raise
    finally:
        # Clean up
        plt.close('all')

if __name__ == "__main__":
    main()