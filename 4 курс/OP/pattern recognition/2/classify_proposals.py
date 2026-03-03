import os
import torch
from torchvision import models, transforms
from PIL import Image
import pandas as pd
import cv2
import xml.etree.ElementTree as ET

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2).to(device)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ИНДЕКСЫ классов ImageNet, соответствующие кошке (пример набора — оставлено как у тебя)
CAT_CLASSES = {281, 282, 283, 284, 285}

def compute_iou(boxA, boxB):
    """
    box format: (x, y, w, h)
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
    inter_w = max(0, xB - xA)
    inter_h = max(0, yB - yA)
    interArea = inter_w * inter_h
    boxAArea = float(boxA[2]) * float(boxA[3])
    boxBArea = float(boxB[2]) * float(boxB[3])
    union = boxAArea + boxBArea - interArea
    if union <= 0:
        return 0.0
    return interArea / union

def parse_voc_xml(xml_path):
    """
    Возвращает список боксов в формате (xmin, ymin, w, h).
    Если xml_path == None или не существует — возвращает [].
    """
    if not xml_path or not os.path.exists(xml_path):
        return []
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        boxes = []
        for obj in root.findall('object'):
            name = obj.find('name').text
            if name is None:
                continue
            if name.strip().lower() == 'cat':
                bndbox = obj.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))
                w = max(0, xmax - xmin)
                h = max(0, ymax - ymin)
                boxes.append((xmin, ymin, w, h))
        return boxes
    except Exception as e:
        print(f"Ошибка парсинга XML {xml_path}: {e}")
        return []

def classify_crop(crop_path, confidence_threshold=0.05):
    try:
        img = Image.open(crop_path).convert('RGB')
        input_tensor = preprocess(img).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(input_tensor)
        probs = torch.softmax(output, dim=1)[0]
        cat_prob = sum(probs[i].item() for i in CAT_CLASSES if i < len(probs))
        pred_class = int(torch.argmax(probs).item())
        confidence = float(probs[pred_class].item())
        is_cat = cat_prob > confidence_threshold
        return {
            'pred_class': pred_class,
            'confidence': confidence,
            'cat_prob': cat_prob,
            'is_cat': is_cat,
            'predicted_label': "cat" if is_cat else "not cat"
        }
    except Exception as e:
        print(f"Ошибка классификации {crop_path}: {e}")
        return {
            'pred_class': -1,
            'confidence': 0.0,
            'cat_prob': 0.0,
            'is_cat': False,
            'predicted_label': "error"
        }

def visualize_results(image_path, results_subdir, top_n=1):
    """
    Оставил твою визуализацию с минимальными правками.
    Ожидается, что results_subdir/<base>_classifications.csv уже есть.
    """
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    csv_path = os.path.join(results_subdir, f"{base_name}_classifications.csv")
    if not os.path.exists(csv_path):
        print(f"Нет результатов классификации для {base_name}")
        return
    
    df = pd.read_csv(csv_path)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        return
    
    orig_h, orig_w = img.shape[:2]
    valid_df = df[df['cat_prob'] > 0.05].copy()
    
    if valid_df.empty:
        # print(f"Нет валидных предложений для {base_name}")
        return
    
    valid_df['final_score'] = (
        0.6 * valid_df['cat_prob'] +
        0.3 * valid_df['score'] +
        0.1 * (1 - valid_df['energy'])
    )
    
    top_df = valid_df.sort_values("final_score", ascending=False).head(top_n)
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
    
    for idx, row in top_df.iterrows():
        mask_path = os.path.join(results_subdir, row['mask_file'])
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            continue
        
        mask_resized = cv2.resize(mask, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)
        contours, _ = cv2.findContours(mask_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color = colors[idx % len(colors)]
        cv2.drawContours(img, contours, -1, color, 2)
        
        label = f"Cat: {row['cat_prob']:.2f}"
        x, y = int(row['x']), int(row['y'])
        cv2.putText(img, label, (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    vis_path = os.path.join(results_subdir, f"{base_name}_visualization.jpg")
    cv2.imwrite(vis_path, img)
    print(f"Визуализация сохранена: {vis_path}")

def process_all_images(image_dir, results_dir, iou_threshold=0.3):
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    all_proposals = []
    total_tp = total_fp = total_tn = total_fn = 0

    print("\nClassifying proposals...")

    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        results_subdir = os.path.join(results_dir, base_name)
        os.makedirs(results_subdir, exist_ok=True)

        proposals_path = os.path.join(results_subdir, f"{base_name}_proposals.csv")
        if not os.path.exists(proposals_path):
            # Try older filename: "<base>_proposals.csv" vs "<base>_proposals.csv"
            proposals_path_alt = os.path.join(results_subdir, f"{base_name}_proposals.csv")
            if not os.path.exists(proposals_path_alt):
                print(f"No proposals found for {image_file}. Skipping.")
                continue
            else:
                proposals_path = proposals_path_alt

        # Определяем источник GT (scaled xml или оригинал)
        scaled_xml_path = os.path.join(results_subdir, f"{base_name}_scaled.xml")
        original_xml_path = os.path.join(image_dir, f"{base_name}.xml")
        
        if os.path.exists(scaled_xml_path):
            gt_source = scaled_xml_path
            gt_type = "scaled"
        elif os.path.exists(original_xml_path):
            gt_source = original_xml_path
            gt_type = "original"
        else:
            gt_source = None
            gt_type = "none"
        
        print(f"\nUsing {gt_type} XML for {base_name}: {gt_source if gt_source else 'NOT FOUND'}")
        
        gt_boxes = parse_voc_xml(gt_source) if gt_source else []
        print(f"Found {len(gt_boxes)} GT cat boxes for {base_name}")
        if gt_boxes:
            print(f"GT boxes coordinates: {gt_boxes}")

        try:
            proposals_df = pd.read_csv(proposals_path)
        except Exception as e:
            print(f"Ошибка чтения proposals csv {proposals_path}: {e}")
            continue

        classifications = []
        # counters per image
        img_tp = img_fp = img_tn = img_fn = 0

        for _, row in proposals_df.iterrows():
            crop_path = os.path.join(results_subdir, row['crop']) if 'crop' in row and pd.notna(row['crop']) else None
            # если crop файл не найден — пропускаем классификацию, но сохраняем запись
            result = classify_crop(crop_path) if crop_path and os.path.exists(crop_path) else {
                'pred_class': -1, 'confidence': 0.0, 'cat_prob': 0.0, 'is_cat': False, 'predicted_label': 'no_crop'
            }

            # Убедимся, что proposal поля числовые
            try:
                proposal_box = (int(row['x']), int(row['y']), int(row['w']), int(row['h']))
            except Exception:
                # Попробуем взять другие имена столбцов, иначе пропустим
                proposal_box = (int(row.get('X', 0)), int(row.get('Y', 0)), int(row.get('W', 0)), int(row.get('H', 0)))

            # Вычислить max IoU с GT
            max_iou = 0.0
            best_gt_idx = -1
            if gt_boxes:
                for gi, gt in enumerate(gt_boxes):
                    iou = compute_iou(proposal_box, gt)
                    if iou > max_iou:
                        max_iou = iou
                        best_gt_idx = gi


            gt_is_cat = max_iou >= iou_threshold

            # подсчёт таблицы истинности (на уровне proposal)
            if result['is_cat'] and gt_is_cat:
                img_tp += 1
            elif result['is_cat'] and not gt_is_cat:
                img_fp += 1
            elif not result['is_cat'] and gt_is_cat:
                img_fn += 1
            else:
                img_tn += 1

            result.update({
                'image': base_name,
                'id': int(row['id']) if 'id' in row and pd.notna(row['id']) else int(row.name),
                'x': int(row['x']),
                'y': int(row['y']),
                'w': int(row['w']),
                'h': int(row['h']),
                'score': float(row['score']) if 'score' in row and pd.notna(row['score']) else 0.0,
                'area': float(row['area']) if 'area' in row and pd.notna(row['area']) else (int(row['w']) * int(row['h'])),
                'energy': float(row['energy']) if 'energy' in row and pd.notna(row['energy']) else 0.0,
                'mask_file': row['mask_file'] if 'mask_file' in row and pd.notna(row['mask_file']) else "",
                'crop': row['crop'] if 'crop' in row and pd.notna(row['crop']) else "",
                'gt_is_cat': gt_is_cat,
                'max_iou': max_iou,
                'best_gt_idx': best_gt_idx
            })
            classifications.append(result)
            all_proposals.append(result)

        # Сохранение per-image csv
        out_csv = os.path.join(results_subdir, f"{base_name}_classifications.csv")
        df_out = pd.DataFrame(classifications)
        # Приводим порядок столбцов полезный
        cols = ['pred_class','confidence','cat_prob','is_cat','predicted_label',
                'image','id','x','y','w','h','score','area','energy','mask_file','crop',
                'gt_is_cat','best_gt_idx','max_iou']
        cols = [c for c in cols if c in df_out.columns]
        df_out.to_csv(out_csv, index=False, columns=cols)
        print(f"Saved classifications CSV: {out_csv}")

        # Суммируем глобально
        total_tp += img_tp
        total_fp += img_fp
        total_fn += img_fn
        total_tn += img_tn

        print(f"Image {base_name} counts — TP: {img_tp}, FP: {img_fp}, FN: {img_fn}, TN: {img_tn}")

        # Сохраняем визуализацию
        image_path = os.path.join(image_dir, image_file)
        visualize_results(image_path, results_subdir, top_n=1)

    # Сохраняем итоговую таблицу истинности по всем изображениям
    summary_path = os.path.join(results_dir, "classification_summary.csv")
    summary = {
        'total_TP': total_tp,
        'total_FP': total_fp,
        'total_FN': total_fn,
        'total_TN': total_tn
    }
    accuracy = (total_tp + total_tn) / (total_tp + total_fp + total_fn + total_tn)
    
    pd.DataFrame([summary]).to_csv(summary_path, index=False)
    print("\nOverall counts:", summary)
    print(f"Summary saved to: {summary_path}")
    print(f"\naccuracy: {accuracy}")


if __name__ == "__main__":
    IMAGE_DIR = "images"
    RESULTS_DIR = "results"
    IOU_THRESHOLD = 0.5

    if not os.path.exists(IMAGE_DIR):
        raise FileNotFoundError(f"Папка с изображениями не найдена: {IMAGE_DIR}")
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    process_all_images(IMAGE_DIR, RESULTS_DIR, IOU_THRESHOLD)
